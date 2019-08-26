from discord import DiscordException, Member, opus
from discord.ext.commands import Cog, command

import decbot.audio as audio
import decbot.config as config
from .error import VoiceError, NoVoice, BadVoice

class Voice(Cog):
	""" A bot mixin handling voice-channel related functionality.

	Set up user-facing TTS commands, as well as utilities for joining/leaving
	Discord voice rooms. Commands are expected to raise exceptions on invalid
	state, so that user responses are managed in the error handlers.
	"""
	def __init__(self, bot):
		""" Create a new voice channel mixin.

		:param bot: The bot this cog will be added to.
		:type  bot: discord.ext.commands.Bot
		"""
		self.bot    = bot
		self.voice  = None
		self.mixer  = audio.Mixer()

	def is_joined(self, member):
		""" Check if the bot is currently in the same voice channel as a member.

		:param member: The target member to compare channels against.
		:type  member: discord.Member

		:returns: `True` if the bot is in a voice channel, and that channel has
		          the same ID as that of the member.
		:rtype:   bool

		:raises NoVoice: An error is raised if the member is not joinable; that
		                 is, the member is not in a voice channel.
		"""
		if not member.voice:
			raise NoVoice('"{}" is not in a voice channel.'.format(member.nick))

		return (self.voice and self.voice.channel.id == member.voice.channel.id)

	async def join(self, member):
		""" Join the specified member in their voice channel.

		:param member: The target member to join.
		:type  member: discord.Member

		:raises NoVoice: This error is propogated from `is_joined()`.
		:raises BadVoice: If the bot is currently playing sound in a different
		                  channel, this error is raised.
		:raises discord.DiscordException: Errors from the Discord connection
		                                  methods are propogated.
		"""
		# Joining the already joined channel is a NOP.
		if self.is_joined(member):
			return

		channel = member.voice.channel
		try:
			if self.voice.is_playing():
				raise BadVoice('Bot is active in "{}".'.format(channel.name))

			# If the bot is waiting in a valid voice channel, the voice client
			# can be moved to the new channel rather than connecting anew.
			await self.voice.move_to(channel)
		except AttributeError:
			# The voice client must be `None` or invalid; create a new one.
			self.voice = await channel.connect()

	async def invoke(self, text):
		""" Convert the given text to speech and play it back to Discord.

		This method should only be called when `self.voice` is a valid client.

		:param text: The text to convert to speech.
		:type  text: str

		:raises decbot.audio.AudioError: Any errors from the Mixer, TTS, etc.
		                                 are propogated.
		"""
		req = audio.Request(text)
		audio.tts.convert(req)

		self.mixer.enqueue(req)
		req.cleanup()

		if not self.voice.is_playing():
			self.voice.play(self.mixer)

	@Cog.listener()
	async def on_ready(self):
		""" Retrieve sibling cogs and perform setup before the bot runs.

		At this point, libopus should have been loaded if it was detected by
		Discord. Otherwise, the path will be grabbed from the config file (it
		must be defined at this point).

		:raises RuntimeError: If libopus could still not be loaded, or no path
		                      was defined in the config, an error is raised.
		"""
		self.send_message = self.bot.get_cog('Text').send_message
		if opus.is_loaded():
			return

		path = config.get('opus')
		if path:
			opus.load_opus(path)

		if not opus.is_loaded():
			raise RuntimeError('Could not load libopus.')

	@command()
	async def talk(self, ctx, *, text: str):
		""" synthesize the given text in your voice channel """
		await self.join(ctx.author)
		await self.invoke(text)

	@command()
	async def tell(self, ctx, member: Member, *, text: str):
		""" synthesize the given text in another user's voice channel """
		await self.join(member)
		await self.invoke(text)

	@command()
	async def quiet(self, ctx):
		""" immediately stop playing any actively synthesized text """
		# If the bot is not in the user's channel, silently NOP.
		if not self.is_joined(ctx.author):
			return
		if not self.voice.is_playing():
			raise BadVoice('Bot is not active.')

		self.voice.stop()

	@command()
	async def bye(self, ctx):
		""" disconnect the bot from your voice channel """
		# If the bot is not in the user's channel, silently NOP.
		if not self.is_joined(ctx.author):
			return
		if self.voice.is_playing():
			raise BadVoice('Bot cannot leave while speaking.')

		await self.voice.disconnect()
		self.voice = None

	@talk.error
	@tell.error
	async def voice_error(self, ctx, err):
		# Both `talk` and `tell` errors can be handled the same; they both
		# do the exact same thing, but with different member arguments.
		if type(err) is NoVoice:
			await self.send_message(ctx, 'I can only talk in voice channels.')
		elif type(err) is BadVoice:
			await self.send_message(ctx, 'Hang on, I\'m talking to someone.')
		elif isinstance(err, DiscordException):
			await self.send_message(ctx, 'I can\'t join you right now.')
		else:
			raise err

	@quiet.error
	async def quiet_error(self, ctx, err):
		# `NoVoice` cannot occur; if it does, it is ignored silently.
		if type(err) is BadVoice:
			await self.send_message(ctx, 'I wasn\'t even talking!')
		elif isinstance(err, DiscordException):
			await self.send_message(ctx, 'For some reason, I can\'t stop...')
		elif not isinstance(err, VoiceError):
			raise err

	@bye.error
	async def bye_error(self, ctx, err):
		# `NoVoice` cannot occur; if it does, it is ignored silently.
		if type(err) is BadVoice:
			await self.send_message(ctx, 'Just a second, I\'m almost done.')
		elif isinstance(err, DiscordException):
			await self.send_message(ctx, 'Something\'s keeping me here...')
		elif not isinstance(err, VoiceError):
			raise err


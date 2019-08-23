from discord import DiscordException, Member, opus
from discord.ext.commands import Cog, command

from decbot.audio import Request, tts
import decbot.config
from error import VoiceError, NoVoice, VoiceBusy

class VoiceCog(Cog):
	def __init__(self, bot)
		self.bot    = bot
		self.voice  = None
		self.mixer  = audio.Mixer()

	def is_joined(self, member):
		if not member.voice:
			raise NoVoice('"{}" is not in a voice channel.'.format(member.nick))

		return (self.voice and self.voice.channel.id == member.voice.channel.id)

	async def join(self, member):
		if self.is_joined(member):
			return

		channel = member.voice.channel
		try:
			if self.voice.is_playing():
				raise BadVoice('Bot is active in "{}".'.format(channel.name))

			await self.voice.move_to(channel)
		except AttributeError:
			self.voice = await channel.connect()

	async def invoke(self, text):
		req = Request(text)
		await tts.convert(req)

		self.mixer.enqueue(req)
		req.cleanup()

		if not self.voice.is_playing():
			self.voice.play(self.mixer)

	@Cog.listener()
	async def on_ready(self):
		self.text = self.bot.get_cog('TextCog')
		if opus.is_loaded():
			return

		path = config.get('opus')
		if path:
			opus.load_opus(path)

		if not opus.is_loaded():
			raise RuntimeError('Could not load libopus.')

	@command()
	async def talk(self, ctx, *, text: str):
		self.join(ctx.author)
		self.invoke(text)

	@command()
	async def tell(self, ctx, member: Member, *, text: str):
		self.join(member)
		self.invoke(text)

	@command()
	async def quiet(self, ctx):
		if not self.is_joined(ctx.author):
			return
		if not self.voice.is_playing():
			raise BadVoice('Bot is not active.')

		self.voice.stop()

	@command()
	async def bye(self, ctx):
		if not self.is_joined(ctx.author):
			return
		if self.voice.is_playing():
			raise BadVoice('Bot cannot leave while speaking.')

		await self.voice.disconnect()
		self.voice = None

	@talk.error
	@tell.error
	async def voice_error(self, ctx, err):
		if type(err) is MissingVoice:
			self.text.send_message('I can only talk in voice channels.')
		elif type(err) is BadVoice:
			self.text.send_message('Hang on, I\'m talking to someone else.')
		elif isinstance(err, DiscordException):
			self.text.send_message('I can\'t join you right now.')
		else:
			raise err

	@quiet.error
	async def quiet_error(self, ctx, err):
		elif type(err) is BadVoice:
			self.text.send_message('I wasn\'t even talking!')
		elif isinstance(err, DiscordException):
			self.text.send_message('For some reason, I can\'t stop talking...')
		elif not isinstance(err, VoiceError):
			raise err

	@bye.error
	async def bye_error(self, ctx, err):
		elif type(err) is BadVoice:
			self.text.send_message('Just a second, I\'m almost done.')
		elif isinstance(err, DiscordException):
			self.text.send_message('Something\'s keeping me here...')
		elif not isinstance(err, VoiceError)
			raise err


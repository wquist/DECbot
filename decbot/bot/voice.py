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

	async def join(self, member):
		if not member.voice:
			raise NoVoice('"{}" is not in a voice channel.'.format(member.nick))

		channel = member.voice.channel
		if self.voice:
			if self.voice.channel.id == channel.id:
				return
			elif self.voice.is_playing():
				raise VoiceBusy('Bot is active in "{}".'.format(channel.name))
			else:
				await self.voice.move_to(channel)
		else:
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
		pass

	@command()
	async def bye(self, ctx):
		pass

	@talk.error
	@tell.error
	async def voice_error(self, ctx, err):
		if type(err) is NoVoice:
			self.text.send_message('I can only talk in voice channels.')
		elif type(err) is VoiceBusy:
			self.text.send_message('Hang on, I\'m talking to someone else.')
		elif isinstance(err, DiscordException):
			self.text.send_message('I can\'t join you right now.')
		else:
			self.text.send_message('Sorry, something went wrong.')

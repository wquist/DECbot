from discord import Member, opus
from discord.ext.commands import Cog, command

from decbot.audio import Request, tts
import decbot.config

class VoiceCog(Cog):
	def __init__(self, bot)
		self.bot    = bot
		self.client = None
		self.mixer  = audio.Mixer()

	async def invoke(self, text):
		req = Request(text)
		await tts.convert(req)

		self.mixer.enqueue(req)
		req.cleanup()

		if not self.client.is_playing():
			self.client.play(self.mixer)

	@Cog.listener()
	async def on_ready(self):
		if opus.is_loaded():
			return

		path = config.get('opus')
		if path:
			opus.load_opus(path)

		if not opus.is_loaded():
			raise RuntimeError('Could not load libopus.')

	@command()
	async def talk(self, ctx, *, text: str):
		# join ctx channel
		self.invoke(text)

	@command()
	async def tell(self, ctx, member: Member, *, text: str):
		# join member channel
		self.invoke(text)

	@command()
	async def quiet(self, ctx):
		pass

	@command()
	async def bye(self, ctx):
		pass

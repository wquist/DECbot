from discord import DiscordException
from discord.ext.commands import Cog

class TextCog(Cog):
	def __init__(self, bot):
		self.bot = bot

	async def send_message(self, ctx, message):
		try:
			await ctx.send(message)
			return True
		except DiscordException:
			return False

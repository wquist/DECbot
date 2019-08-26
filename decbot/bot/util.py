from discord import DiscordException
from discord.ext.commands import Cog, command, CommandNotFound, is_owner

class Util(Cog):
	""" A bot mixin handling miscellaneous functionality.

	This sets up info commands and control commands targeting the bot owner.
	"""
	def __init__(self, bot):
		""" Create a new utility mixin.

		:param bot: The bot this cog will be added to.
		:type  bot: discord.ext.commands.Bot
		"""
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		""" Retrieve sibling cogs and perform setup before the bot runs.

		This pulls messaging utilities from the text cog.
		"""
		self.send_message = self.bot.get_cog('Text').send_message

	@Cog.listener()
	async def on_command_error(self, ctx, err):
		""" Handle unknown command errors.

		This method is called when any error occurs, including those in valid
		commands. Filter out only the unknown command exceptions to handle.

		:param ctx: The context from the active error.
		:type  ctx: discord.ext.commands.Context
		:param err: The raised exception object.
		:type  err: Exception
		"""
		if type(err) is CommandNotFound:
			await self.send_message(ctx, 'I don\'t know how to do that.')

	@command()
	async def ping(self, ctx):
		""" check if DECbot is responsive and view server latency """
		ms = round(self.bot.latency * 1000)
		await self.send_message(ctx, 'Pong! ({} ms)'.format(ms))

	@command()
	@is_owner()
	async def quit(self, ctx):
		""" shutdown DECbot (owner only) """
		await self.bot.logout()

from discord import DiscordException
from discord.ext.commands import Cog

class Text(Cog):
	""" A bot mixin handling text messaging related functionality.

	This handles sending messages to users and consumes any errors; if an error
	is thrown while messaging, not much else can be done to notify the user.
	"""
	def __init__(self, bot):
		""" Create a new text messaging mixin.

		:param bot: The bot this cog will be added to.
		:type  bot: discord.ext.commands.Bot
		"""
		self.bot = bot

	async def send_message(self, ctx, message):
		""" Send a text message to the given context.

		If an error occurs while messaging, it is caught and handled silently.

		:param ctx: The context to send the message to. This will usually
		            result in the `ctx.author` user receiving the message.
		:type  ctx: discord.ext.commands.Context
		:param message: The text content of the message to be sent.
		:type  message: str

		:returns: `True` if the message sent successfully, `False` otherwise.
		:rtype:   bool
		"""
		try:
			await ctx.send(message)
			return True
		except DiscordException:
			return False

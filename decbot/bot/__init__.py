from discord.ext.commands import Bot

from .error import BotError
from .text import Text
from .util import Util
from .voice import Voice

def create(prefix = '!dec '):
	""" Create a new DECbot instance.

	This method manages creating the `discord.py` client and attaching the cogs
	defined in this module. Note that the resultant client is not logged in or
	running; this must be done after the fact.

	:param prefix: The prefix needed to invoke the bot within Discord. Note the
	               space; the default uses it to act like a command group.
	:type  prefix: str

	:returns: The newly created bot instance.
	:rtype:   discord.ext.commands.Bot

	:raises discord.DiscordException: Errors from `discord.py` are propogated.
	"""
	client = Bot(command_prefix = prefix)
	for Cog in [Text, Util, Voice]:
		client.add_cog(Cog(client))

	return client

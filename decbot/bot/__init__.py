from discord.ext.commands import Bot

from .text import Text
from .util import Util
from .voice import Voice

def create(prefix = '!dec '):
	client = Bot(command_prefix = prefix)

	client.add_cog(Text(client))
	client.add_cog(Util(client))
	client.add_cog(Voice(client))

	return client

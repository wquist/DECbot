from discord.ext.commands import Bot

from text import TextCog
from voice import VoiceCog

def create(prefix = '!dec '):
	client = Bot(command_prefix = prefix)

	client.add_cog(TextCog(client))
	client.add_cog(VoiceCog(client))

	return client

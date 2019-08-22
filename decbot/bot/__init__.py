from discord.ext.commands import Bot

def create(prefix = '!dec '):
	client = Bot(command_prefix = prefix)

	return client

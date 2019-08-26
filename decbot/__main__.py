from argparse import ArgumentParser
import asyncio
import sys

from . import bot
from . import config

parser = ArgumentParser(description = 'Run a Discord bot that can DECTalk.')
parser.add_argument('-c', '--config', type = str,
	help = 'use the specified path to load the configuration YAML')
parser.add_argument('-V', '--verbose', action = 'store_true',
	help = 'write detailed output to standard out')

args = parser.parse_args()
if args.config is not None:
	config.set_path(args.config)

try:
	client = bot.create()
	token  = config.get('token')

	# Manually run the event loop, since `client.run()` does not seem the same.
	# Exiting with a `^C` does not quit cleanly like this manual version.
	loop = asyncio.get_event_loop()
	loop.run_until_complete(client.start(token))
except KeyboardInterrupt:
	loop.run_until_complete(client.close())

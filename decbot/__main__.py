from argparse import ArgumentParser
import asyncio
import sys

from . import bot
from . import config

def main():
	parser = ArgumentParser(description = 'Run a Discord bot that can DECTalk.')
	parser.add_argument('-c', '--config', type = str,
		help = 'use the specified path to load the configuration YAML')
	parser.add_argument('-i', '--invite', action = 'store_true',
		help = 'generate an oauth invite link for the config client ID')
	parser.add_argument('-p', '--permissions', type = int, default = 3149056,
		help = 'use the given permissions mask (defaults to 3149056)')

	args = parser.parse_args()
	if args.config:
		config.set_path(args.config)

	if args.invite:
		# Note that the default permissions are minimal; `DECbot` must be able
		# to read and write text messages, and also view, join, and speak in
		# voice ones. The default permissions also give DECbot the priority
		# voice option, although this can be unchecked by the admin.
		link = '{}?client_id={}&scope=bot&permissions={}'.format(
			'https://discordapp.com/oauth2/authorize',
			config.get('client'),
			args.permissions
		)

		print(link)
		return 0

	try:
		client = bot.create()
		token  = config.get('token')

		# Manually run the event loop, since `client.run()` does not seem the
		# same. Exiting with a `^C` does not quit cleanly like this version.
		loop = asyncio.get_event_loop()
		loop.run_until_complete(client.start(token))
	except KeyboardInterrupt:
		loop.run_until_complete(client.close())

	return 0

if __name__ == '__main__':
	sys.exit(main())

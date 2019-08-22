from argparse import ArgumentParser

import config

parser = ArgumentParser(description = 'Run a Discord bot that can DECTalk.')
parser.add_argument('-c', '--config', type = str,
	help = 'use the specified path to load the configuration YAML')
parser.add_argument('-V', '--verbose', action = 'store_true',
	help = 'write detailed output to standard out')

args = parser.parse_args()
if args.config is not None:
	config.set_path(args.config)

# Run the bot...
pass

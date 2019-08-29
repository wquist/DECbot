from setuptools import setup, find_packages

setup(
	name             = "decbot",
	version          = "1.0.0",

	author           = 'Wyatt Lindquist',
	author_email     = 'git.wquist@gmail.com',
	description      = "a Discord bot that uses DECtalk text-to-speech",
	long_description = open('./README.md').read(),
	long_description_content_type = 'text/markdown',
	url              = 'https://github.com/wquist/DECbot',
	license          = 'MIT',
	classifiers      = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix"
    ],

	packages         = find_packages(),
	install_requires = ['discord.py', 'pydub', 'pynacl', 'pyyaml'],
	entry_points     = { 'console_scripts': ['decbot = decbot.__main__:main'] }
)

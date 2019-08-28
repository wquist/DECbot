# `DECbot`

_A Discord bot that uses DECtalk text-to-speech (think Stephen Hawking or
Moonbase Alpha)._

`DECbot` uses [wine](https://www.winehq.org/) and the original DECtalk `say.exe`
to synthesize text from text chat into a voice channel. The bot offers a set of
commands allowing users to control how and where `DECbot` synthesizes speech.
The bot can also take multiple commands at once, allowing multiple sounds and
voices to be played back at the same time.


# Requirements

- [Python 3](https://www.python.org/)
- [wine](https://www.winehq.org/)
- A copy of the DECtalk executable and support. This includes `say.exe`,
  `dectalk.dll`, and the dictionary, `dtalk_us.dic`.


# Commands

`DECbot` can synthesize text into different voice channels depending on the
command:
- `!dec talk <text>` plays the text back in the current voice channel.
- `!dec tell <@mention> <text>` plays the text back in the voice channel of the
  user mentioned.

The presence of `DECbot` can also be controlled (to minimize annoyance):
- `!dec quiet` stops the currently playing text immediately.
- `!dec leave` forces the bot to leave its current voice channel.

Both TTS commands run using the "Perfect Paul" voice with phonemes enabled (so
the bot can "sing"). Additional options can be specified as they would in a
normal `say.exe` command: with brackets and a colon (`[:command]`). For example,
`DECbot` can talk as "Frail Frank" by starting the text with `[:nf]`.


# Installation

```bash
$ pip install decbot
```

The bot can also be run from source as a module. In the top level directory:

```bash
$ python -m decbot
```


# Running

A new Discord bot must be set up before the application can be run:

1. Create a new Discord application in the
   [developer portal](http://discordapp.com/developers/applications/me).
2. Fill in the general information, and note the **Client ID** on this page.
3. Set up your bot in the "Bot" tab. Note the **Token** on this page.

Next, to start the application:

1. Create a `DECbot` configuration file. At minimum, this must have the bot
   `token`, and the path to the DECtalk executable, `tts.bin`.
2. Get an invite link (the `client` field must be specified in the config):

	```bash
	$ decbot --invite
	```

3. Have the Discord server administrator add the bot. Note that it must be
   granted the ability to read and send text messages, and be able to view,
   join, and talk in voice channels.
4. Start the bot. The application looks for a configuration file in the same
   directory called `.decbot`. Specify a different path as follows:

	```bash
	$ decbot --config /path/to/my/config
	```

5. To stop the bot, the application can be stopped from the command line, or
   the owner can issue `!dec quit` in the Discord server chat.

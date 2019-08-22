from asyncio import create_subprocess_shell, subprocess
import os

import decbot.config
from error import TTSError

async def convert(self, req, params = '[:phoneme on]'):
	""" Invoke the TTS executable.

	:param req: The Request to convert. This takes the text in the `input` file
	            and generates audio data stored in the `output` identifier.
	:type  req: Request
	:param params: The "pre" commands to send to DEC. By default, this enables
	               phonemes, to enable "singing" with pitch specifications.
	               Execute `wine say.exe -h` for more information.
	:type  params: str

	:raises TTSError: If the DEC command fails, this error is raised with the
	                  contents of stderr.
	"""
	path = config.get('tts.bin')
	# Change directory into the configured binary path since `say.exe`
	# depends on other files within (namely a dictionary and .dll), and will
	# not be able to find them when executed from another directory.
	command = 'cd {} && wine say.exe -pre "{}"'.format(path, params)

	# Apply the request-specific arguments and execute the command.
	command = '{} -w {} < {}'.format(command, req.output, req.input)
	proc    = await create_subprocess_shell(cmd, stderr = subprocess.PIPE)

	# Retrieve only stderr (second item in tuple) from `proc`.
	stderr = await proc.communicate()[1]
	if proc.returncode is not 0:
		raise TTSError('Error executing TTS: {}'.format(stderr.decode()))
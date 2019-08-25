from asyncio import create_subprocess_shell, subprocess
import os

import decbot.config as config
from .error import TTSError

def convert(req, params = '[:phoneme on]'):
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

	try:
		# Execute the command directly; using an async subprocess seemed
		# significantly slower in comparison.
		error = os.system(command)
	except OSError:
		# An exception means there was an error RUNNING the command, not an
		# error from the command/shell itself.
		raise TTSError('Could not invoke TTS command')

	if error:
		# A non-zero error code signifies an error with DEC.
		raise TTSError('TTS executable exited with code {}.'.format(error))

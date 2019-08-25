import contextlib
import os
from uuid import uuid4

import decbot.config as config
from .error import RequestError

class Request:
	""" A text-to-speech conversion request.

	Represent the input (the text data) and the output (the speech audio) of a
	TTS operation. Text input is written to a file to prevent command line
	injection, and audio data is created during a call to DEC. Both files are
	named after a random UUID to prevent collisions.
	"""
	def __init__(self, text):
		""" Create a new TTS request.

		The target directory for both the input and output files is specified
		through the configuration YAML; if `tmp` is not specified under `tts`,
		the system-wide temporary directory will be used instead.

		:param text: The input data (the words to by synthesized).
		:type  text: str

		:raises RequestError: The configuration-specified path may be invalid or
		                      inaccessible, raising an error.
		"""
		uid  = uuid4().hex
		path = config.get('tts.tmp', '/tmp')

		# Format the input/output filenames based on the config path and UUID.
		# The class controls the input file, and the output of DEC is a WAV.
		self.input  = '{}/{}.txt'.format(path, uid)
		self.output = '{}/{}.wav'.format(path, uid)

		try:
			# write the conversion request to a file.
			with open(self.input, 'w') as f:
				f.write(text)
		except OSError:
			raise RequestError('Could not write request text to file.')

	def cleanup(self):
		""" Remove the request information written to disk.

		Remove the input text and output sound from the filesystem. The
		configuration value 'archive' can be used to prevent this behavior; the
		files will exist until the user deletes them or the parent folder.
		"""
		if not config.get('tts.archive', False):
			# The file(s) may not exist if an exception occurred or the request
			# has not been fulfilled yet, so ignore these errors.
			with contextlib.suppress(FileNotFoundError):
				os.remove(self.input)
				os.remove(self.output)

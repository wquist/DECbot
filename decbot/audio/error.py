class MixerError(Exception):
	""" An audio mixer IO error.

	An error that occurs while loading audio data from disk.
	"""
	pass

class RequestError(Exception):
	""" A TTS request IO error.

	An error that occurs when writing a request to disk.
	"""
	pass

class TTSError(Exception):
	""" A TTS invocation error.

	An error that occurs when the external TTS command fails. This is raised
	when the DEC invocation returns an error code other than zero. Information
	written to stderr by DEC is usually included with this exception.
	"""
	pass

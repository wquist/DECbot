class AudioError(Exception):
	""" Any audio-related error.

	This is used as the base error type for all errors in the audio module.
	"""
	pass

class MixerError(AudioError):
	""" An audio mixer IO error.

	An error that occurs while loading audio data from disk.
	"""
	pass

class RequestError(AudioError):
	""" A TTS request IO error.

	An error that occurs when writing a request to disk.
	"""
	pass

class TTSError(AudioError):
	""" A TTS invocation error.

	An error that occurs when the external TTS command fails. This is raised
	when the DEC invocation returns an error code other than zero. Information
	written to stderr by DEC is usually included with this exception.
	"""
	pass

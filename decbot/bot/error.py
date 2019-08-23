class VoiceError(Exception):
	pass

class NoVoice(VoiceError):
	pass

class BadVoice(VoiceError):
	pass

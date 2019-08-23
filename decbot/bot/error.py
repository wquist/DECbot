class VoiceError(Exception):
	pass

class NoVoice(VoiceError):
	pass

class VoiceBusy(VoiceError):
	pass

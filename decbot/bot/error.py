class BotError(Exception):
	pass

class VoiceError(BotError):
	pass

class NoVoice(VoiceError):
	pass

class BadVoice(VoiceError):
	pass

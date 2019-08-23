import discord
from pydub import AudioSegment

from .error import MixerError

class Mixer(discord.AudioSource):
	""" A multi-channel mixed audio source.

	Allow multiple audio streams to be played as a single Discord AudioSource.
	Each enqueued audio segment will play overlayed for their duration. They do
	not have to match in length; the AudioSource will stay alive until the
	longest is finished playing.
	"""
	def __init__(self):
		""" Create a new mixed audio source.

		The object stores the remaining audio data for each segment, and returns
		it to Discord in 20ms slices.
		"""
		self.segments = []

	def enqueue(self, req):
		""" Mix new audio data into the active source.

		Requests can be added at any time; they will start playing in the middle
		of any currently active sources.

		:param req: The Request to load the audio `output` from.
		:type  req: Request

		:raises MixerError: An error is raised when the source audio cannot be
		                    loaded from disk.
		"""
		try:
			seg = AudioSegment.from_file(req.output).set_frame_rate(48000)
		except OSError:
			raise MixerError('Could not load audio file from request.')

		self.segments.append(seg)

	def read(self):
		""" Retrieve a 20ms slice of mixed audio.

		This method is overriden from `discord.AudioSource`. This slice is
		always clamped to 20ms regardless of how much is remaining in the
		segments; for segments less than 20ms, the slice is padded with silence.

		:returns: The next 20ms audio sample, of all segments overlayed.
		:rtype:   bytes
		"""
		# No more audio; signal to the source that the stream has ended.
		if not self.segments:
			return []

		# Specifying a starting 20ms segment will force all overlayed segments
		# to be clamped to 20ms as well.
		accum = AudioSegment.silent(duration = 20)
		for seg in self.segments:
			accum = accum.overlay(seg)

		# Cut off the first 20ms of each sample for the next read. If any
		# segments are less than or equal to 20ms, their last portion must have
		# just been played; filter them out.
		self.segments[:] = [seg[20:] for seg in self.segments if len(seg) > 20]
		# DEC returns mono data; convert this to stereo for Discord.
		return AudioSegment.from_mono_audiosegments(accum, accum).raw_data

	def cleanup(self):
		""" Reset/release state once the stream is finished.

		This method is overriden from `discord.AudioSource`. This is called
		after `read()` returns an empty slice, or when the stream is cancelled.
		Clear the segment state in case this source is to be used again.
		"""
		self.segments = []

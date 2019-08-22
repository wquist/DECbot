class ConfigError(Exception):
	""" A configuration IO/logic error.

	An error that occurs during loading or parsing the configuration file. Any
	errors that occur internally to the config namespace are caught and rethrown
	as configuration errors.
	"""
	pass

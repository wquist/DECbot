import yaml

from .error import ConfigError

_path   = '.decbot'
_values = None

def set_path(path):
	""" Specify where the configuration should be loaded from.

	:param path: A filesystem path pointing to a valid YAML document.
	:type  path: str

	:raises ConfigError: This method should only be called before `get()` is
	                     used (and a config file has been loaded.)
	"""
	if _values is not None:
		raise ConfigError('Configuration has already been loaded.')

	global _path
	_path = path

def get(name, default = None):
	""" Retrieve a configuration value.

	The configuration is lazy loaded (based on the path given to `set_path()`)
	if this is the first call to the method.

	:param name: The name of the configuration value. This may be a YAML node
	             with children, in which case a dictionary is returned, or a
	             hierarchy (with each level separated by a '.' - for example
	             'group.value'), which returns the single value.
	:type  name: str
	:param default: The value to return if a node is invalid or undefined. If
	                the value is `None`, an exception is raised instead.

	:return: The retrieved configuration value
	:raises ConfigError: If lazy loading occurs, an exception may be raised when
	                     the file is not found or has bad permissions. Else,
	                     an error will occur if the specified name is not found.
	"""
	global _values
	# `_values` is only None when the file has not been read yet.
	if _values is None:
		try:
			with open(_path) as f:
				# `safe_load()` prevents potential code execution.
				_values = yaml.safe_load(f)
		except yaml.YAMLError as e:
			try:
				pos  = e.problem_mark
				info = '{}:{}'.format(pos.line + 1, pos.column + 1)

				raise ConfigError('Parse error at {}.'.format(info))
			except AttributeError:
				raise ConfigError('Unknown parse error.')
		except IOError:
			raise ConfigError('Could not load configuration file.')

	value = _values
	# Descend the values dictionary for each name component.
	for node in name.split('.'):
		try:
			if node not in value:
				if default is None:
					raise ConfigError('Unknown node "{}".'.format(node))
				else:
					return default
		# A `TypeError` may occur if the specified name tries to go too deep
		# (for example, trying to check for a key in an integer).
		except TypeError:
			if default is None:
				raise ConfigError('Node "{}" does not have children.')
			else:
				return default

		value = value[node]

	return value

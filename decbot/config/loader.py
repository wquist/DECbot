import yaml
from error import ConfigError

_path   = '.decbot'
_values = None

def set_path(path):
	if _values is not None:
		raise ConfigError('Configuration has already been loaded.')

	global _path
	_path = path

def get(name):
	global _values
	if _values is None:
		try:
			with open(_path) as f:
				_values = yaml.safe_load(f)
		except yaml.YAMLError as e:
			raise ConfigError('Bad configuration format: {}'.format(e.message))
		except IOError:
			raise ConfigError('Could not load configuration file.')

	value = _values
	for node in name.split('.'):
		try:
			if node not in value:
				raise ConfigError('Unknown node "{}".'.format(node))
		except TypeError:
			raise ConfigError('Node "{}" does not have children.')

		value = value[node]

	return value

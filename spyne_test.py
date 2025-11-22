import spyne.util.six as s
print('module spyne.util.six loaded, attrs:', [a for a in dir(s) if not a.startswith('__')])
print('has moves?', hasattr(s, 'moves'))
import six
print('six.moves present?', hasattr(six, 'moves'))

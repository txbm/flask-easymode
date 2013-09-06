from simplejson import dumps
from blinker import Namespace
from datetime import datetime

crud_signals = Namespace()

object_created = crud_signals.signal('object_created')
object_read = crud_signals.signal('object_read')
object_updated = crud_signals.signal('object_updated')
object_deleted = crud_signals.signal('object_deleted')

class Create(object):

	@classmethod
	def create(cls, **kwargs):
		o = cls()
		object_created.send(o, **kwargs)
		return o

class Read(object):

	_readable = ()

	@classmethod
	def read(cls, **kwargs):
		r = object_read.send(cls, **kwargs)
		return r[0][1]

	@classmethod
	def read_many(cls, **kwargs):
		r = object_read.send(cls, _many=True, **kwargs)
		return r[0][1]

	@property
	def as_dict(self):
		d = {}
		for attr in self._readable:
			parts = attr.split('.')
			value = getattr(self, parts[0])
			for part in parts[1:]:
				if value is None:
					continue
				value = getattr(value, part)

			# TODO: think about adding some flexibility to the type handling 
			if type(value) is datetime:
				value = str(value)

			d[attr.replace('.', '_')] = value
		return d

	@property
	def as_json(self):
		return dumps(self.as_dict)

class Update(object):

	_updateable = ()

	def update(self, **kwargs):
		filtered = dict([(k, v) for k, v in kwargs.iteritems() if k in self._updateable])
		[setattr(self, k, v) for k, v in filtered.iteritems()]
		return object_updated.send(self, **filtered)[0][1]

class Delete(object):

	def delete(self):
		object_deleted.send(self)

class CRUD(Create, Read, Update, Delete): pass
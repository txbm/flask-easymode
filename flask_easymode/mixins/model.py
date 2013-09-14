# -*- coding: utf-8 -*-

from simplejson import dumps
from blinker import Namespace
from datetime import datetime

easy_signals = Namespace()

object_created = easy_signals.signal('object_created')
object_read = easy_signals.signal('object_read')
object_updated = easy_signals.signal('object_updated')
object_deleted = easy_signals.signal('object_deleted')
object_injected = easy_signals.signal('object_injected')

class Create(object):

	@classmethod
	def create(cls, **kwargs):
		o = cls()
		object_created.send(cls, o=o, **kwargs)
		return o

class Read(object):

	@classmethod
	def read(cls, **kwargs):
		r = object_read.send(cls, **kwargs)
		try:
			return r[0][1]
		except IndexError: pass

	@classmethod
	def read_many(cls, **kwargs):
		r = object_read.send(cls, _many=True, **kwargs)
		try:
			return r[0][1]
		except IndexError: pass

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
			
			value = unicode(value)
		
			d[attr.replace('.', '_')] = value
		return d

	@property
	def as_json(self):
		return dumps(self.as_dict)

class Update(object):

	@classmethod
	def update(cls, o, **kwargs):
		r = object_updated.send(cls, o=o, **kwargs)
		try:
			return r[0][1]
		except IndexError: pass

class Delete(object):

	def delete(self):
		object_deleted.send(self)

class CRUD(Create, Read, Update, Delete): pass

class Injectable(object):

	@classmethod
	def load(cls, conditions, **kwargs):
		r = object_injected.send(cls, conditions=conditions, **kwargs)
		try:
			return r[0][1]
		except IndexError: pass

class CRUDI(CRUD, Injectable): pass
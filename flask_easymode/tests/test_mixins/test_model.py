from nose.tools.trivial import assert_equals, assert_true, assert_is_instance, assert_in

from ...mixins.model import CRUD, object_created, object_read, object_updated, \
	object_deleted


class CRUDMan(CRUD):

	_readable = ('name', 'catch_phrase')
	_updateable = ('name')


	def __init__(self):
		self.name = 'CRUD Man'
		self.catch_phrase = 'I am CRUD Man. Fear my power.'

def test_create():

	@object_created.connect
	def create_fxn(cls, o, **kwargs):
		o.touched_by_signal = True

	o = CRUDMan.create()

	assert_true(o.touched_by_signal)
	assert_is_instance(o, CRUDMan)

def test_read():

	@object_read.connect
	def reading_fxn(cls, **kwargs):
		assert_equals(cls, CRUDMan)
		assert_in('name', kwargs.keys())

		if kwargs.get('_many'):
			return 'Many things'
		return 'Something'

	r = CRUDMan.read(name='CRUD Man')
	assert_equals(r, 'Something')

	r = CRUDMan.read_many(name='CRUD Man')
	assert_equals(r, 'Many things')

	o = CRUDMan.create()
	o.as_dict
	o.as_json

def test_update():

	data_dict = {'name': 'CRUD Woman', 'catch_phrase': 'Cant change this'}

	@object_updated.connect
	def updating_fxn(cls, o, **kwargs):
		assert_equals(o.name, 'CRUD Man')
		assert_equals(o.catch_phrase, 'I am CRUD Man. Fear my power.')
		return o.as_dict

	o = CRUDMan.create()

	r = CRUDMan.update(o, **data_dict)
	assert_equals(r, {'name': 'CRUD Man', 'catch_phrase': 'I am CRUD Man. Fear my power.'})

def test_delete():

	o = CRUDMan.create()
	o.name = 'Dying CRUD Man'

	@object_deleted.connect
	def delete_fxn(o, **kwargs):
		assert_equals(o.name, 'Dying CRUD Man')

	o.delete()
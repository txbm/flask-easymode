from nose.tools.nontrivial import with_setup
from nose.tools.trivial import assert_equals, assert_in

from simplejson import loads

from . import app_setup, em, app

@with_setup(app_setup)
def test_xhr_api():
	with app.app_context():
		em.enable_xhr()

		with app.test_client() as c:
			r = c.get('/')
			assert_in('I am the index page', r.data)

			r = c.get('/xhr', headers=[('X-Requested-With', 'XMLHttpRequest')])

			py_data = loads(r.data)
			assert_in('data', py_data.keys())
			assert_in('messages', py_data.keys())

			assert_equals(len(py_data['data']), 2)
			assert_equals(len(py_data['messages']), 5)

			r = c.get('/xhr-failure')
			py_data = loads(r.data)
			assert_in('error', py_data.keys())

			r = c.get('/xhr-failure', headers=[('X-Requested-With', 'XMLHttpRequest')])
			py_data = loads(r.data)
			assert_in('error', py_data.keys())

			r = c.get('/xhr-failure-with-code', headers=[('X-Requested-With', 'XMLHttpRequest')])
			assert_equals(r.status_code, 500)
			py_data = loads(r.data)
			assert_in('error', py_data.keys())
			assert_in('code', py_data.keys())
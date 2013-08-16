from nose.tools.nontrivial import with_setup
from nose.tools.trivial import assert_equals, assert_in

from . import app_setup, em, app

@with_setup(app_setup)
def test_xhr_api():
	with app.app_context():
		em.enable_xhr()

		with app.test_client() as c:
			r = c.get('/')
			assert_in('I am the index page', r.data)

			r = c.get('/xhr', headers=[('X-Requested-With', 'XMLHttpRequest')])
			print r.data
# -*- coding: utf-8 -*-

from nose.tools.trivial import (
    assert_equals, assert_in, assert_raises)

from simplejson import loads

from flask_easymode import EasyMode
from flask_easymode.tests import (
    create_app, InjectableClass, NonInjectableClass)


def _setup():
    app = create_app()
    em = EasyMode()
    em.init_app(app)
    return (em, app)


def test_xhr_api():
    em, app = _setup()
    em.enable_xhr(app)

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

        r = c.get('/xhr-failure', headers=[
                  ('X-Requested-With', 'XMLHttpRequest')])
        py_data = loads(r.data)
        assert_in('error', py_data.keys())

        r = c.get('/xhr-failure-with-code', headers=[
                  ('X-Requested-With', 'XMLHttpRequest')])
        assert_equals(r.status_code, 500)
        py_data = loads(r.data)
        assert_in('error', py_data.keys())
        assert_in('code', py_data.keys())

        r = c.get('/xhr-that-allows-regular-http')
        py_data = loads(r.data)
        assert_in('test', py_data['data'].keys())
        assert_in('A message in a bottle.', py_data['messages'][0])


def test_xhr_api_off():
    em, app = _setup()

    with app.test_client() as c:
        r = c.get('/')
        assert_in('I am the index page.', r.data)

        r = c.get('/xhr')
        assert_in('403', r.data)

        r = c.get('/xhr', headers=[('X-Requested-With', 'XMLHttpRequest')])
        assert_in('403', r.data)

        r = c.get('/xhr-that-returns-something')
        assert_in('some string', r.data)


def test_inject():
    em, app = _setup()
    em.enable_xhr(app)
    em.enable_injection(app)
    em.add_injectable(InjectableClass)

    with app.test_client() as c:
        r = c.get('/inject/joe-slug')
        assert_in('joe-slug', r.data)

        r = c.get('/inject-as-arg/joe-slug')
        assert_in('joe-slug', r.data)

        with assert_raises(RuntimeError):
            r = c.get('/inject-non-injectable/here-comes-an-error')

        em.add_injectable(NonInjectableClass)

        with assert_raises(RuntimeError):
            r = c.get('/inject-non-injectable/still-going-to-fail')

        with assert_raises(AttributeError):
            r = c.get('/inject-skip-by-default')

        r = c.get('/inject-list-denoting/apples')
        assert_equals(r.status_code, 200)


def test_inject_off():
    em, app = _setup()

    with app.test_client() as c:
        with assert_raises(Exception):
            r = c.get('/inject/only-bad-can-come-of-this')

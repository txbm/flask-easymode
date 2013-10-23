# -*- coding: utf-8 -*-


from flask import Flask, flash, g

from flask_easymode.decorators import xhr_api, inject
from flask_easymode.exceptions import XHRError
from flask_easymode.mixins.model import CRUD, CRUDI, object_injected


def create_app():
    app = Flask('easymode')

    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = '123454fdsafdsfdsfdsfds'

    @app.route('/')
    def index():
        return 'I am the index page.'

    @app.route('/xhr')
    @xhr_api()
    def xhr_endpoint():
        try:
            g.xhr.data['test'] = 'monkey'
            g.xhr.data['walrus'] = 'punch'
        except AttributeError:
            pass

        flash('This is a test message.')
        flash('This is a warning.', 'warning')
        flash('This is an error', 'error')
        flash('This is just some info', 'info')
        flash('This is another warning', 'warning')

    @app.route('/xhr-failure')
    @xhr_api()
    def xhr_failure():
        try:
            g.xhr.data['test'] = 'monkey'
        except AttributeError:
            pass

        raise XHRError('Disaster everywhere.')

    @app.route('/xhr-failure-with-code')
    @xhr_api()
    def xhr_failure_with_code():
        try:
            g.xhr.data['test'] = 'monkey'
        except AttributeError:
            pass

        raise XHRError('Disaster befalls the city', status_code=500)

    @app.route('/xhr-that-returns-something')
    @xhr_api()
    def xhr_that_returns_something():
        try:
            g.xhr.data['test'] = 'monkey'
        except AttributeError:
            pass

        return 'Here is some string that would never be returned if the XHR API were active.'

    @app.route('/xhr-that-allows-regular-http')
    @xhr_api(allow_http=True)
    def xhr_that_allows_regular_http():
        try:
            g.xhr.data['test'] = 'monkey'
        except AttributeError:
            pass

        flash('A message in a bottle.')

        return 'Here is some regular return stuff'

    @app.route('/inject/<injectable_class_slug_name>')
    @inject('injectable_class')
    def inject_test_class_slug_name():
        return 'I have been injected with %s' % g.injectable_class.slug_name

    @app.route('/inject-as-arg/<injectable_class_slug_name>')
    @inject('injectable_class', as_args=True)
    def inject_test_class_args(injectable_class):
        return 'I have been injected with %s' % injectable_class.slug_name

    @app.route('/inject-non-injectable/<non_injectable_class_slug_name>')
    @inject('non_injectable_class')
    def inject_the_noninjectable():
        return 'This will never happen because there will be an exception :('

    @app.route('/inject-skip-by-default', defaults={'injectable_class_slug_name': None})
    @app.route('/inject-skip-by-default/<injectable_class_slug_name>')
    @inject('injectable_class', as_args=True)
    def inject_skip_by_default(injectable_class):
        return injectable_class.slug_name

    @app.route('/inject-list-denoting/<injectable_class_category_name>')
    @inject('injectable_class', default='skip', lists='denote', as_args=True)
    def inject_list_denoting(injectable_class_list):
        return str(injectable_class_list)

    return app


class InjectableClass(CRUDI):

    def __init__(self):
        self.slug_name = 'joe-slug'
        self.category_name = 'apples'


class NonInjectableClass(CRUD):
    pass


@object_injected.connect_via(InjectableClass)
def injectable_injected(cls, conditions, **kwargs):
    for c in conditions:
        k, v = c
        if k == 'slug_name' and v == 'joe-slug':
            return InjectableClass()

        if k == 'category_name' and v == 'apples':
            return [InjectableClass(), InjectableClass(), InjectableClass()]

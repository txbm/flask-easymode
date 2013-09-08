from collections import namedtuple
from functools import partial

from flask import current_app, request, g, abort

from .exceptions import XHRError, handle_xhr_error

class EasyMode(object):

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		self.app = app
		self.app.config['XHR_API_ENABLED'] = False
		self.app.config['XHR_API_ALLOW_HTTP'] = False
		self.app.config['VIEW_DI_ENABLED'] = False

	# as dirty as this looks, it's the best way to do it without using the decorator
	# because there is no built in function in flask yet to do it.
	def enable_xhr(self):
		self.app.config['XHR_API_ENABLED'] = True
		self.app.error_handler_spec.setdefault(None, {}).setdefault(None, []) \
		.append((XHRError, handle_xhr_error))

	def enable_injection(self):
		self.app.config['VIEW_DI_ENABLED'] = True
		self._injectables = {}
		self._setup_injectable_preprocessor()

	def add_injectable(self, cls):
		self._injectables[cls.__name__.lower()] = cls

	def _setup_injectable_preprocessor(self):
		app = self.app
		
		@app.url_value_preprocessor
		def detect_injectables(endpoint, values):
			g._injections = {}

			def _extract_injections(values):
				injections = {}
				possibles = [k.split('_', 1) + [k, v] for k, v in values.iteritems()]
				
				for p in possibles:
					cls_name, prop_name, param, value = p
					try:
						cls = self._injectables[cls_name]
					except KeyError:
						continue
					injections.setdefault(cls_name, {'class': cls, 'params': [], 'conditions': []})
					injections[cls_name]['params'].append(param)
					injections[cls_name]['conditions'].append((prop_name, value))

				return injections

			g._injections = dict(_extract_injections(values).items() + _extract_injections(request.form.to_dict()).items())
import re

from flask import current_app, request, g, abort

from .exceptions import XHRError, handle_xhr_error

class EasyMode(object):

	_injectables = {}

	def __init__(self, app=None):
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		app.config['XHR_API_ENABLED'] = False
		app.config['XHR_API_ALLOW_HTTP'] = False
		app.config['VIEW_DI_ENABLED'] = False

	# as dirty as this looks, it's the best way to do it without using the decorator
	# because there is no built in function in flask yet to do it.
	def enable_xhr(self, app):
		app.config['XHR_API_ENABLED'] = True
		app.error_handler_spec.setdefault(None, {}).setdefault(None, []) \
		.append((XHRError, handle_xhr_error))

	def enable_injection(self, app):
		app.config['VIEW_DI_ENABLED'] = True
		
	def add_injectable(self, cls, alt=None):
		cls_name = alt or cls.__name__
		cls_name = re.sub(r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', r"_\g<0>", cls_name).lower()
		EasyMode._injectables[cls_name] = cls
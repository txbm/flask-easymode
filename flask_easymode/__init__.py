from flask import current_app

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

	# as dirty as this looks, it's the best way to do it without using the decorator
	# because there is no built in function in flask yet to do it.
	def enable_xhr(self):
		self.app.config['XHR_API_ENABLED'] = True
		self.app.error_handler_spec.setdefault(None, {}).setdefault(None, []) \
		.append((XHRError, handle_xhr_error))

	def disable_xhr(self):
		self.app.config['XHR_API_ENABLED'] = False
		t = (XHRError, handle_xhr_error)
		self.app.error_handler_spec[None][None].remove(t)
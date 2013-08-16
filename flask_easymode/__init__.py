from flask import current_app
from flask.json import JSONEncoder

from .exceptions import XHRError, handle_xhr_error

class EasyMode(object):

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		self.app = app
		self.app.config['XHR_API_ENABLED'] = False

	# as dirty as this looks, it's the best way to do it without using the decorator
	# because there is no built in function in flask yet to do it.
	def enable_xhr(self):
		self.app.config['XHR_API_ENABLED'] = True
		self.app.json_encoder = CustomJSONEncoder
		self.app.error_handler_spec.setdefault(None, {}).setdefault(None, []) \
		.append((XHRError, handle_xhr_error))

	def disable_xhr(self):
		self.app.config['XHR_API_ENABLED'] = False
		self.app.json_encoder = JSONEncoder
		t = (XHRError, handle_xhr_error)
		self.app.error_handler_spec[None][None].remove(t)


class CustomJSONEncoder(JSONEncoder):

	def __init__(self, *args, **kwargs):
		kwargs['namedtuple_as_object'] = True
		super(CustomJSONEncoder, self).__init__(*args, **kwargs)
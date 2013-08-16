from flask import current_app, redirect, request, flash, url_for, g, \
	abort, get_flashed_messages, jsonify

from functools import wraps
from collections import namedtuple

from .exceptions import XHRError

xhr = namedtuple('xhr', ('data', 'messages'))

def xhr_api():
	def _decorator(f):
		@wraps(f)
		def _wrapper(*args, **kwargs):
			if not current_app.config.get('XHR_API_ENABLED'):
				return f(*args, **kwargs)
			if not request.is_xhr:
				raise XHRError('XHR endpoints may not be called directly.', status_code=500)

			g.xhr = xhr({}, [])
			f(*args, **kwargs)
			g.xhr.messages.extend(get_flashed_messages(with_categories=True))
			return jsonify(g.xhr)
		return _wrapper
	return _decorator




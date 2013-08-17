from flask import current_app, redirect, request, flash, url_for, g, \
	abort, get_flashed_messages, jsonify

from functools import wraps
from collections import namedtuple

from .exceptions import XHRError

xhr = namedtuple('xhr', ('data', 'messages'))

def xhr_api(allow_http=None):
	def _decorator(f):
		@wraps(f)
		def _wrapper(*args, **kwargs):
			if not current_app.config.get('XHR_API_ENABLED'):
				view_result = f(*args, **kwargs)
				if not view_result:
					abort(403)
				return view_result
			
			a = allow_http
			if a is None:
				a = current_app.config.get('XHR_API_ALLOW_HTTP')

			if not request.is_xhr and not a:
				raise XHRError('XHR endpoints must be called asynchronously.', status_code=500)

			g.xhr = xhr({}, [])
			f(*args, **kwargs)
			g.xhr.messages.extend(get_flashed_messages(with_categories=True))
			return jsonify(data=g.xhr.data, messages=g.xhr.messages)
		return _wrapper
	return _decorator




from flask import current_app, redirect, request, flash, url_for, g, \
	abort, get_flashed_messages, jsonify, _app_ctx_stack

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


def inject(*classes, **options):
	def _decorator(f):
		@wraps(f)
		def _wrapper(*args, **kwargs):
			classes_by_len = sorted(classes, key=len) # most to least specific to eliminate ambiguity when dealing with nested prefix class names
			classes_by_len.reverse()
			ctx = _app_ctx_stack.top

			def _extract_injections(kvps):
				injections = {}
				for k, v in kvps.iteritems():
					for cls_name in classes_by_len:
						r = k.replace(cls_name, '')
						if r != k:
							prop_name = r[1:]
							try:
								cls = ctx._injectables[cls_name]
							except KeyError:
								raise RuntimeError('You must add %s as an injectable before it can injected! Use EasyMode.add_injectable(cls).')
							
							injections.setdefault(cls_name, {'class': cls, 'params': [], 'conditions': []})
							injections[cls_name]['params'].append(k)
							injections[cls_name]['conditions'].append((prop_name, v))
				return injections

			injections = dict(_extract_injections(kwargs).items() + _extract_injections(request.form.to_dict()).items())

			for cls_name, i in injections.iteritems():
				if cls_name in classes:
					try:
						o = i['class'].load(i['conditions'])
					except AttributeError:
						raise RuntimeError('To use %s with dependency injection, the class must either define a load(cls, conditions, **kwargs) interface or just inherit from the provided mixin.' % i.cls.__name__)
					
					if options.get('as_args'):
						kwargs[cls_name] = o
					else:
						setattr(g, cls_name, o)
	
					[kwargs.pop(p, None) for p in i['params']]

			return f(*args, **kwargs)
		return _wrapper
	return _decorator
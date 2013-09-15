# -*- coding: utf-8 -*-

from flask import current_app, redirect, request, flash, url_for, g, \
	abort, get_flashed_messages, jsonify

from functools import wraps
from collections import namedtuple

from . import EasyMode
from .exceptions import XHRError

xhr = namedtuple('xhr', ('data', 'messages', 'html'))

class XHR(object):

	def __init__(self):
		self.html = ''
		self.data = {}
		self.messages = []

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

			g.xhr = XHR()
			f(*args, **kwargs)
			g.xhr.messages.extend(get_flashed_messages(with_categories=True))
			return jsonify(data=g.xhr.data, messages=g.xhr.messages, html=g.xhr.html)
		return _wrapper
	return _decorator


def inject(*classes, **options):
	def _decorator(f):
		@wraps(f)
		def _wrapper(*args, **kwargs):
			if not current_app.config.get('VIEW_DI_ENABLED'):
				return f(*args, **kwargs)
			
			# most to least specific to eliminate ambiguity when dealing with nested prefix class names
			classes_by_len = sorted(classes, key=len)
			classes_by_len.reverse()

			injections = {}

			def _param_to_cls_prop_pair(param):
				for cls_name in classes_by_len:
					r = param.replace(cls_name, '')
					if r != param:
						return (cls_name, r[1:])

			def _extract_injections(kvps):
				for k, v in kvps.iteritems():
					try:
						cls_name, prop_name = _param_to_cls_prop_pair(k)
					except TypeError:
						continue
					
					injections[cls_name]['params'].append(k)
					injections[cls_name]['conditions'].append((prop_name, v))

			for cls_name in classes:
				try:
					cls = EasyMode._injectables[cls_name]
				except KeyError:
					raise RuntimeError('Class "%s" has not been added as injectable. Use EasyMode.add_injectable(cls_name).' % cls_name)

				injections.setdefault(cls_name, {'class': cls, 'params': [], 'conditions': []})
			
			_extract_injections(kwargs)
			_extract_injections(request.form.to_dict())
			json = request.get_json(silent=True) or {}
			_extract_injections(json)

			for cls_name, i in injections.iteritems():
				if cls_name in classes:
					try:
						o = i['class'].load(i['conditions'])
					except AttributeError:
						raise RuntimeError('To use %s with dependency injection, the class must either define a load(cls, conditions, **kwargs) interface or just inherit from the provided mixin.' % i['class'].__name__)
					
					if options.get('as_args'):
						kwargs[cls_name] = o
					else:
						setattr(g, cls_name, o)
	
					[kwargs.pop(p, None) for p in i['params']]

			return f(*args, **kwargs)
		return _wrapper
	return _decorator
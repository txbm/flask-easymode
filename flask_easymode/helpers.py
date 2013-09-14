# -*- coding: utf-8 -*-

from flask import request, redirect, url_for

def redirect_to_self(clear=False):
	if clear:
		return redirect(url_for(request.endpoint))
	return redirect(url_for(request.endpoint, **request.view_args))

redirect_self = redirect_to_self

def redirect_to_next(clear=True, key='next'):
	if key in request.args:
		if clear:
			return redirect(request.args.get('next'))
		else:
			next = request.args.pop('next')
			return redirect(next, **request.view_args)

redirect_next = redirect_to_next
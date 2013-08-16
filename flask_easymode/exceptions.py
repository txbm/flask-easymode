from flask import flash, jsonify

def handle_xhr_error(error):
	response = jsonify(error=error.message, code=error.status_code)
	response.status_code = error.status_code
	return response

class XHRError(Exception):
	status_code = 500

	def __init__(self, message, status_code=None):
		super(XHRError, self).__init__()
		self.message = message
		if status_code is not None:
			self.status_code = status_code
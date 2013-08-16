from flask import Flask, flash, g

from .. import EasyMode
from ..decorators import xhr_api
from ..exceptions import XHRError

em = EasyMode()

def create_app():
	app = Flask('easymode')

	@app.route('/')
	def index():
		return 'I am the index page.'

	@app.route('/xhr')
	@xhr_api()
	def xhr_endpoint():
		g.xhr.data['test'] = 'monkey'
		g.xhr.data['walrus'] = 'punch'

		flash('This is a test message.')
		flash('This is a warning.', 'warning')
		flash('This is an error', 'error')
		flash('This is just some info', 'info')
		flash('This is another warning', 'warning')

	@app.route('/xhr-failure')
	@xhr_api()
	def xhr_failure():
		g.xhr.data['test'] = 'monkey'
		raise XHRError('Disaster everywhere.')

	@app.route('/xhr-failure-with-code')
	@xhr_api()
	def xhr_failure_with_code():
		g.xhr.data['test'] = 'monkey'
		raise XHRError('Disaster befalls the city', status_code=500)

	return app

app = create_app()
app.config['TESTING'] = True
app.config['SECRET_KEY'] = '123454fdsafdsfdsfdsfds'

def app_setup():
	em.init_app(app)
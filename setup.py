"""
Flask EasyMode
-----------------

This extension is a modular extension (meaning you can turn features on and off) designed
to provide modules of useful helpers, decorators, and mixins to make your Flask web app
development experience even easier than it already is thanks to Flask's good design.

The purpose of this extension is not to turn Flask's modular nature into something monolithic.

Every feature of this extension can be enabled or disabled at will and most features are disabled
by default.

Initializing this extension does very little other than associate the application.
	
"""

from setuptools import setup, find_packages

setup(
	name='Flask-EasyMode',
	version='0.1',
	url='http://github.com/petermelias/flask-easymode',
	license='BSD',
	author='Peter M. Elias',
	author_email='petermelias@gmail.com',
	description='Make Flask development even easier',
	long_description=__doc__,
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	platforms='any',
	install_requires=[
		'Flask',
		'Werkzeug',
		'blinker',
		'simplejson'
	],
	classifiers=[
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
)
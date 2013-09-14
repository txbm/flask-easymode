from setuptools import setup, find_packages

setup(
	name='flask-easymode',
	version='0.0.4',
	url='http://github.com/petermelias/flask-easymode',
	license='BSD',
	author='Peter M. Elias',
	author_email='petermelias@gmail.com',
	description='Make Flask development even easier',
	long_description=open('README.md').read(),
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
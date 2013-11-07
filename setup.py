from setuptools import setup, find_packages

setup(
    name='flask-easymode',
    version='0.0.17',
    url='http://github.com/petermelias/flask-easymode',
    license='MIT',
    author='Peter M. Elias',
    author_email='petermelias@gmail.com',
    description='Make Flask development even easier',
    long_description=open('README.md').read(),
    packages=find_packages(),
    platforms='any',
    install_requires=[
            'Flask',
            'Werkzeug',
            'blinker',
            'simplejson',
            'mrpython'
    ],
    extras_require={
        'test': [
            'nose',
            'coveralls'
        ]
    },
    test_suite='nose.collector',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

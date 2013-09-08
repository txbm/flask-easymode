# Flask EasyMode

## Motivation


This package was mainly created to consolidate and provide an API for common 
patterns that come up when using Flask for standard web applications.

Primarily it focuses on web API patterns, and view <--> model data handling 
patterns that generally do not change very often and can be very repetitive
at times.

## Design

This extension uses Blinker heavily to provide abstract plug points and assume
nothing about the application of any of the features provided by the API.
Generally speaking, you are expected to register Blinker recipient functions
in order to define your application specific behavior.

I highly recommend using ```@signal.connect``` and ```@signal.connect_via```
to register generic and increasingly specific handlers. This has the pleasant
effect of being efficient, lightweight, and decoupled.

I have made an effort to modularize and break up the various features so that
this package still follows the "opt-in" philosophy of Flask and its extensions.

For this reason, ```init_app()``` does almost nothing until you start enabling specific
features which will start touching config variables and the application context stack.

Much of the functionality is contained within mixins, helpers, and decorators which
must be imported after a feature has been enabled. Obviously there are certain
components that are usable directly and are not tied to a specific feature.

For example, the some of the mixins provided are mainly to assist with common
model class operations that come up on almost every project. These mixins
can just be plainly imported and used separately from even Flask itself.

That said, do not try and use decorators and/or helpers that depend on 
optionally-enabled features until you have enabled them. In some cases 
they will simply ignore you, in other cases they will throw errors.


## Features

* View Function Dependency-Injection of Models (by far the coolest feature)
* Fully Automatic XHR API Mode (error handling, data serialization, and more)
* Totally Abstract CRUD Mixins (examples using SQLAlchemy in Wiki)
* Useful View Helper functions such as ```redirect_self()``` and ```redirect_next()```

## Examples

### View Function DI

This example uses SQLAlchemy to look up our hypothetical user. Understand that the point
of using Signals here is that you can attach any lookup system you want. Totally abstract.

```python

# setup app
em = EasyMode()
em.init_app(app)
with app.app_context():
	em.enable_injection()
	em.add_injectable(User) # DO NOT FORGET TO DO THIS
	# Sadly, EasyMode cannot magically know where you like to keep your injectable models

# inherit user from Injectable mixin
class User(object, Injectable):
	
	def __init__(self, name):
		self.name = name

# subscribe database lookup to injection signal
@object_injected.connect_via(User)
def lookup_user(cls, conditions, **kwargs)
	query = session.query(cls)
	for attr, value in conditions:
		query.filter(attr==value)
	return query.first()
	# or redis
	# or cassandra
	# or a floppy disk


# setup routes
@app.route('/user/edit/<user_name>')
@inject('user')
def user_edit():
	return g.user.name # user is automagically assigned to g object (unless you turn that off)

# make a request
with app.test_client() as c:
	print c.get('/user/edit/petermelias') # petermelias
```

Super cool. Imagine all the code you can delete now because you don't have to lookup models
from your ```view_args```.

For anybody who is wondering, ```request.form``` is also checked for dependencies, so you can post params
as well and they will get picked up and injected right alongside url params. Merge behavior of course.

If you don't like the auto-g-assignment, do this instead:

```python
@app.route('/user/edit/<user_name>')
@inject('user', as_args=True)
def user_edit(user):
	return user.name # injects as parameter instead of global, sexy I know.
```

Just when you thought it was over... you can specify unlimited conditions.

```python
@app.route('/users/list/<user_name>/<user_age>/<user_eye_color>')
@inject('user')
def users_list():
	print users # [User, User, User] all matching the parameters if your lookup function works

```

You can use arbitrarily long class names, the only rule is that the route params must be separated
by underscores between every word.

```python
class PharoahOfEgypt(object, Injectable): pass

@app.route('/pharoah/worship/<pharoah_of_egypt_name>')
@inject('pharoah_of_egypt')
def worship_pharoah():
	p = g.pharoah_of_egypt
```

### Full Auto XHR

This is really useful when you're communicating with a JavaScript frontend.

```python
# app
em = EasyMode()
em.init_app(app)
with app.app_context():
	em.enable_xhr()

@app.route('/some-xhr-endpoint')
@xhr_api()
def xhr_endpoint():
	g.xhr.data['some-data'] = 'that I want to send to the client'

	flash('A super important message')
	flash('A huge problem', 'error')

	# you're not blind, there is no return statement necessary in this mode

with app.app_context() as c:
	r = c.get('/some-xhr-endpoint', headers=[('X-Requested-With', 'XMLHttpRequest')])
	print r.data

	'''
	{
		"data": {
			"some-data": "that I want to send to the client"
		},
		"messages": [
			["message", "A super important messsage"],
			["error", "A huge problem"]
		]
	}
	'''
```

There are many options and behavior notes for the XHR API but they are for specific
use cases that will be documented in the Wiki.

### Abstract CRUD Interface

Mixins and signals for attaching CRUD handlers. Also includes the Injectable mixin
and a bundled one if you want the super bonus 5-pack. See the CRUDI mixin.

```python

class User(CRUD):

	_updateable = ('name', 'age', 'gender') # define this for auto-update feature
	_readable = ('id', 'name', 'age', 'gender') # define this for auto-serialization feature

# or if you want Injectable too
# class User(CRUDI): pass

# generic handling function for ALL models
@object_created.connect
def model_created(cls, o, **kwargs):
	data = kwargs.get('data')
	if data:
		o.update(**data) # update function comes from CRUD

# user specific handling function
@object_created.connect_via(User)
def user_created(cls, user, **kwargs):
	user.initialize_account()
	user.send_welcome_email()
	facebook.report_signup_to_nsa(user)

# generic model reading function using SQLAlchemy
@object_read.connect
def read_model(model, _many=False, **kwargs):
	r = None
	query = session.query(model)
	filters = kwargs.get('f')

	[query.filter(f) for f in filters if filters]

	if _many:
		r = query.all()
	else:
		r = query.first()
	return r

@object_deleted.connect
def delete_object(o, **kwargs):
	session.delete(o) # owned

# and in our view...

@app.route('/user/lookup/<user_name>')
@inject('user', as_args=True)
def lookup_user(user):
	user.update(**request.form.to_dict()) # because who needs validation anyway?
	user.delete() # or this user for that matter (comes from CRUD)

	some_other_user = User.read(filters=[User.name=='Mike', User.age>=12]) # read comes from CRUD
	user_list = User.read_many(filters=[User.age>=21]) # as does read_many (shortcuts _many=True)
 
	return jsonify(**some_other_user.as_dict) # as_dict and as_json come from CRUD

```

As you can see this is both a fun, concise and robust way to set up data handling since it requires
the bare minimum amount of code to build an efficient framework for loading and modifying data.

In otherwords, no ActiveRecord bullshit here.

Also, keep in mind that ALL signalling uses ```**kwargs.``` You can make your handlers as simple and/or
as complex as needed. This library tries to assume the minimum level of convenience for the
consumer and uses private kwarg keys internally to avoid polluting your public API-space.

Fork, extend, merge, repeat!

## Tests

```nosetests```

## License
MIT
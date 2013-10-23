## Changelog
current version: v0.0.12

### v0.0.12
* Added the ``` lists='denote' ``` option to the ``` @inject ``` decorator. This default setting appends the class name of an injected result with the suffix '_list' to make it clear that a collection result is expected.

### v0.0.11
* Removed the ``` as_dict ``` and ``` as_json ``` interfaces from the ``` Read ``` model. Decided that was an overeach of responsibility for this extension. Recommend implementing in application space using something like ``` jsonpickle ``` library to create application-specific mixins for this behavior. Much cleaner, and more appropriately scoped.
* BREAKING: ``` delete ``` method on the ``` Delete ``` model is now a class method to match the others. The original motivation for making it an instance method was convenience. I have since decided that was a silly motivation and that for maximum ease of extensibility, class method (like the others) is the way to go. Consistency is also something I always want to maintain across my APIs and that was a factor in this decision. Old way: ``` obj.delete() ``` new way ``` ObjClass.delete(obj) ```
* You can now specify the sources you want to read from for injection ['json', 'params', 'form', 'query_string'] Use like this: ``` em.enable_injection(app, scan=('json', 'form')) ``` This would ignore the query string and the url parameters and only check POST and JSON data.
* Re-worked the internal configuration management model. Was driving me a little nuts. Do not read or write extension config variables on the ``` Flask.config ``` object. They are prefixed and one-way written from the extension. Use the ``` EasyMode.enable*() ``` functions to do stuff, the configuration values are really only for internal use by the extension.

### v0.0.10
* random fixes

### v0.0.9
* random fixes

### v0.0.8

* App context no longer used, pass application reference directly to enable*() functions.
* request.get_json() parsed for injection parameters.
* Alternate class names can be specified when adding new classes to the injector (this can happen as many times as you want)
* The Update Mixin has been modified to use a classmethod like the others and now operates on the instance as an argument.
  this changes the API from ```o.update(**data) ``` to ```ClassName.update(o, **data) ```. The reasoning behind this was to
  ensure that the consuming signal functions would have the same degree of flexibility in decision making as the other hook
  points for the CRUD system.
* Removed the default implementations for hook points like update(). It is not mission of the this library to make assumptions
  at that level. Even the default as_dict() implementation may be turned into a signal in later versions, and I may separate
  out the default impls into a module that can be activated or overridden at will. I would do this to provide the OOB experience
  for people in a hurry and also to allow for maximum choice for those looking to customize.
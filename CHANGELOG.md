# v0.0.8

* App context no longer used, pass application reference directly to enabler functions.
* request.get_json() parsed for injection parameters.
* Alternate class names can be specified when adding new classes to the injector (this can happen as many times as you want)
* The Update Mixin has been modified to use a classmethod like the others and now operates on the instance as an argument.
  this changes the API from ```o.update(**data)``` to ```ClassName.update(o, **data)```. The reasoning behind this was to
  ensure that the consuming signal functions would have the same degree of flexibility in decision making as the other hook
  points for the CRUD system.
* Removed the default implementations for hook points like update(). It is not mission of the this library to make assumptions
  at that level. Even the default as_dict() implementation may be turned into a signal in later versions, and I may separate
  out the default impls into a module that can be activated or overridden at will. I would do this to provide the OOB experience
  for people in a hurry and also to allow for maximum choice for those looking to customize.
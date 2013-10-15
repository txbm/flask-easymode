* Add reverse dependency lookup capability against parameters that resolve to other injectable classes
* Add an automatic API generator for CRUD operations. Variable modes[semi-auto, full-auto]
* Make it so that if an injection is called and there are no parameters sent with the request, it can return a list of all objects [optional behavior]
* Allow injectables to be injected under and alternate name from the class name (aliases basically, for brevity)
* Examine a way to have the injector read data that has been validated already. This may become important in order to support the possibility of the incoming data needing to be transformed in some way before it can be used for proper lookup. Also makes it easy to abort a request that's missing data before wasting a trip to the database only to reach the same conclusion.
* Add interface to inject list of classes. Make it take tuples for aliased names and/or a dictionary
* Make the update signal actually a class method in order to allow consumers to implement their own behavior. Same as all the other signals...
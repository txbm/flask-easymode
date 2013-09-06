================
Flask EasyMode
================

Disclaimer: This package was mainly created out of personal motivation for
consolidating common patterns that I use when using Flask for various web
applications.

Primarily it focuses on web API patterns, and model data handling patterns
that generally do not change very often and can be very repetitive at times.

That said-- I have made an effort to modularize and break up the various
features so that his package may still follow the "opt-in" philosophy of
flask.

For this reason, activating the plugin does almost nothing initially until
you start enabling specific features which modify applications variables
and setup certain functionality.

Obviously there are certain components that are usable directly via imports.
For example, the mixins provided are mainly to assist with various common
model class operations that come up on almost every project. These mixins
can just be plainly imported and used separately from even flask itself.

Blinker is a dependency as well as Flask itself and simplejson. Perhaps
at a later date I will break these up into extras_require to allow an even
more purely module install.
# -*- coding: utf-8 -*-

import re

from flask_easymode.exceptions import XHRError, handle_xhr_error

from mrpython.fxn import enum

_CONFIG_PREFIX = 'EM'


def _options():
    return enum(
        XHR_API_ENABLE=False,
        XHR_API_ALLOW_HTTP=False,
        DI_ENABLE=False,
        DI_SCAN=()
    )


class EasyMode(object):

    _injectables = {}
    _app_configs = {}

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    @classmethod
    def _set_config_option(cls, option, value, app):
        config = cls._lookup_config(app)
        if hasattr(config, option):
            setattr(config, option, value)
            cls._sync_config(config, app)

    @classmethod
    def _lookup_config(cls, app):
        try:
            return cls._app_configs[app]
        except KeyError:
            cls._app_configs[app] = _options()
            return cls._app_configs[app]

    @classmethod
    def _sync_config(cls, config, app):
        prefixed = {_CONFIG_PREFIX + '_' + k:
                    v for k, v in config.items.iteritems()}
        app.config.update(prefixed)

    @classmethod
    def _get_config_option(cls, option, app):
        config = cls._lookup_config(app)
        return getattr(config, option)

    @classmethod
    def config(cls, app):
        return cls._lookup_config(app)

    def init_app(self, app):
        EasyMode._sync_config(EasyMode._lookup_config(app), app)

    # as dirty as this looks, it's the best way to do it without using the decorator
    # because there is no built in function in flask yet to do it.
    def enable_xhr(self, app):
        self._set_config_option('XHR_API_ENABLE', True, app)
        app.error_handler_spec.setdefault(None, {}).setdefault(None, []) \
            .append((XHRError, handle_xhr_error))

    def enable_injection(self, app, scan=('json', 'form', 'params', 'query_string')):
        self._set_config_option('DI_ENABLE', True, app)
        self._set_config_option('DI_SCAN', scan, app)

    def add_injectable(self, cls, alt=None):
        cls_name = alt or cls.__name__
        cls_name = re.sub(
            r'(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', r"_\g<0>", cls_name).lower()
        EasyMode._injectables[cls_name] = cls

    def add_injectables(self, classes):
        for cls in classes:
            c, alt = cls, None
            try:
                c, alt = cls
            except ValueError:
                pass
            self._add_injectable(c, alt)

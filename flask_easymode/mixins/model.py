# -*- coding: utf-8 -*-

from blinker import Namespace

easy_signals = Namespace()

object_created = easy_signals.signal('object_created')
object_read = easy_signals.signal('object_read')
object_updated = easy_signals.signal('object_updated')
object_deleted = easy_signals.signal('object_deleted')
object_injected = easy_signals.signal('object_injected')


class Create(object):

    @classmethod
    def create(cls, **kwargs):
        o = cls()
        object_created.send(cls, o=o, **kwargs)
        return o


class Read(object):

    @classmethod
    def read(cls, **kwargs):
        r = object_read.send(cls, **kwargs)
        try:
            return r[0][1]
        except IndexError:
            pass

    @classmethod
    def read_many(cls, **kwargs):
        r = object_read.send(cls, _many=True, **kwargs)
        try:
            return r[0][1]
        except IndexError:
            pass


class Update(object):

    @classmethod
    def update(cls, o, **kwargs):
        r = object_updated.send(cls, o=o, **kwargs)
        try:
            return r[0][1]
        except IndexError:
            pass


class Delete(object):

    @classmethod
    def delete(cls, o, **kwargs):
        r = object_deleted.send(cls, o=o, **kwargs)
        try:
            return r[0][1]
        except IndexError:
            pass


class CRUD(Create, Read, Update, Delete):
    pass


class Injectable(object):

    @classmethod
    def load(cls, conditions, **kwargs):
        r = object_injected.send(cls, conditions=conditions, **kwargs)
        try:
            return r[0][1]
        except IndexError:
            pass


class CRUDI(CRUD, Injectable):
    pass

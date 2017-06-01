#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import utime

from tornado.concurrent import return_future

from .file_storage import Storage as BaseStorage


class Storage(BaseStorage):
    @return_future
    def get(self, callback):
        def middleware(result):
            if result:
                path = self.context.request.url
                file_abspath = self.normalize_path(path)
                utime(file_abspath, None)
            return callback(result)
        return super(Storage, self).get(middleware)

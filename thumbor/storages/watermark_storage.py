#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import os

import thumbor.storages as storages
from tornado.concurrent import return_future


class Storage(storages.BaseStorage):

    @return_future
    def get(self, path, callback):
        abs_path = self.path_on_filesystem(path)

        def file_exists(resource_available):
            if not resource_available:
                callback(None)
            else:
                with open(self.path_on_filesystem(path), 'r') as f:
                    callback(f.read())

        self.exists(None, file_exists, path_on_filesystem=abs_path)

    def path_on_filesystem(self, path):
        return "/".join(
            [
                self.context.config.WATERMARK_ROOT_PATH.rstrip('/'),
                path,
            ]
        )

    @return_future
    def exists(self, path, callback, path_on_filesystem=None):
        if path_on_filesystem is None:
            path_on_filesystem = self.path_on_filesystem(path)
        callback(os.path.exists(path_on_filesystem))

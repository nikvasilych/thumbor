#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com
import os

from thumbor.utils import logger
from .file_storage import Storage as FileStorage


class JoinedPathFileStorageMixin(object):
    """
    конвертирует путь для хранения так что весь путь к картинке становится одной папкой.
    помогает cнизить потребление inodes.
    параметры в конфиге:
    JOINED_PATH_FILE_STORAGE_PATH_MARKER = '/pic/'
    JOINED_PATH_FILE_STORAGE_PATH_REPLACE_DELIMITER = '-'
    ищет начало строки по JOINED_PATH_FILE_STORAGE_PATH_MARKER
    и заменяет в ней '/' (os.sep) на JOINED_PATH_FILE_STORAGE_PATH_REPLACE_DELIMITER
    например:
    '/thumbor/result_storage/v2/un/sa/unsafe/rotate:270/210x140/filters:quality(70)/pic/hotels/15219/dd7571528f309482c0fb56aa931704ff.JPG'
    становится
    '/thumbor/result_storage/v2/un/sa/unsafe/rotate:270/210x140/filters:quality(70)/pic-hotels-15219/dd7571528f309482c0fb56aa931704ff.JPG'
    """

    def _modify_path(self, path):
        try:
            marker = self.context.config.JOINED_PATH_FILE_STORAGE_PATH_MARKER
            delimiter = self.context.config.JOINED_PATH_FILE_STORAGE_PATH_REPLACE_DELIMITER
            if marker and delimiter:
                thumbor_part, file_storage_part = path.split(marker, 1)
                file_storage_part = ''.join((marker, file_storage_part,))
                file_storage_part = file_storage_part.lstrip(os.sep)
                file_storage_path, file_storage_file = file_storage_part.rsplit(os.sep, 1)

                file_storage_path = file_storage_path.replace(os.sep, delimiter)

                new_path = os.sep.join((
                    thumbor_part,
                    file_storage_path,
                    file_storage_file
                ))
                logger.debug("[JOINED_PATH_RESULT_STORAGE] path was converted form \"%s\" to \"%s\"" % (path, new_path))
                path = new_path
        except Exception as e:
            logger.error("[JOINED_PATH_RESULT_STORAGE] error: %s" % str(e))
        return path

    def normalize_path(self, path):
        normalized_path = super(JoinedPathFileStorageMixin, self).normalize_path(path)
        return self._modify_path(normalized_path)


class Storage(JoinedPathFileStorageMixin, FileStorage):
    pass


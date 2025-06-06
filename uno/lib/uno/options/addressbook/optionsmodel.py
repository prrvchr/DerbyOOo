#!
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020-25 https://prrvchr.github.io                                  ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

from ..unotool import createService
from ..unotool import getConfiguration
from ..unotool import getSimpleFile

from ..helper import getDataBaseUrl

from ..configuration import g_identifier
from ..configuration import g_implementation


class OptionsModel():
    def __init__(self, ctx):
        self._ctx = ctx
        self._config = getConfiguration(ctx, g_identifier, True)
        self._url = getDataBaseUrl(ctx)
        self._factor = 60

    @property
    def _Timeout(self):
        timeout = self._config.getByName('ReplicateTimeout')
        return timeout // self._factor
    @property
    def _ViewName(self):
        return self._config.getByName('AddressBookName')

# OptionsModel getter methods
    def getViewData(self):
        return self._Timeout, self._ViewName, self._hasDatasource()

    def getTimeout(self):
         return self._Timeout

    def getViewName(self):
        return self._ViewName

    def getDatasourceUrl(self):
        return self._url


# OptionsModel setter methods
    def loadDriver(self):
        try:
            driver = createService(self._ctx, g_implementation)
        except:
            # Nothing to do the error is already logged
            pass

# OptionsModel getter methods
    def setViewData(self, timeout, view):
        changed = False
        if timeout != self._Timeout:
            self._config.replaceByName('ReplicateTimeout', timeout * self._factor)
        if view != self._ViewName:
            self._config.replaceByName('AddressBookName', view)
        if self._config.hasPendingChanges():
            self._config.commitChanges()
            changed = True
        return changed

# OptionsModel private getter methods
    def _hasDatasource(self):
        return getSimpleFile(self._ctx).exists(self._url)


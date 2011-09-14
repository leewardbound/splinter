# -*- coding: utf-8 -*-

import sys

from splinter.driver.webdriver import BaseWebDriver

# automatically convert Qt types by using api 2
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from pyphantomjs.phantom import Phantom
from pyphantomjs.pyphantomjs import parseArgs
from pyphantomjs.utils import SafeStreamFilter

from PyQt4.QtGui import QApplication

# using pythons stdout and stderr, phantom replaces them
if isinstance(sys.stdout, SafeStreamFilter):
    sys.stdout = sys.stdout.target
if isinstance(sys.stderr, SafeStreamFilter):
    sys.stderr = sys.stderr.target

_executed = None

import atexit
@atexit.register
def exec_app_atexit():
    global _executed
    if _executed is False:
        _executed = True
        QApplication.exec_()

class NotAsynchronousCodeError(Exception):
    def __str__(self):
        return 'You should pass a callback to this function.'

class WebpageError(Exception):
    def __str__(self):
        return 'Page "%s" could not be loaded.' % self.args[0]


class WebDriver(BaseWebDriver):
    def __init__(self, *args, **kwargs):
        self.app = QApplication(sys.argv)
        self.phantom = Phantom(self.app, parseArgs(['bootstrap.js']))
        super(WebDriver, self).__init__(*args, **kwargs)

    def visit(self, url, callback=None):
        global _executed
        _executed = False

        if callback is None:
            raise NotAsynchronousCodeError

        page = self.phantom.createWebPage()
        def exit():
            self.exit()
            #self.phantom._destroy(page)
            #if len(self.phantom.m_pages) == 1:
                #self.phantom.exit()
        def onload(status):
            if status != 'success':
                raise WebpageError(url)
            callback(page, self, exit)
        page.loadFinished.connect(onload)
        page.openUrl(url, 'get', self.phantom.defaultPageSettings)

    def execute(self):
        exec_app_atexit()

    def exit(self):
        self.app.quit()


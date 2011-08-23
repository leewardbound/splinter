# -*- coding: utf-8 -*-

import sys
import signal
import time

import sip

from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager

from pyphantomjs.webpage import WebPage

from PyQt4.QtCore import SIGNAL, QUrl
from PyQt4.QtGui import QApplication

phantom_defaults = {
    'loadImages': True,
    'loadPlugins': False,
    'javascriptEnabled': True,
    'XSSAuditing': False,
    'localAccessRemote': True,
}

# should emulate the selenium api so we can use the full BaseWebDriver power
class WebkitDriver(WebPage):

    def get(self, url):
        self.openUrl(url, 'get', phantom_defaults)

    @property
    def current_url(self):
        return str(self.m_mainFrame.url().toString())

    @property
    def title(self):
        return str(self.m_mainFrame.title())

    def quit(self):
        QApplication.instance().quit()


class WebDriver(BaseWebDriver):
    def __init__(self, *args, **kwargs):
        self.app = QApplication(sys.argv)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.driver = WebkitDriver(self.app)
        #self.element_class = WebDriverElement
        #self._cookie_manager = CookieManager(self.driver)
        super(WebDriver, self).__init__(*args, **kwargs)

    def loaded(self):
        self._loaded = True
        QApplication.instance().quit()

    def visit(self, url):
        self._loaded = False
        self.driver.loadFinished.connect(self.loaded)
        super(WebDriver, self).visit(url)
        QApplication.instance().exec_()
        while not self._loaded:
            time.sleep(0.01)



import unittest

from splinter.browser import Browser

from tests.base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP

class PhantomJSTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('phantomjs')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


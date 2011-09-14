from splinter.browser import Browser
from splinter.driver.webdriver.phantom import WebDriver as PhantomWebDriver, WebpageError

from fake_webapp import EXAMPLE_APP, start_server, stop_server

from pyvows import Vows, expect


@Vows.batch
class PhantomJS(Vows.Context):
    def setup(self):
        start_server()
        self.browser = Browser('phantomjs')

    def teardown(self):
        self.browser.execute()
        stop_server()

    class WhenVisitingKnownPage(Vows.Context):
        @Vows.asyncTopic
        def topic(self, callback):
            def wrapper(page, driver, exit):
                callback(page=page, driver=driver, exit=exit)
                exit()
            self.parent.browser.visit(EXAMPLE_APP, wrapper)

        def should_be_able_to_get_pages_title(self, topic):
            expect(topic.page.m_mainFrame.title()).to_equal('Example Title')

        def should_be_able_to_visit_get_title_and_quit(self, topic):
            expect(topic.driver).to_be_instance_of(PhantomWebDriver)


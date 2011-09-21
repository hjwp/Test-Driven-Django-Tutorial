try: import unittest2 as unittest #for Python <= 2.6
except: import unittest

from selenium import webdriver


ROOT = 'http://127.0.0.1:8000'


class TestPollsAdmin(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.close()


    def test_can_create_new_poll_via_admin_site(self):
        self.browser.get(ROOT + '/admin/')
        polls_link = self.browser.find_element_by_link_text('Polls')
        polls_link.click()
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()



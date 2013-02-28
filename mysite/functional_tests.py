import unittest
from selenium import webdriver

class PollsFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_voting_on_a_poll(self):
        # Herbert goest to check out a cool new polls site he's heard about
        self.browser.get('http://localhost:8000')

        # It is obviously all about polls:
        self.assertIn('Polls', self.browser.title)

        self.fail('finish this test')

if __name__ == '__main__':
    unittest.main()


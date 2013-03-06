import unittest
from selenium import webdriver

class PollsFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def test_voting_on_a_poll(self):
        # Elspeth goest to check out a cool new polls site she's heard about
        self.browser.get('http://localhost:8000')

        # It is obviously all about polls:
        self.assertIn('Poll', self.browser.title)

        # She clicks on the link to the first Poll, which is titled
        # "How awesome is TDD?"
        self.fail('finish this test')

        # She is taken to a poll 'results' page, which says
        # "No-one has voted on this poll yet"

        # She also sees a form, which offers her several choices.
        # There are three options with radio buttons

        # She decided to select "very awesome", which is answer #1

        # Elspeth clicks 'submit'

        # The page refreshes, and she sees that her choice
        # has updated the results.  They now say
        # "1 vote" and "100 %: very awesome".

        # Elspeth decides to try to vote again

        # The site is not very clever (yet) so it lets her

        # She votes for another choice, and the percentages go 50%-50%

        # She votes again, and they go 66% - 33%

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main()


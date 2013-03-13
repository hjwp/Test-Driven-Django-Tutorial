import unittest
from selenium import webdriver

class PollsFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_voting_on_a_poll(self):
        # Elspeth goes to check out a cool new polls site she's heard about

        # She clicks on the link to the first Poll, which is titled
        # "How awesome is TDD?"

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
        pass


    def test_can_create_a_new_poll_via_admin_site(self):
        # Mo the administrator goes to the admin page

        # He sees the familiar 'Django administration' heading

        # He types in his username and passwords and hits return

        # His username and password are accepted, and he is taken to
        # the Site Administration page

        # He sees a section named "Polls" with a model called "Polls" in it

        # He clicks the second link, which takes him to the polls listing page
        # which shows there are no polls yet

        # He clicks the 'Add poll' link

        # He types in an interesting question for the Poll

        # He sets the date and time of publication - it'll be a new year's
        # poll!

        # He sees he can enter choices for the Poll.  He adds three

        # Mo clicks the save button

        # He is returned to the "Polls" listing, where he can see his
        # new poll, listed as a clickable link
        pass


if __name__ == '__main__':
    unittest.main()


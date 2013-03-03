import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PollsFunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def DONTtest_voting_on_a_poll(self):
        # Elspeth goes to check out a cool new polls site she's heard about
        self.browser.get('http://localhost:8000')

        # She clicks on the link to the first Poll, which is titled
        # "How awesome is TDD?"
        self.fail('finish this test')

        # She is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"

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


    def test_can_create_a_new_poll_via_admin_site(self):
        # Mo the administrator goes to the admin page
        self.browser.get('http://localhost:8000/admin/')

        # He sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # He types in his username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # His username and password are accepted, and he is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # He sees a section named "Polls" with a model called "Polls" in it
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)
        self.fail('Use the admin site to create a poll')

        # He clicks the second link, which takes him to the polls listing page
        # which shows there are no polls yet
        polls_links[1].click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 polls', body.text)

        # He clicks the 'Add poll' link
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()


if __name__ == '__main__':
    unittest.main()


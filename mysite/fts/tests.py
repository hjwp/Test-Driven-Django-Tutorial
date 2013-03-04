from datetime import datetime
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AdminPage(object):

    def __init__(self, test, browser):
        self.test = test
        self.browser = browser

    def login(self):
        # Mo the administrator goes to the admin page
        self.browser.get(self.test.live_server_url + '/admin/')

        # He sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.test.assertIn('Django administration', body.text)

        # He types in his username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # His username and password are accepted, and he is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.test.assertIn('Site administration', body.text)


    def logout(self):
        self.browser.find_element_by_link_text('Log out').click()


    def add_poll(self, question, pub_date, choices):
        self.browser.get(self.test.live_server_url + '/admin/')
        # He sees a section named "Polls" with a model called "Polls" in it
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.test.assertEquals(len(polls_links), 2)
        polls_links[1].click()

        # He clicks the 'Add poll' link
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()

        # He types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys(question)

        # He sets the date and time of publication
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys(pub_date.date().strftime('%x'))
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys(pub_date.time().strftime('%X'))

        # He sees he can enter choices for the Poll.  He adds them
        for no, choice in enumerate(choices):
            choice_input = self.browser.find_element_by_name(
                'choice_set-%d-choice' % (no,)
            )
            choice_input.send_keys(choice)

        # Mo clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # He is returned to the "Polls" listing, where he can see his
        # new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text(
                question
        )
        self.test.assertEquals(len(new_poll_links), 1)



class PollsFunctionalTest(LiveServerTestCase):

    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_voting_on_a_poll(self):
        # Mo the administrator has entered a couple of polls
        admin_page = AdminPage(self, self.browser)
        admin_page.login()
        admin_page.add_poll(
            question="How awesome is TDD?",
            pub_date = datetime.today(),
            choices=['Very awesome', 'Quite awesome', 'Moderately awesome'],
        )
        admin_page.add_poll(
            question="Which workshop treat do you prefer?",
            pub_date = datetime.today(),
            choices=['Beer', 'Pizza', 'The Acquisition of Knowledge'],
        )
        admin_page.logout()

        # Elspeth goes to check out a cool new polls site she's heard about
        self.browser.get(self.live_server_url)

        # It is obviously all about polls:
        self.assertIn('Poll', self.browser.title)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Current polls')

        # She clicks on the link to the first Poll, which is titled
        # "How awesome is TDD?"
        self.browser.find_element_by_link_text('How awesome is TDD?').click()

        # She is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        body = self.browser.find_element_by_tag_name('body')
        self.test.assertIn("no-one has voted on this poll yet", body.text)

        # She also sees a form, which offers her several choices.
        # There are three options with radio buttons
        self.fail('finish this test')

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
        # and creates a new poll, with 3 choices
        admin_page = AdminPage(self, self.browser)
        admin_page.login()
        admin_page.add_poll(
            question="How awesome is Test-Driven Development?",
            pub_date=datetime(2012,01,01),
            choices = ['Very awesome', 'Quite awesome', 'Moderately awesome']
        )
        admin_page.logout()





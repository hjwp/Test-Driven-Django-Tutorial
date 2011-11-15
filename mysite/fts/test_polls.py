from collections import namedtuple
from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys

PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo("How awesome is Test-Driven Development?", [
    'Very awesome',
    'Quite awesome',
    'Moderately awesome',
])
POLL2 = PollInfo("Which workshop treat do you prefer?", [
    'Beer',
    'Pizza',
    'The Acquisition of Knowledge',
])

class TestPolls(FunctionalTest):

    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        self.fail('todo: finish this test, using the comments below')

        # Now, Herbert the regular user goes to the homepage of the site.
        # He sees an h1 heading which says "Current Polls"

        # Under this, he sees that the poll questions are listed

        # Now he notices that the poll questions are also links

        # So he clicks on the link witht the text 'How awesome is test-driven development?'

        # rest of test TBC!



    def _setup_polls_via_admin(self):
        # Gertrude logs into the admin site
        self.browser.get(ROOT + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # She has a number of polls to enter.  For each one, she:

        for poll_info in [POLL1, POLL2]:
            # Follows the link to the Polls app, and adds a new Poll
            self.browser.find_elements_by_link_text('Polls')[1].click()
            self.browser.find_element_by_link_text('Add poll').click()

            # Enters its name, and uses the 'today' and 'now' buttons to set
            # the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            self.browser.find_element_by_link_text('Today').click()
            self.browser.find_element_by_link_text('Now').click()

            # Sees she can enter choices for the Poll on this same page,
            # so she does
            for i, choice_text in enumerate(poll_info.choices):
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                choice_field.send_keys(choice_text)

            # Saves her new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(
                    poll_info.question
            )
            self.assertEquals(len(new_poll_links), 1)

            # She goes back to the root of the admin site
            self.browser.get(ROOT + '/admin/')

        # She logs out of the admin site
        self.browser.find_element_by_link_text('Log out').click()




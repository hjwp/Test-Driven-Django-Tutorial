from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys
from collections import namedtuple

PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question="How awesome is Test-Driven Development?",
    choices=[
        'Very awesome',
        'Quite awesome',
        'Moderately awesome',
    ],
)
POLL2 = PollInfo(
    question="Which workshop treat do you prefer?",
    choices=[
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge',
    ],
)

class TestPolls(FunctionalTest):
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


    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(ROOT)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')

        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        first_poll_title = 'How awesome is Test-Driven Development?'
        self.browser.find_element_by_link_text(first_poll_title).click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

        # He also sees a form, which offers him several choices.
        # There are three options with radio buttons
        choice_inputs = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        self.assertEquals(len(choice_inputs), 3)

        # The buttons have labels to explain them
        choice_labels = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
            'Vote:', # this label is auto-generated for the whole form
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])
        # He decided to select "very awesome", which is answer #1
        chosen = self.browser.find_element_by_css_selector(
                "input[value='1']"
        )
        chosen.click()

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # The page also says "1 vote"
        self.assertIn('1 vote', body_text)

        # Harold suspects that the website isn't very well protected
        # against people submitting multiple votes yet, so he tries
        # to do a little astroturfing

        chosen = self.browser.find_element_by_css_selector(
                "input[value='1']"
        )
        chosen.click()
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  it still says
        # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # But the page now says "2 votes"
        self.assertIn('2 votes', body_text)

        # Cackling manically over his l33t haxx0ring skills, he tries
        # voting for a different choice
        chosen = self.browser.find_element_by_css_selector(
                "input[value='2']"
        )
        chosen.click()
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # Now, the percentages update, as well as the votes
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('67 %: Very awesome', body_text)
        self.assertIn('33 %: Quite awesome', body_text)
        self.assertIn('3 votes', body_text)

        # Satisfied, he goes back to sleep


from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys

class TestPollsAdmin(FunctionalTest):

    def test_can_create_new_poll_via_admin_site(self):

        # Gertrude opens her web browser, and goes to the admin page
        self.browser.get(ROOT + '/admin/')

        # She sees the familiar 'Django Administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('adm1n')
        password_field.send_keys(Keys.RETURN)

        # She now sees a hyperlink that says "Polls"
        polls_link = self.browser.find_element_by_link_text('Polls')

        # She sees a hyperlink that says "Polls"
        polls_link = self.browser.find_element_by_link_text('Polls')

        # So, she clicks it
        polls_link.click()

        # She is taken to a new page on which she sees a link to "Add poll"
        new_poll_link = self.browser.find_element_by_link_text('Add poll')

        # So she clicks that too
        new_poll_link.click()



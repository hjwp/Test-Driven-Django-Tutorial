from functional_tests import FunctionalTest, ROOT

class TestPollsAdmin(FunctionalTest):

    def test_can_create_new_poll_via_admin_site(self):
        self.browser.get(ROOT + '/admin/')
        polls_link = self.browser.find_element_by_link_text('Polls')
        polls_link.click()
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()



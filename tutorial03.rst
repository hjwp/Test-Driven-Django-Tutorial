Welcome to part 3 of the tutorial!  This week we'll finally get into writing
our own web pages, rather than using the Django Admin site.

Let's pick up our FT where we left off - we now have the admin site set up to
add Polls, including Choices.  We now want to flesh out what the user sees.

Last time we wrote the code to get Gertrude the admin to log in and create a 
poll.  Let's write the next bit, where Herbert the normal user opens up our
website, sees some polls and votes on them.

.. sourcecode:: python

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
        self.browser.find_element_by_link_text('How awesome is Test-Driven Development?').click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Poll Results')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

Let's run that, and see where we get::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/Test-Driven-Django-Tutorial/mysite/fts/test_polls.py", line 57, in test_voting_on_a_new_poll
        self.assertEquals(heading.text, 'Polls')
    AssertionError: u'Page not found (404)' != 'Polls'

    ----------------------------------------------------------------------
    Ran 2 tests in 19.772s


The FT is telling us that 

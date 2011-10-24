Welcome to part 3 of the tutorial!  This week we'll finally get into writing
our own web pages, rather than using the Django Admin site.

Let's pick up our FT where we left off - we now have the admin site set up to
add Polls, including Choices.  We now want to flesh out what the user sees.

First, let's run our FT, to see where we are::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/Test-Driven-Django-Tutorial/mysite/fts/test_polls.py", line 57, in test_voting_on_a_new_poll
        self.assertEquals(heading.text, 'Polls')
    AssertionError: u'Page not found (404)' != 'Polls'

    ----------------------------------------------------------------------
    Ran 2 tests in 19.772s

      1.4% ( 17.0)   nautilu

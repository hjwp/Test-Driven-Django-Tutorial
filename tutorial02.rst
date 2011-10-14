Welcome to part 2 of the tutorial!  Hope you've had a little break, maybe a
nice chocolate biscuit, and are super-excited to do more!

So far we've only worked with the Django admin site - now it's time to start
creating our own web pages.  Much more fun.

So, the next thing we want to do is write some of the test of what non-admin
users will see of our polls application - viewing existing polls, responding to
polls by submitting a choice, and viewing poll results.

So, let's write a functional test that does all three of those things. We'll
create a new file for it called ``fts/test_polls.py``.  We'll be re-using some
of the code from ``test_polls_admin.py``, so you might want to do a "save as"
based on that file.

Let's start by writing out our FT as human-readable comments, which describe
the user's actions, and the expected behaviour of the site::

    from functional_tests import FunctionalTest, ROOT
    from selenium.webdriver.common.keys import Keys

    class TestPolls(FunctionalTest):

        def test_voting_on_a_new_poll(self):
            # First, Gertrude the administrator logs into the admin site and
            # creates a couple of new Polls, and their response choices

            # Now, Herbert the regular user goes to the homepage of the site. He
            # sees a list of polls.

            # He clicks on the link to the first Poll, which is called
            # 'How awesome is test-driven development?'

            # He is taken to a poll 'results' page, which says
            # "no-one has voted on this poll yet"

            # He also sees a form, which offers him several choices.
            # He decided to select "very awesome"

            # He clicks 'submit'

            # The page refreshes, and he sees that his choice
            # has updated the results.  they now say
            # "100 %: very awesome".

            # The page also says "1 votes"

            # Satisfied, he goes back to sleep


A nice little test, but that very first comment rather glosses over a lot.  We
haven't created anything to do with choices yet!  Let's split out the Gertrude
bit into its own method, for tidiness::

        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

And add the new method::

    class TestPolls(FunctionalTest):
        def _setup_polls_via_admin(self):


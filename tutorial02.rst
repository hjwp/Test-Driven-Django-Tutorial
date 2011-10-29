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
the user's actions, and the expected behaviour of the site

.. sourcecode:: python

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
bit into its own method, for tidiness

.. sourcecode:: python

        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

And add the new method

.. sourcecode:: python

    class TestPolls(FunctionalTest):

        def _setup_polls_via_admin(self):
            # Gertrude logs into the admin site
            self.browser.get(ROOT + '/admin/')
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('admin')
            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('adm1n')
            password_field.send_keys(Keys.RETURN)

            # She follows the link to the Polls app, and adds a new Poll
            self.browser.find_elements_by_link_text('Polls')[1].click()
            self.browser.find_element_by_link_text('Add poll').click()

            # She enters its name, and uses the 'today' and 'now' buttons to set
            # the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys("How awesome is Test-Driven Development?")
            self.browser.find_element_by_link_text('Today').click()
            self.browser.find_element_by_link_text('Now').click()

            # She sees she can enter choices for the Poll.  She adds three
            choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
            choice_1.send_keys('Very awesome')
            choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
            choice_2.send_keys('Quite awesome')
            choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
            choice_3.send_keys('Moderately awesome')

            # She saves her new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # She is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link
            new_poll_links = self.browser.find_elements_by_link_text(
                    "How awesome is Test-Driven Development?"
            )
            self.assertEquals(len(new_poll_links), 1)

            # She logs out of the admin site
            self.browser.find_element_by_link_text('Log out').click()

Looks like I was lying about not messing about with the admin site any more. Ah well. Let's try running our fts again::

    ======================================================================
    ERROR: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 40, in test_voting_on_a_new_poll
        self._setup_polls_via_admin()
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 26, in _setup_polls_via_admin
        choice_1 = self.browser.find_element_by_name('choice_0')
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 244, in find_element_by_name
        return self.find_element(by=By.NAME, value=name)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 525, in find_element
        {'using': by, 'value': value})['value']
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 144, in execute
        self.error_handler.check_response(response)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/errorhandler.py", line 118, in check_response
        raise exception_class(message, screen, stacktrace)
    NoSuchElementException: Message: u'Unable to locate element: {"method":"name","selector":"choice_set-0-choice"}' 

    ----------------------------------------------------------------------
    Ran 2 tests in 23.710s

    FAILED (errors=1)


Right, the FT can't find the "choice" elements to fill in on the admin page.
Let's go ahead and create our "Choice" model then. As usual, we start with some
unit tests - ``polls/tests.py``

.. sourcecode:: python

    class TestPollChoicesModel(TestCase):

        def test_creating_some_choices_for_a_poll(self):
            # start by creating a new Poll object
            poll = Poll()
            poll.question="What's up?"
            poll.pub_date = datetime.datetime(2012, 12, 25)
            poll.save()

            # now create a Choice object
            choice = Choice()

            # link it with our Poll
            choice.poll = poll

            # give it some text
            choice.choice = "doin' fine..."

            # and let's say it's had some votes
            choice.votes = 3

            # save it
            choice.save()

            # try retrieving it from the database, using the poll object's reverse
            # lookup
            poll_choices = poll.choice_set.all()
            self.assertEquals(poll_choices.count(), 1)

            # finally, check its attributes have been saved
            choice_from_db = poll_choices[0]
            self.assertEquals(choice_from_db, choice)
            self.assertEquals(choice_from_db.choice, "doin' fine...")
            self.assertEquals(choice_from_db.votes, 3)

Also remember to add the import to the top of the file

.. sourcecode:: python

    from polls.models import Choice, Poll

And we may as well give it something to import too - in ``polls/models.py``

.. sourcecode:: python

    class Choice(object):
        pass

And let's do a unit test run::

    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.TestPollChoicesModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 62, in test_creating_some_choices_for_a_poll
        choice.save()
    AttributeError: 'Choice' object has no attribute 'save'

    ----------------------------------------------------------------------
    Ran 326 tests in 2.745s

    FAILED (errors=1)

no attribute save - let's make our Choice class into a proper Django model::

    class Choice(models.Model):
        pass

Have you noticed it says "326 tests"?  Surely we haven't written that many?
That's because ``manage.py test`` runs all the tests for all the Django stuff,
as well as your own tests.  If you want to, you can tell Django to just run the
tests for your own app, like this::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    E...
    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.TestPollChoicesModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 66, in test_creating_some_choices_for_a_poll
        poll_choices = poll.choice_set.all()
    AttributeError: 'Poll' object has no attribute 'choice_set'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    FAILED (errors=1)
    Destroying test database for alias 'default'...

Our tests are complaining that the "poll" object has no attribute
``choice_set``. This is a special attribute that allows you to retrieve all the
related Choice objects for a particular poll, and it gets added by Django whenever
you define a relationship between two models - a foreign key relationship for 
example. Let's add that now

.. sourcecode:: python

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)

Re-running the unit tests, we get::

    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.TestPollChoicesModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 72, in test_creating_some_choices_for_a_poll
        self.assertEquals(choice_from_db.choice, "doin' fine")
    AttributeError: 'Choice' object has no attribute 'choice'

    ----------------------------------------------------------------------

Let's give Choice a choice...

.. sourcecode:: python

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)

Tests again::

    AttributeError: 'Choice' object has no attribute 'votes'

Let's add votes

.. sourcecode:: python

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField()

Another test run?::

    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK

Hooray! What's next?  Well, one of the great things about TDD is that, once
you've written your tests, you don't really have to keep track of what's next
any more.  You can can just run the tests, and they'll tell you what to do.
So, what do the tests want?  Let's re-run the FTs::

    ======================================================================
    ERROR: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 40, in test_voting_on_a_new_poll
        self._setup_polls_via_admin()
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 26, in _setup_polls_via_admin
        choice_1 = self.browser.find_element_by_name('choice_0')
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 244, in find_element_by_name
        return self.find_element(by=By.NAME, value=name)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 525, in find_element
        {'using': by, 'value': value})['value']
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 144, in execute
        self.error_handler.check_response(response)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/errorhandler.py", line 118, in check_response
        raise exception_class(message, screen, stacktrace)
    NoSuchElementException: Message: u'Unable to locate element: {"method":"name","selector":"choice_set-0-choice"}' 

    ----------------------------------------------------------------------

Ah, the FTs want to be able to add "choices" to a poll from the admin view.
Django has a way:

Let's edit ``polls/admin.py``, and do some customising on the way the Poll
admin page works

.. sourcecode:: python

    from django.contrib import admin
    from polls.models import Choice, Poll

    class ChoiceInline(admin.StackedInline):
        model = Choice
        extra = 3

    class PollAdmin(admin.ModelAdmin):
        inlines = [ChoiceInline]

    admin.site.register(Poll, PollAdmin)

Django has lots of ways of customising the admin site, and I don't want to
dwell on them for too long - check out the docs for more info:
https://docs.djangoproject.com/en/1.3/intro/tutorial02/#adding-related-objects

Let's run the FT again::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 48, in test_voting_on_a_new_poll
        self._setup_polls_via_admin()
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 42, in _setup_polls_via_admin
        self.assertEquals(len(new_poll_links), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------

You may have noticed, during the run, that the form got all grumpy about the
'votes' field being required (if you don't believe me, why not spin up the
test server using ``manage.py runserver`` and check for yourself?  Remember, you
may need to ``syncdb``)

Let's make 'votes' default to 0, by adding a new test in ``tests.py``

.. sourcecode:: python

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)

And run it::

    AssertionError: None != 0

And set the default, in ``polls/models.py``

.. sourcecode:: python

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

And re-run our tests::

    .
    ----------------------------------------------------------------------
    Ran 2 tests in 21.043s

    OK

Hooray!  Tune in next week, for when we *really* get off the admin site, and
into testing some Django pages we've written ourselves...


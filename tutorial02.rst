Welcome to part 2 of the tutorial!  Hope you've had a little break, maybe a
`nice chocolate biscuit <http://www.nicecupofteaandasitdown.com/biscuits/previous.php3?item=29>`_,
and are super-excited to do more!

Tutorial 2 - Customising the admin site
=======================================

Last time we managed to get the admin site up and running, this time it's time
to actualy get it working the way we want it to, so that we can use it to
create new polls for our site.

Here's an outline of what we're going to do:

    * Create an FT that can create a new poll via the admin site

    * Customise the human-readable display for polls

    * Create "Choice" related model objects to go with polls

    * Add choices to the admin site



Inspecting the admin site to decide what to test next
-----------------------------------------------------

Let's fire up the development server, and do a bit of browsing around the admin
site - that way we can figure out what we want the "Polls" bit to look like.::

    python manage.py runserver

Then, open your web browser and go to ``http://localhost:8000/admin/``. Login
with the admin username and password (``admin / adm1n``).

If you go into the Polls section and try and create a new Poll, you need to
click on a link that says "Add Poll" - let's add that to our FT.  In
``fts/tests.py``:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # She now sees a couple of hyperlink that says "Polls"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)

        # The second one looks more exciting, so she clicks it
        polls_links[1].click()

        # She is taken to the polls listing page, which shows she has
        # no polls yet
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 polls', body.text)

        # She sees a link to 'add' a new poll, so she clicks it
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()

``find_element_by_link_text`` is a very useful Selenium function - it's a good
combination of the presentation layer (what the user sees when they click a
link) and the functionality of the site (hyperlink one of the major ways that
users actually interact with a website)

Now, when you click the link you should see a menu a bit like this.

.. image:: /static/images/add_poll_need_verbose_name_for_pub_date.png

Pretty neat, but `Pub date` isn't a very nice label for our publication date
field.  Django normally generates labels for its admin fields automatically, by
just taking the field name and capitalising it, converting underscores to
spaces.  So that works well for ``question``, but not so well for ``pub_date``.

So that's one thing we'll want to change.  Let's add a test for that to the end
of our FT

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # She sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Date published:', body.text)


Mmmh, "Date Published", much nicer.


More ways of finding elements on the page using Selenium
--------------------------------------------------------

If you try filling in a new Poll, and fill in the 'date' entry but not a
'time'.  You'll find django complains that the field is required. So, in our
test, we need to fill in three fields: `question`, `date`, and `time`. 

In order to get Selenium to find the text input boxes for those fields, there
are several options::

    find_element_by_id 
    find_element_by_xpath
    find_element_by_link_text
    find_element_by_name
    find_element_by_tag_name
    find_element_by_css_selector

And several others - find out more in the selenium documentation (choose Python
as your language for the examples), or just by looking at the source code:
http://seleniumhq.org/docs/03_webdriver.html
http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py

In our case `by name` is a useful way of finding fields, because the name
attribute is usually associated with input fields from forms.  If you take a
look at the HTML source code for the Django admin page for entering a new poll
(either the raw source, or using a tool like Firebug, or developer tools in
Google Chrome), you'll find out that the 'name' for our three fields are
`question`, `pub_date_0` and `pub_date_1`.:


.. sourcecode:: html
    :filename: html source for admin site

    <label for="id_question" class="required">Question:</label>
    <input id="id_question" type="text" class="vTextField" name="question" maxlength="200" />

    <label for="id_pub_date_0" class="required">Date published:</label>
    <p class="datetime">
        Date: 
        <input id="id_pub_date_0" type="text" class="vDateField" name="pub_date_0" size="10" />
        <br />
        Time:
        <input id="id_pub_date_1" type="text" class="vTimeField" name="pub_date_1" size="8" />
    </p>
                        
                    

Let's use them in our FT

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # She sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Date published:', body.text)

        # She types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys("How awesome is Test-Driven Development?")

        # She sets the date and time of publication - it'll be a new year's
        # poll!
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('01/01/12')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')


We can also use the CSS selector to pick up the "Save" button

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()


Then, when you hit 'Save', you'll see that we get taken back to the Polls
listings page.  You'll notice that the new poll is just described as "Poll
object".  

.. image:: /static/images/django_admin_poll_object_needs_verbose_name.png

Django lets you give them more descriptive names, including any attribute of
the object.  So let's say we want our polls listed by their question... And
let's call that the end of our FT - you can get rid of the ``self.fail``.

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # She is returned to the "Polls" listing, where she can see her
        # new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text(
                "How awesome is Test-Driven Development?"
        )
        self.assertEquals(len(new_poll_links), 1)

        # Satisfied, she goes back to sleep

That's it for now - if you've lost track in amongst all the copy & pasting, you
can compare your version to mine, which is hosted here:

https://github.com/hjwp/Test-Driven-Django-Tutorial/blob/master/mysite/fts/tests.py`


Human-readable names for models and their attributes
----------------------------------------------------

Let's re-run our tests.  Here's our first expected failure, the fact that "Pub
date" isn't the label we want for our field ("Date published")::

    python manage.py test fts

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 43, in 
      test_can_create_new_poll_via_admin_site
        self.assertIn('Date published:', body.text)
        django.kill() #TODO: doesn't kill child processes, fix
    AssertionError: 'Date published:' not found in u'Django administration\n
    Welcome, admin. Change password / Log out\n
    Home \u203a Polls \u203a Polls \u203a Add poll\nAdd poll\nQuestion:\n
    Pub date:\nDate:  Today | \nTime:  Now | '

    ----------------------------------------------------------------------


Unit testing the verbose name for pub_date
------------------------------------------

Django stores human-readable names for model attributes in a special attribute
called `verbose_name`.  Let's write a unit test that checks the verbose name
for our ``pub_date`` field.  Add the following method to ``polls/tests.py``

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    def test_verbose_name_for_pub_date(self):
        for field in Poll._meta.fields:
            if field.name ==  'pub_date':
                self.assertEquals(field.verbose_name, 'Date published')


To write this test, we have to grovel through the ``_meta`` attribute on the
Poll class.  That's some Django-voodoo right there, and you may have to take my
word for it, but it's a way to get at some of the information about the
metadata on the model. There's more info here (James Bennet is one of the
original Django developers, and wrote a book about it too)
http://www.b-list.org/weblog/2007/nov/04/working-models/

Anyway, running our tests with ``python manage.py test polls`` gives us our
expected fail::

    AssertionError: 'pub date' != 'Date published'


Now that we have a unit test, we can implement! Let's make a change in
``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

Run the unit tests again to check that's worked::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

Now, re-running our functional tests, things have moved on::


    $ python manage.py test fts

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 63, in 
      test_can_create_new_poll_via_admin_site
        self.assertEquals(len(new_poll_links), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------

We're almost there - the FT has managed to create and save the new poll, but
when it gets back to the listings page, it can't find a hyperlink whose text is
the new question - it's still listed as an unhelpful "Poll object"


To make this work, we need to tell Django how to print out a Poll object.  This
happens in the ``__unicode__`` method.  As usual, we unit test first, in this
case it's a very simple one -

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    def test_poll_objects_are_named_after_their_question(self):
        p = Poll()
        p.question = 'How is babby formed?'
        self.assertEquals(unicode(p), 'How is babby formed?')

Running the unit tests shows the following error::

    ======================================================================
    FAIL: test_poll_objects_are_named_after_their_question (polls.tests.PollModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 37, in 
      test_poll_objects_are_named_after_their_question
        self.assertEquals(unicode(p), 'How is babby formed?')
    AssertionError: u'Poll object' != 'How is babby formed?'

    ----------------------------------------------------------------------

And the fix is simple too - we define a ``__unicode__`` method on our Poll
class, in ``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

        def __unicode__(self):
            return self.question


And you should now find that the unit tests pass::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    ...
    Ran 3 tests in 0.001s


And now, our functional tests should get to the end::

    AssertionError: todo: finish tests


Let's do just that.
 

Adding Choices to the Poll admin page
=====================================

Now, our polls currently only have a question - we want to give each poll a set
of possible answers, or "choices", for the user to pick between. Ideally, we
want Gertrude to be able to fill in the choices on the same screen as she
defines the question.  Thankfully, Django allows this - you can see it in the
Django tutorial, you can have Choices on the same page as the "Add new Poll"
page.

https://docs.djangoproject.com/en/1.4/intro/tutorial02/#adding-related-objects

So let's add that as an intermediate step in our FT, in between where Florence
enters the question, and when she hits save.  

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        [...]
        time_field.send_keys('00:00')

        # She sees she can enter choices for the Poll.  She adds three
        choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
        choice_1.send_keys('Very awesome')
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Quite awesome')
        choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
        choice_3.send_keys('Moderately awesome')

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        [...]


For now you'll have to trust me on those ``choice_set-0-choice`` name
attributes! Let's try running our fts again::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"name","selector":"choice_set-0-choice"}' 


Relations between models: Polls and Choices
-------------------------------------------

Right, naturally the FT can't find the "choice" elements to fill in on the
admin page, because there's no such thing yet! Let's go ahead and create our
"Choice" model then. As usual, we start with some unit tests - in ``polls/tests.py``

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    class ChoiceModelTest(TestCase):

        def test_creating_some_choices_for_a_poll(self):
            # start by creating a new Poll object
            poll = Poll()
            poll.question="What's up?"
            poll.pub_date = timezone.now()
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
    :filename: mysite/polls/tests.py

    from polls.models import Choice, Poll

And we may as well give it something to import too - in ``polls/models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(object):
        pass

And let's do a unit test run::

    python manage.py test polls

    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.ChoiceModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 62, in test_creating_some_choices_for_a_poll
        choice.save()
    AttributeError: 'Choice' object has no attribute 'save'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.745s

    FAILED (errors=1)

No attribute save - let's make our Choice class into a proper Django model::

    class Choice(models.Model):
        pass

OK, our tests are complaining that the "poll" object has no attribute
``choice_set``. This is a special attribute that allows you to retrieve all the
related Choice objects for a particular poll, and it gets added by Django
whenever you define a relationship between two models - a foreign key
relationship for example. 

You can see some more examples of creating Polls and related Choices here:

https://docs.djangoproject.com/en/1.4/intro/tutorial01/#playing-with-the-api

Let's add that relationship now

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)

Re-running the unit tests, we get::

    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.ChoiceModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 72, in test_creating_some_choices_for_a_poll
        self.assertEquals(choice_from_db.choice, "doin' fine")
    AttributeError: 'Choice' object has no attribute 'choice'

    ----------------------------------------------------------------------

Let's give Choice a choice...

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)

Tests again::

    AttributeError: 'Choice' object has no attribute 'votes'

Let's add votes

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField()

Another test run?::

    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK

Further customisations of the admin view: related objects inline
----------------------------------------------------------------

Hooray! What's next?  Well, one of the great things about TDD is that, once
you've written your tests, you don't really have to keep track of what's next
any more.  You can can just run the tests, and they'll tell you what to do. So,
what do the tests want?  Let's re-run the FTs::

    python manage.py test fts

    ======================================================================
    ERROR: test_voting_on_a_new_poll (test_polls.PollsTest)
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

That's right, the FTs want to be able to add "choices" to a poll in the admin
view. Django has a way. Let's edit ``polls/admin.py``, and do some customising
on the way the Poll admin page works

.. sourcecode:: python
    :filename: mysite/polls/admin.py

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

https://docs.djangoproject.com/en/1.4/intro/tutorial02/#adding-related-objects

Let's run the FT again::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 48, in test_voting_on_a_new_poll
        self._setup_polls_via_admin()
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 42, in _setup_polls_via_admin
        self.assertEquals(len(new_poll_links), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------

You may have noticed, during the run, that the form got all grumpy about the
'votes' field being required (if you don't believe me, why not spin up the test
server using ``manage.py runserver`` and check for yourself?  Remember, you may
need to ``syncdb``... Alternatively you can add a ``time.sleep(10)`` to the FT
just before the error, and that will let you see what's happening)

Let's make 'votes' default to 0, by adding a new test in ``polls/tests.py``

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)

And run it::

    python manage.py test polls
    [...]
    AssertionError: None != 0

And set the default, in ``polls/models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

And re-run our tests::

    .
    ----------------------------------------------------------------------
    Ran 2 tests in 21.043s

    OK

Hooray!  Tune in next week, for when we finally get off the admin site, and
into testing some Django pages we've written ourselves...


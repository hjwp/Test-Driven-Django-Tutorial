
The Concept
-----------

This idea is to provide an introduction to Test-Driven web development using
Django (and Python).  Essentially, we run through the same material as the
official Django tutorial, but instead of 'just' writing code, we write tests
first at each stage - both "functional tests", in which we actually pretend to
be a user, and drive a real web browser, as well as "unit tests", which help us
to design and piece together the individual working parts of the code.



Who is this for?
----------------

Maybe you've done a bit of Python programming, and you're thinking of learning
Django, and you want to do it "properly".  Maybe you've done some test-driven
web development in another language, and you want to find out about how it all
works in the Python world.  Most importantly, you've heard of, or had experience
of, working on a project where complexity has started to get the better of you,
where you're scared to make changes, and you wished there had been better
testing from the get-go.



Why should you listen to me?
----------------------------

I was lucky enough to get my first "proper" software development job with a
bunch of Extreme Programming fanatics, who've thoroughly inculcated me into
their cult of Test-Driven development.  Believe me when I say I'm contrary
enough to have questioned every single practice, challenged every single
decision, moaned about every extra minute spent doing "pointless" tests instead
of writing "proper" code.  But I've come round to the idea now, and whenever
I've had to go back to some of my old projects which don't have tests, boy have
I ever realised the wisdom of the approach.

So, I've learnt from some really good people, and the learning process is still 
fresh in my mind, so I hope I'll be good at communicating it.  Most importantly,
I still have the passion of a recent convert, so I hope I'll be good at conveying
some enthusiasm.



Why Test-Driven Development?
----------------------------

The thing is, when you start out on  a small project, you don't really need tests.
Tests take time to write - as much as, if not more than, the actual code for your
application.  You've got to learn testing frameworks, and they inevitably come 
with a whole host of their own problems (and this applies especially to web-browser
testing. oh boy.).  Meanwhile, you know you could just knock out a few lines of
code, and your application would be off the ground, and would start to be
useful. There are deadlines!  Clients who are paying for your time!  Or maybe
just the smell of that `Internet money`, and arriving late to the party means
none of it will be for you!

Well, that's all true.  At first.  At first, it's obvious whether everything 
works.  You can just log into the dev server, click around a bit, and see
whether everything looks OK.  And changing this bit of code over `here`, is
only ever going to affect these things `here` and `here`... So it's easy to
change stuff and see if you've broken anything...

But as soon as your project gets slightly larger, complexity rears its ugly
head.  Combinatorial explosion starts to make you its bitch. Changes start to
have unpredictable effects.  You start to worry about making changes to that
thing over there, because you wrote it ages ago, and you're pretty sure other
things depend on it... best to just use it as it is, even though it's hideously
ugly...  Well, anyway, changing this thing over `here` shouldn't affect too much
stuff.  I'll just run through the main bits of the site to check... Can't possibly
check everything though... Oh well, I'll just deploy and see if anyone complains...

Automated tests can save you from this fate.  If you have automated tests, you can
know for sure whether or not your latest changes broke anything.  With tests, 
you're free to keep refactoring your code, to keep trying out new ways to optimise
things, to keep adding new functionality, safe in the knowledge that your tests
will let you know if you get things wrong.

Look, that's got to be enough evangelising.  If you don't believe me, just ask
someone else with experience.  They know.  Now, onto the practicals.




What's the approach?
--------------------

Test-First!  So, before we're allowed to write any real production code, we write
some tests.  We start by writing some browser tests - what I call `functional`
tests, which simulate what an actual user would see and do.  We'll use `Selenium`,
a test tool which actually opens up a real web browser, and then drives it like
a real user, clicking on links and buttons, and checking what is shown on the
screen.  These are the tests that will tell us whether or not our application
behaves the way we want it to, from the user's point of view.

Once we've written our functional tests (which, incidentally, have forced us
to thing through the way our application will work, from the point of view
of the user - never a bad thing...) we can start to think about how we want
to implement that functionality from a technical point of view.

Thankfully we won't have to do too much difficult thinking, because the functional
tests will be our guide - what do we have to do to get the functional tests to
get a bit further towards passing?  How would we implement that?

Once we've settled on the function or the class that will solve our first problem,
we can write a unit test for it.  Again, it forces us to think about how it will
work from the outside, before we write it.


Some setup before we start
--------------------------

For functional testing, we'll be using the excellent Selenium.  Let's install that,
and Django, and a couple of other Python modules we might need::

    easy_install django
    easy_install selenium
    easy_install pexpect
    easy_install mock

We also need the selenium java server::

    wget -O selenium-server-standalone-2.6.0.jar http://selenium.googlecode.com/files/selenium-server-standalone-2.6.0.jar 



Setting up our Django project, and settings.py
----------------------------------------------

Django structures websites as "projects", each of which can have several
constituent "apps"... Ostensibly, the idea is that apps can be self-contained,
so that you could use one app in several projects... Well, I've never actually
seen that done, but it remains a nice way of splitting up your code.

As per the official Django tutorial, we'll set up our project, and its first app,
a simple application to handle online polls.

Django has a couple of command line tools to set these up::

    django-admin startproject mysite
    mv selenium-server-standalone-2.6.0.jar mysite/
    cd mysite
    ./manage.py startapp polls


Django stores project-wide settings in a file called ``settings.py``. One of the key
settings is what kind of database to use.  We'll use the easiest possible, sqlite.

Find settings ``settings.py`` in the root of the new ``mysite`` folder, and
open it up in your favourite text editor. Find the lines that mention ``DATABASES``,
and change them, like so::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'database.sqlite',                      # Or path to database file if using sqlite3.


<pic>

Setting up the functional test runner
-------------------------------------

The next thing we need is a single command that will run all our FT's, as well
as a folder to keep them all in::

    mkdir fts
    touch fts/__init__.py

Here's one I made earlier... A little Python script that'll run all your tests
for you.::

    wget -O functional_tests.py https://raw.github.com/hjwp/Test-Driven-Django-Tutorial/master/functional_tests.py
    chmod +x functional_tests.py


Our first test: The django admin
--------------------------------

In the test-driven methodology, we tend to group functionality up into
bite-size chunks, and write functional tests for each one of them. You
can describe the chunks of functionality as "user stories", if you like,
and each user story tends to have a set of tests associated with it,
and the tests track the potential behaviour of a user.


We have to go all the way to the second page of the django tutorial to see an
actual user-visible part of the application:  the `django admin site`.  The 
django admin site is a really useful part of Django, which generates a UI
for site administrators to manage key bits of information in your database:
user accounts, permissions groups, and, in our case, polls.  The admin site
will let admin users create new polls, enter their descriptive text and start
and end dates and so on, before they are published via the user-facing website.

All this stuff comes 'for free' and automatically, just using the django admin
site.  

<link>

So, our first user story is that the user should be able to log into the django
admin site using an admin username and password, and create a new poll.

<pic>

Let's open up a file inside the ``fts`` directory called
``test_polls_admin.py`` and enter the code below.

Note the nice, descriptive names for the test functions, and the comments,
which describe in human-readable text the actions that our user will take.
Mhhhh, descriptive names.....

It's always nice to give the user a name... Mine is called Gertrude...::

    from functional_tests import FunctionalTest, ROOT

    class TestPollsAdmin(FunctionalTest):

        def test_can_create_new_poll_via_admin_site(self):

            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(ROOT + '/admin/')

            # She sees the familiar 'Django Administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django Administration', body.text)

            # She sees a hyperlink that says "Polls"
            polls_link = self.browser.find_element_by_link_text('Polls')

            # So, she clicks it
            polls_link.click()

            # She is taken to a new page on which she sees a link to "Add poll"
            new_poll_link = self.browser.find_element_by_link_text('Add poll')

            # So she clicks that too
            new_poll_link.click()

            <to be added - creating new poll, with dates etc>



Let's try running our first test::
    ./functional_tests.py

<pic>

The test output will looks something like this::

    Starting Selenium
    selenium started
    starting django test server
    django test server running
    running tests
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (test_polls_admin.TestPollsAdmin)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/test_polls_admin.py", line 12, in test_can_create_new_poll_via_admin_site
        self.assertIn('Django Administration', body.text)
    AssertionError: 'Django Administration' not found in u"It worked!\nCongratulations on your first Django-powered page.\nOf course, you haven't actually done any work yet. Here's what to do next:\nIf you plan to use a database, edit the DATABASES setting in mysite/settings.py.\nStart your first app by running python mysite/manage.py startapp [appname].\nYou're seeing this message because you have DEBUG = True in your Django settings file and you haven't configured any URLs. Get to work!"

    ----------------------------------------------------------------------
    Ran 1 test in 4.754s

    FAILED (failures=1)


First few steps...
------------------

So, let's start trying to get our test to pass... or at least get a little
further on.  We'll need to set up the django admin site.  This is on
page two of the official django tutorial::

    * Add "django.contrib.admin" to your INSTALLED_APPS setting.

    * Run python manage.py syncdb. Since you have added a new application to
      INSTALLED_APPS, the database tables need to be updated.

    * Edit your mysite/urls.py file and uncomment the lines that reference the
      admin

When we run the syncdb, we'll need to enter a username and password. Let's use
the ultra-secure  ``admin`` and ``adm1n``.

In our ``urls.py``, we'll be looking to uncomment these two lines::

    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('',
        # [...]
        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )

Let's re-run our tests.  We should find they get a little further::

    ./functional_tests.py
    ======================================================================
    ERROR: test_can_create_new_poll_via_admin_site (test_polls_admin.TestPollsAdmin)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/test_polls_admin.py", line 24, in test_can_create_new_poll_via_admin_site
        polls_link = self.browser.find_element_by_link_text('Polls')
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 208, in find_element_by_link_text
        return self.find_element(by=By.LINK_TEXT, value=link_text)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 525, in find_element
        {'using': by, 'value': value})['value']
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 144, in execute
        self.error_handler.check_response(response)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/errorhandler.py", line 118, in check_response
        raise exception_class(message, screen, stacktrace)
    NoSuchElementException: Message: u'Unable to locate element: {"method":"link text","selector":"Polls"}' 

    ----------------------------------------------------------------------
    Ran 1 test in 10.203s

Well, the test is happy that there's a django admin site, and it can log in fine,
but it can't find a link to administer "Polls".  So next we need to create our
Polls object.


Our first unit tests
--------------------

The django unit test runner will automatically run any tests we put in
``tests.py``.  Later on, we might decide we want to put our tests somewhere
else, but for now, let's use that file::

    from django.test import TestCase
    from polls.models import Poll

    class TestPollsModel(TestCase):
        def test_creating_a_new_poll_and_saving_it_to_the_database(self):
            # start by creating a new Poll object with its "question" set
            poll = Poll()
            poll.question = "What's up?"

            # check we can save it to the database
            poll.save()

            # check we can adjust its publication date
            poll.pub_date = datetime.datetime(2012, 12, 25)
            poll.save()

            # now check we can find it in the database again
            all_polls_in_database = Poll.objects.all()
            self.assertEquals(len(all_polls_in_database), 1)
            only_poll_in_database = all_polls_in_database[0]
            self.assertEquals(only_poll_in_database, poll)

            # and check that it's saved its two attributes: question and pub_date
            self.assertEquals(only_poll_in_database.question, "What's up?")
            self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)


Unit tests are designed to check that the individual parts of our code work
the way we want them too.  Aside from being useful as tests, they're useful
to help us think about the way we design our code... It forces us to think 
about how things are going to work, from a slightly external point of view.

Here we're creating a new Poll object, and checking that we can save it to 
the database, as well as checking that we can set and store a Poll's main two
attributes: the question and the publication date.

    ./manage.py test

You should see an error like this::

      File "/usr/local/lib/python2.7/dist-packages/django/test/simple.py", line 35, in get_tests
        test_module = __import__('.'.join(app_path + [TEST_MODULE]), {}, {}, TEST_MODULE)
      File "/home/harry/workspace/mysite/polls/tests.py", line 2, in <module>
        from polls.models import Poll
      ImportError: cannot import name Poll

Not the most interesting of test errors - we need to create a Poll object for the
test to import.  In TDD, once we've got a test that fails, we're finally allowed
to write some "real" code.  But only the minimum required to get the tests to get 
a tiny bit further on!

So let's create a minimal Poll class, in ``polls/models.py``::

    from django.db import models

    class Poll(object):
        pass 

And re-run the tests.  Pretty soon you'll get into the rhythm of TDD - run the
tests, change a tiny bit of code, check the tests again, see what tiny bit of
code to write next. Run the tests...::

    Creating test database for alias 'default'...
    ........................................................................................................................................................................................................................................................................E..........................................................
    ======================================================================
    ERROR: test_creating_a_poll (polls.tests.TestPollsModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 8, in test_creating_a_poll
        self.assertEquals(poll.name, '')
    AttributeError: 'Poll' object has no attribute 'save'

    ----------------------------------------------------------------------
    Ran 323 tests in 2.504s

    FAILED (errors=1)
    Destroying test database for alias 'default'...


Right, the tests are telling us that we can't "save" our Poll.  That's because
it's not a django model object.  Let's make the minimal change required to get 
our tests further on::

    class Poll(models.Model):
        pass


Running the tests again, we should see a slight change to the error message::

    ======================================================================
    ERROR: test_creating_a_new_poll_and_saving_it_to_the_database (polls.tests.TestPollsModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 26, in test_creating_a_new_poll_and_saving_it_to_the_database
        self.assertEquals(only_poll_in_database.question, "What's up?")
    AttributeError: 'Poll' object has no attribute 'question'

----------------------------------------------------------------------


Notice that the tests have got all the way through to line 26, where we retrieve
the object back out of the database, and it's telling us that we haven't saved the
question attribute.  Let's fix that::

    class Poll(models.Model):
        question = models.CharField(max_length=200)

(note on max_length=200)?

Now our tests get slightly further - they tell us we need to add a pub_date::

    ======================================================================
    ERROR: test_creating_a_new_poll_and_saving_it_to_the_database (polls.tests.TestPollsModel)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 27, in test_creating_a_new_poll_and_saving_it_to_the_database
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
    AttributeError: 'Poll' object has no attribute 'pub_date'
    ----------------------------------------------------------------------

Let's add that too::

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField()


And run the tests again::

    ...................................................................................................................................................................................................................................................................................................................................
    ----------------------------------------------------------------------
    Ran 323 tests in 2.402s

    OK


Hooray!  The joy of that unbroken string of dots!  That lovely, understated "OK".
Does this mean our functional test will pass?::



    NoSuchElementException: Message: u'Unable to locate element: {"method":"link text","selector":"Polls"}' 


<syncdb!>


Ah, not quite.  We still need to add the "Poll" model to the django admin site.
To do that, we just need to create a file called ``admin.py`` to the ``polls``
directory, with the following three lines::

    from polls.models import Poll
    from django.contrib import admin

    admin.site.register(Poll)



LINKS
=====

https://docs.djangoproject.com/en/dev/intro/tutorial02/

http://pypi.python.org/pypi/selenium

http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py

http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webelement.py

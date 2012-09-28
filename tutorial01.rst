What's the approach?
--------------------

Test-First!  So, before we're allowed to write any real production code, we
write some tests.  We start by writing some browser tests - what I call
`functional` tests, which simulate what an actual user would see and do.  We'll
use `Selenium`, a test tool which actually opens up a real web browser, and
then drives it like a real user, clicking on links and buttons, and checking
what is shown on the screen.  These are the tests that will tell us whether or
not our application behaves the way we want it to, from the user's point of
view.

Once we've written our functional tests (which, incidentally, have forced us to
think through the way our application will work, from the point of view of the
user - never a bad thing...) we can start to think about how we want to
implement that functionality from a technical point of view.

Thankfully we won't have to do too much difficult thinking, because the
functional tests will be our guide - what do we have to do to get the
functional tests to get a bit further towards passing?  How would we implement
that? 

Once we've settled on the function or the class that will solve our first
problem, we can write a unit test for it.  Again, it forces us to think about
how it will work from the outside, before we write it.


What do we want to achieve in part 1?
-------------------------------------

In general with TDD, whenever we want to do something, we also ask ourselves
"how will I know when I've succeeded" - and the answer is usually - a test!

So here are our objectives for this first tutorial:

=========================================    ==================================
Objective                                    How will we know we've succeeded?
=========================================    ==================================
Set up Django                                Run the *Django development server* 
                                             and manually browse the default
                                             "Hello World" page
-----------------------------------------    ----------------------------------
Set up the Django admin site                 Write our first *functional test*,
                                             which logs into the admin site
-----------------------------------------    ----------------------------------
Create our first model for "Poll" objects    Extend our functional test to
                                             create a new Poll via the
                                             admin site. Write *unit tests*
=========================================    ==================================


Some setup before we start
--------------------------

For functional testing, we'll be using the excellent Selenium.  Let's install
that, and Django, and a couple of other Python modules we might need::

    pip install django
    pip install selenium
    pip install mock
    pip install unittest2 # (only if using Python 2.6)

If you don't know what ``pip`` is, you'll need to find out, and install it.
It's a must-have for working with Python.

At this point, you should be able to open up a command line, and type
``python`` to get the Python interpreter running, and from in there you should
be able to ``import django`` and ``import selenium`` without any errors.  If
any of that gives you problems, take a look at:
https://docs.djangoproject.com/en/1.4/intro/install/


Setting up our Django project
-----------------------------

Django structures websites as "projects", each of which can have several
constituent "apps"... Ostensibly, the idea is that apps can be self-contained,
so that you could use one app in several projects... Well, I've never actually
seen that done, but it remains a nice way of splitting up your code.

So let's start by creating our `project`, which we'll call "mysite". Django has
a command-line tool for this::

    django-admin startproject mysite


If you're on windows, you may need to type ``django-admin.py startproject
mysite``. If you have any problems, you can take a look at the tips on 
https://docs.djangoproject.com/en/1.4/intro/tutorial01/#creating-a-project

This will create a folder called ``mysite`` to hold your project, and another
folder within that also called ``mysite``.  It will also set up a few key
django files, including ``manage.py`` which will let you run some
administration tools for your site, and ``settings.py``, which will hold
configuration information about your site::

    `-- mysite
        |-- manage.py
        `-- mysite
            |-- __init__.py
            |-- settings.py
            |-- urls.py
            `-- wsgi.py

    
*(NB - on Django 1.3 and earlier, ``startproject`` would only create a single
``mysite`` folder, which would contain both ``manage.py`` and ``settings.py``.
This tutorial is written for 1.4 -- bleeding edge FTW! -- but if you're stuck
with an earlier version, you should find most things work with a little
tweaking, as long as you get yourself a hold of a LiveServerTestCase backport)*

Checking we've succeeded: running the development server
--------------------------------------------------------

Django comes with a built-in development server which you can fire up during
development to take a peek at how things are looking. You can start it up by
typing::

    cd mysite
    python manage.py runserver

If you then fire up your web browser and go to http://127.0.0.1:8000, you
should see something a bit like this:

.. image:: /static/images/django_it_worked_default_page.png

There's more information about the development server here:
https://docs.djangoproject.com/en/1.4/intro/tutorial01/#the-development-server

Now, manual tests like the one we've just done are all very well, but in TDD
they're exactly what we're tring to avoid!  Our next objective is to set up an
automated test.

I did want to introduce ``runserver`` at the outset though - that way, at any
point during this tutorial, if you want to check what the site actually looks
like, you can always fire up the development server and have a look around


Starting our first functional test: The Django admin site
=========================================================

In this section, we're going to do several things:

    * create our first FT

    * setup our database using ``settings.py``

    * switch on django admin 

    * create an admin user account


Let's start with the FT. In the test-driven methodology, we tend to group
functionality up into bite-size chunks, and write functional tests for each one
of them. You can describe the chunks of functionality as "user stories", if you
like, and each user story tends to have a set of tests associated with it, and
the tests track the potential behaviour of a user.

We have to go all the way to the second page of the Django tutorial to see an
actual user-visible part of the application:  the *Django admin site*.  The
admin site is a really useful part of Django, which generates a UI for site
administrators to manage key bits of information in your database: user
accounts, permissions groups, and, in our case, polls.  The admin site will let
admin users create new polls, enter their descriptive text and start and end
dates and so on, before they are published via the user-facing websiteke. All
this stuff comes 'for free' and automatically, just using the Django admin
site.

You can find out more about the philosophy behind the admin site, including
Django's background in the newspaper industry, here:

https://docs.djangoproject.com/en/1.4/intro/tutorial02/

So, our first user story is that the user should be able to log into the Django
admin site using an admin username and password, and create a new poll.  Here's
a couple of screenshots of what the admin site looks like:

.. image:: /static/images/admin03t.png

.. image:: /static/images/admin05t.png


We'll add more to this test later, but for now let's just get it to do the
absolute minimum:  we want the test to open up the admin site (which we want to
be available via the url ``/admin/``), and see that it "looks OK" - for this,
we'll check that the page contains the words *Django administration*, which it
does by default.

Let's create an app for our functional tests.  It's a matter of preference
whether you keep your FTs in a separate app or in the same app as your source
code, I like to keep them separate firstly so that FTs and unit tests are easy
to run separately, and secondly because FTs are meant to test the whole
application, which may well mean that a single FT uses functionality provided
by several different apps.

Run the following command::

    python manage.py startapp fts

Your directory tree will now look like this::

    mysite
    |-- fts
    |   |-- __init__.py
    |   |-- models.py
    |   |-- tests.py
    |   `-- views.py
    |-- manage.py
    `-- mysite
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        `-- wsgi.py


Now, let's open up the ``fts/tests.py`` file (inside the ``fts`` folder), and
write our first Functional test.  You can delete the example test case that
Django have put in there, and replace it with this:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # She sees the familiar 'Django administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # TODO: use the admin site to create a Poll
            self.fail('finish this test')

Functional tests are grouped into classes, and each test is a method inside the
class.  The special rule is that test methods must begin with a ``test_``.

Note the nice, descriptive names for the test function, and the comments, which
describe in human-readable text the actions that our user will take. Mhhhh,
descriptive names.....

We use a ``LiveServerTestCase`` which is a new test case provided by Django
1.4, which starts up a test web server with our Django site on it, in a
separate thread, for the tests to run against.

The special methods ``setUp`` and ``tearDown`` are executed before and after
each test. We're using them to start up and shut down our Selenium WebDriver
browser instance.

The ``implicitly_wait`` call tells webdriver to use a 3-second timeout when
performing its actions - it doesn't slow things down though, because it's a
maximum timeout: if Selenium can tell that the page has loaded and any
javascript processing is done, it will move on before the end..


Aside from that, there are 3 lines of test code here:

.. sourcecode:: python

    self.browser.get(self.live_server_url + '/admin/')

``self.browser`` is the selenium object which represents the web browser, aka
the ``WebDriver``. 

``.get`` is tells the browser to go to a new page, and we pass it the url,
which is made up of ``self.live_server_url``, which is set up for us by
``LiveServerTestCase``, and then we tack on the ``/admin/`` url to get to the
admin site.


Next we use

.. sourcecode:: python

    body = self.browser.find_element_by_tag_name('body') 

``find_element_by_tag_name``, which tells Selenium to look through the page and
find the HTML element for a particular tag - in this case, ``body``, which
means the whole of the visible part of the page.  The method returns an
``WebElement`` object, which represents the HTML element.

Finally, we get to an assertion - where we say what we expect, and the test
should pass or fail at this point:

.. sourcecode:: python

    self.assertIn('Django administration', body.text)

This is equivalent to doing

.. sourcecode:: python

    assert 'Django administration' in body.text

but we use the ``unittest`` method on ``self.`` because it will give us a more
helpful error message.

The ``body`` WebElement object's ``.text`` attribute essentially gives us all
of the visible text on the rendered page - stripping out all the HTML markup.

You can find out more about ``WebDriver`` and ``WebElement`` in the Selenium
documentation (choose Python as your language for the examples), or just by
looking at the source code:

http://seleniumhq.org/docs/03_webdriver.html

http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py

At the end, I've left a ``TODO`` - calling ``self.fail()`` means the test will
always fail at the end there, so that will be a reminder that we're not quite
finished.

Oh, and one las thing: it's always nice to give the user a name... Mine is
called Gertrude!


First functional test run
-------------------------

Let's try running our functional tests::

    python manage.py test fts

And you should see something like this::

    python manage.py test fts
    Traceback (most recent call last):
      File "manage.py", line 10, in <module>
        execute_from_command_line(sys.argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 443, in execute_from_command_line
        utility.execute()
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 382, in execute
        self.fetch_command(subcommand).run_from_argv(self.argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/commands/test.py", line 49, in run_from_argv
        super(Command, self).run_from_argv(argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 196, in run_from_argv
        self.execute(*args, **options.__dict__)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 232, in execute
        output = self.handle(*args, **options)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/commands/test.py", line 72, in handle
        failures = test_runner.run_tests(test_labels)
      File "/usr/local/lib/python2.7/dist-packages/django/test/simple.py", line 380, in run_tests
        suite = self.build_suite(test_labels, extra_tests)
      File "/usr/local/lib/python2.7/dist-packages/django/test/simple.py", line 263, in build_suite
        app = get_app(label)
      File "/usr/local/lib/python2.7/dist-packages/django/db/models/loading.py", line 152, in get_app
        raise ImproperlyConfigured("App with label %s could not be found" % app_label)
    django.core.exceptions.ImproperlyConfigured: App with label fts could not be found

Whenever you add a new app to your project, you have to tell Django that you
really meant it, and that you want this app to be a part of your site.  We do
this in ``settings.py``


settings.py - adding our fts app and setting up the database
------------------------------------------------------------

Django stores project-wide settings in a file called ``settings.py``, and that
includes which apps we want to be active.  Let's edit it now, and find the
``INSTALLED_APPS`` part.  We need to add ``'fts',``:


.. sourcecode:: python

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        # Uncomment the next line to enable the admin:
        # 'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
        'fts',
    )

Let's try running our fts again::

    $ python manage.py test fts

    Creating test database for alias 'default'...
    Traceback (most recent call last):
      File "manage.py", line 10, in <module>
        execute_from_command_line(sys.argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 443, in execute_from_command_line
        utility.execute()
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 382, in execute
        self.fetch_command(subcommand).run_from_argv(self.argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/commands/test.py", line 49, in run_from_argv
        super(Command, self).run_from_argv(argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 196, in run_from_argv
        self.execute(*args, **options.__dict__)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/base.py", line 232, in execute
        output = self.handle(*args, **options)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/commands/test.py", line 72, in handle
        failures = test_runner.run_tests(test_labels)
      File "/usr/local/lib/python2.7/dist-packages/django/test/simple.py", line 381, in run_tests
        old_config = self.setup_databases()
      File "/usr/local/lib/python2.7/dist-packages/django/test/simple.py", line 317, in setup_databases
        self.verbosity, autoclobber=not self.interactive)
      File "/usr/local/lib/python2.7/dist-packages/django/db/backends/creation.py", line 256, in create_test_db
        self._create_test_db(verbosity, autoclobber)
      File "/usr/local/lib/python2.7/dist-packages/django/db/backends/creation.py", line 321, in _create_test_db
        cursor = self.connection.cursor()
      File "/usr/local/lib/python2.7/dist-packages/django/db/backends/dummy/base.py", line 15, in complain
        raise ImproperlyConfigured("settings.DATABASES is improperly configured. "
    django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured. Please supply the ENGINE value. Check settings documentation for more details.


A reasonably helpful error message!  Let's open up ``settings.py`` again, and
set up a database. We'll use the easiest possible, *SQLite*. Find the lines
that mention ``DATABASES``, and change the setting for ``ENGINE`` and ``NAME``,
like so:

.. sourcecode:: python
    :filename: mysite/mysite/settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 
            'NAME': 'database.sqlite',


You can find out more about projects, apps and ``settings.py`` here:
https://docs.djangoproject.com/en/1.4/intro/tutorial01/#database-setup

Let's see if it worked by trying to run the functional tests again::

    python manage.py test fts

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 20, in test_can_create_new_poll_via_admin_site
        self.assertIn('Django administration', body.text)
    AssertionError: 'Django administration' not found in u'A server error occurred.  Please contact the administrator.'

    ----------------------------------------------------------------------
    Ran 1 test in 2.622s

Hooray - I know it says "Fail", but that's still better than the last test
runner, which just had an error.  In fact, this is what you'd call an "expected
failure" - our FT is checking that the url ``/admin/`` produces the django
admin page (by looking for the words "Django Administration", but instead it's
just seeing an error.  That' because we haven't finished setting up the admin
site yet.

Incidentally, as you run these test, you will probably see a bunch of
tracebacks saying something like this::

      [...]
      File "/usr/local/lib/python2.7/dist-packages/django/template/loader.py", line 145, in get_template
        template, origin = find_template(template_name)
      File "/usr/local/lib/python2.7/dist-packages/django/template/loader.py", line 138, in find_template
        raise TemplateDoesNotExist(name)
      TemplateDoesNotExist: 500.html

It's OK to ignore these for now - we'll deal with templates for 500 errors in a
later tutorial.

Switching on the admin site
---------------------------

This is described on page two of the official Django tutorial:

https://docs.djangoproject.com/en/1.4/intro/tutorial02/#activate-the-admin-site

We need to edit two files: ``settings.py`` and ``urls.py``.  In both cases,
Django has some helpful comments in those files by default, and all we need to
do is uncoment a couple of lines.

First, in ``settings.py`` we add ``django.contrib.admin`` to ``INSTALLED_APPS``:

.. sourcecode:: python
    :filename: mysite/mysite/settings.py

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
        'fts',
    )

And in ``urls.py``, we uncomment three lines that mention the admin site - two
near the top, and one near the bottom

.. sourcecode:: python
    :filename: mysite/mysite/urls.py

    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('',
        # [...]
        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )

Let's see if it worked!  Try running the functional tests again::

    $ python manage.py test fts

    Creating tables ...
    Installing custom SQL ...
    Installing indexes ...
    No fixtures found.
    running tests
    No fixtures found.
    Validating models...

    0 errors found
    Django version 1.4, using settings 'settings_for_fts'
    Development server is running at http://localhost:8001/
    Quit the server with CONTROL-C.
    [28/Nov/2011 04:00:28] "GET /admin/ HTTP/1.1" 200 2028

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/tmp/mysite/fts/tests.py", line 16, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test')
    AssertionError: finish this test

    ----------------------------------------------------------------------

Hooray! The tests got to the end, just leaving us with our "TODO".  Still, I
imagine you're thinking it doesn't feel quite real?  Just to reassure ourselves
then, maybe it would be nice to take a look around manually.

Taking another look around
--------------------------

Let's fire up the Django dev server using ``runserver``, and have a look; aside
from anything else, it should give us some inspiration on the next steps to
take for our site.::

    python manage.py runserver

If you take another look at ``http://localhost/``, you will probably see an
error message like this:

.. image:: /static/images/page_not_found_debug_error.png


Now that we've switched on the admin site, Django no longer serves its default
"it worked" page.  It will give us helpful error messages (while we leave
``DEBUG = True`` in settings.py), and this one is telling us that the only
active url on the site is ``/admin/``.

So let's go there instead - point your browser towards
``http://localhost/admin/``, and you should see a slightly different error
message

.. image:: /static/images/no_such_table_error.png


Django is telling us that there's a missing table in the database.  The
solution to this sort of error is usually a ``syncdb``.


Setting up the database with ``syncdb``
---------------------------------------

The database needs a bit more setting up -- so far we gave it a name in
``settings.py``, but we also need to tell Django to create all the tables it
needs. For this we use a command named ``syncdb``.

In this case, syncdb will notice it's the first run, and proposes that you
create a superuser.  Let's go ahead and do that (you may have to hit Ctrl-C to
quit the development server first)::

    python manage.py syncdb

Let's use the ultra-secure  ``admin`` and ``adm1n`` as our username and
password for the superuser.:::

    $ python manage.py syncdb
    Username (Leave blank to use 'harry'): admin
    E-mail address: admin@example.com
    Password: 
    Password (again): 
    Superuser created successfully.
     

Let's see if that worked - try firing up the development server again::

    python manage.py runserver

And if you go back to ``http://localhost/admin/``, you should see the Django
login screen:

.. image:: /static/images/django_admin_login.png

And if you try logging in with the username and password we set up earlier
(``admin`` and ``adm1n``), you should be taken to the main Django admin page

.. image:: /static/images/django_admin_logged_in.png

By default, the admin site lets you manage users (like the ``admin`` user we
set up just now), as well as Groups and Sites (no need to worry about those for
now).

Having a look around manually is useful, because it helps us decide what we
want next in our FT.  This is particularly true when you're working with
external tools, rather than with parts of the website you've written entirely
yourself.

We want to use the django admin site to manage the polls in our polls app.
Basically, "Polls" should be one of the options, maybe just below Users,
Groups, and Sites.

If you hover over the blue headers, you'll see that "Auth" and "Sites" are both
hyperlinks.  "Groups", "Users" and the second "Sites" are also hyperlinks.  So,
we'll want to add a section for "Polls", and within that there should be
another link to "Polls".  Let's add that to our FT.

Extending the FT to login and look for Polls
--------------------------------------------

So, we now want our FT to cover logging into the admin site, and checking that
"Polls" is an option on the main page:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # She sees the familiar 'Django administration' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Django administration', body.text)

            # She types in her username and passwords and hits return
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('admin')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('adm1n')
            password_field.send_keys(Keys.RETURN)

            # her username and password are accepted, and she is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Site administration', body.text)

            # She now sees a couple of hyperlink that says "Polls"
            polls_links = self.browser.find_elements_by_link_text('Polls')
            self.assertEquals(len(polls_links), 2)

            # TODO: Gertrude uses the admin site to create a new Poll
            self.fail('todo: finish tests')


Don't miss the extra ``import`` at the top there - we need the special ``Keys``
class to send a carriage return to the password field.

We're using a couple of new test methods here...

    * ``find_elements_by_name`` which is most useful for form input fields,
      which it locates by using the ``name="xyz"`` HTML attribute

    * ``send_keys`` - which sends keystrokes, as if the user was typing
      something (notice also the ``Keys.RETURN``, which sends an enter key-
      there are lots of other options inside ``Keys``, like tabs, modifier keys
      etc

    * ``find_elements_by_link_text`` - notice the **s** on ``elements``; this
      method returns a *list* of WebElements.


Let's try running the FT again and seeing how far it gets::

    python manage.py test fts
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 33, in test_can_create_new_poll_via_admin_site
        self.assertIn('Site administration', body.text)
    AssertionError: 'Site administration' not found in u'Django administration\nPlease enter the correct username and password for a staff account. Note that both fields are case-sensitive.\nUsername:\nPassword:\n '

    ----------------------------------------------------------------------
    Ran 1 test in 10.203s

The username and password didn't work - you might think that's strange, because
we literally just set them up during the ``syncdb``, but the reason is that the
Django test runner actually creates a *separate* database to run tests against
- this saves your test runs from interfering with production data.

Creating a test fixture
-----------------------

So we need a way to set up an admin user account in the test database.
Thankfully, Django has the concept of *fixtures*, which are a way of loading
data into the database from text files.

We can save the admin account using the django ``dumpdata`` command, and put
them into a folder called ``fixtures`` in our ``fts`` app.::

    mkdir fts/fixtures
    python manage.py dumpdata auth.User --indent=2 > fts/fixtures/admin_user.json

You can take a look at the file if you like -- it's a JSON representation of
the user account.

Now we need to tell our tests to load this fixture. That happens via an
attribute called ``fixtures`` on the test class:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    class PollsTest(LiveServerTestCase):
        fixtures = ['admin_user.json']

        def setUp(self):
            [...]

You can find out more about fixtures here:
https://docs.djangoproject.com/en/1.4/topics/testing/#fixture-loading

Let's try again::

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 37, in test_can_create_new_poll_via_admin_site
        self.assertEquals(len(polls_links), 2)
    AssertionError: 0 != 2

    ----------------------------------------------------------------------
    Ran 1 test in 3.069s

    FAILED (failures=1)
    Destroying test database for alias 'default'...


Now the test is happy that there's a Django admin site, and it can log in fine,
but it can't find any links to administer "Polls".  

The polls application, our first Django model and unit tests
============================================================

In this next section, we're going to create a new Django *"app"* for our Polls,
as well as a new ``Poll`` class to represent our poll objects in the database.
We'll also be writing our first unit tests.::

    python manage.py startapp polls

Your directory tree should now look like this::

    mysite
    |-- database.sqlite
    |-- fts
    |   |-- fixtures
    |   |   `-- admin_user.json
    |   |-- __init__.py
    |   |-- models.py
    |   |-- tests.py
    |   `-- views.py
    |-- manage.py
    |-- mysite
    |   |-- __init__.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    `-- polls
        |-- __init__.py
        |-- models.py
        |-- tests.py
        `-- views.py


The next thing we need to do is tell Django that, yes, we really meant it, and
would it please take notice of this new polls app and assume we want to use it
- we do this by adding it to ``INSTALLED_APPS`` in ``settings.py``:

.. sourcecode:: python
    :filename: mysite/mysite/settings.py

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
        'fts',
        'polls',
    )


Then we need to create the representation of a Poll inside Django - a *model*,
in Django terms.


Our first unit tests: testing a new "Poll" model
================================================

The tests for the polls app are in ``polls/tests.py``. Again, you can delete
the example test that Django put in there.  In this test, we'll create a Poll
and save it to the database, then retrieve it again to check the poll was saved
properly.  You'll notice that in this test we don't use Selenium, instead we
interact with our application at a much lower level.

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    from django.test import TestCase
    from django.utils import timezone
    from polls.models import Poll

    class PollModelTest(TestCase):
        def test_creating_a_new_poll_and_saving_it_to_the_database(self):
            # start by creating a new Poll object with its "question" set
            poll = Poll()
            poll.question = "What's up?"
            poll.pub_date = timezone.now()

            # check we can save it to the database
            poll.save()

            # now check we can find it in the database again
            all_polls_in_database = Poll.objects.all()
            self.assertEquals(len(all_polls_in_database), 1)
            only_poll_in_database = all_polls_in_database[0]
            self.assertEquals(only_poll_in_database, poll)

            # and check that it's saved its two attributes: question and pub_date
            self.assertEquals(only_poll_in_database.question, "What's up?")
            self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)


Whereas functional tests are meant to test how the whole system behaves, from
the point of view of a user, unit test are meant to check that the individual
parts of our code work the way we want them to.  Unit tests are much more
granular, and they typically test individual functions or classes.

Aside from being useful as tests, in the TDD philosophy writing unit tests also
helps us because it forces us to do some design before we start to code. That's
because when we write test, we have to think about the function or class we're
about to write *from the outside* - in terms of its API, and its desired
behaviour.  Often when you find yourself struggling to write tests, finding
things long winded, it's an indication that the design of your code isn't quite
right...


The django ORM - model classes
------------------------------

If you've never worked with Django, this test will also be your first
introduction to the Django `ORM` - the API for working with database objects in
Django. 

You can see that everything revolves around ``Poll``, which is a class that
represents our polls, which we import from ``models.py``.  Usually a model
class corresponds to a single table in the database.

In the test we creating a new "Poll" object, and then we set some of its
attributes: ``question`` and ``pub_date``. The object corresponds to a row in
the database, and the attributes are the values for the table's columns.

Finally, we call ``save()``, which actually INSERTs the object into the
database.

Later on, you can also see how we look up existing objects from the database
using a special classmethod, ``Poll.objects``, which lets us run queries
against the database.  We've used the simplest possible query, ``.all()``, but
all sorts of other options are available, and Django's API is very helpful and
intuitive.  You can find out more at:

https://docs.djangoproject.com/en/1.4/intro/tutorial01/#playing-with-the-api

The unit-test / code cycle
--------------------------

Let's run the unit tests.::

    python manage.py test polls

You should see an error like this::

      [...]
      File "/usr/local/lib/python2.7/dist-packages/Django/test/simple.py", line 35, in get_tests
        test_module = __import__('.'.join(app_path + [TEST_MODULE]), {}, {}, TEST_MODULE)
      File "/home/harry/workspace/mysite/polls/tests.py", line 2, in <module>
        from polls.models import Poll
      ImportError: cannot import name Poll

Not the most interesting of test errors - we need to create a Poll object for
the test to import.  In TDD, once we've got a test that fails, we're finally
allowed to write some "real" code.  But only the minimum required to get the
tests to get a tiny bit further on!

So let's create a minimal Poll class, in ``polls/models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py
    

    from django.db import models

    class Poll(object):
        pass 

And re-run the tests.  Pretty soon you'll get into the rhythm of TDD - run the
tests, change a tiny bit of code, check the tests again, see what tiny bit of
code to write next. Run the tests...::

    ======================================================================
    ERROR: test_creating_a_poll (polls.tests.PollModelTest)
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
it's not a Django model object.  Let's make the minimal change required to get
our tests further on

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        pass

Inheriting from Django's ``Model`` class will give us the ``save()`` method.
Running the tests again, we should see a slight change to the error message::

    ======================================================================
    ERROR: test_creating_a_new_poll_and_saving_it_to_the_database (polls.tests.PollModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 26, in test_creating_a_new_poll_and_saving_it_to_the_database
        self.assertEquals(only_poll_in_database.question, "What's up?")
    AttributeError: 'Poll' object has no attribute 'question'

    ----------------------------------------------------------------------

Notice that the tests have got all the way through to line 26, where we
retrieve the object back out of the database, and it's telling us that we
haven't saved the question attribute.  Let's fix that, by telling Django that
we want polls to have an attribute called "question".

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        question = models.CharField(max_length=200)


The `question` attribute will be translated into a column in the databse.  We
use a type of ``models.CharField`` because we want to store a string of
characters.  Django has lots more field types for different data types, see the
full list here:
https://docs.djangoproject.com/en/1.4/ref/models/fields/#field-types

*(Exercise for the reader:  Did you notice we haven't got an explicit test for*
``max_length`` *? It's because it's not entirely straightforward to write one.
Once you've been through a few tutorials and are comfortable with unit testing,
why not come back and write one?  Hint: you'll probably need to use*
``full_clean`` *)*

Now our tests get slightly further - they tell us we need to add a pub_date::

    ======================================================================
    ERROR: test_creating_a_new_poll_and_saving_it_to_the_database (polls.tests.PollModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 27, in test_creating_a_new_poll_and_saving_it_to_the_database
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
    AttributeError: 'Poll' object has no attribute 'pub_date'
    ----------------------------------------------------------------------

Let's add that too

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField()


And run the tests again::

    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.402s

    OK


Hooray!  The joy of that unbroken string of dots!  That lovely, understated "OK".

So, we've now created a new model (table) for our database, the Poll, which has two attributes (columns).


Back to the functional tests: registering the model with the admin site
-----------------------------------------------------------------------

So the unit tests all pass. Does this mean our functional test will pass?::

    python manage.py test fts
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 25, in test_can_create_new_poll_via_admin_site
        self.assertEquals(len(polls_links), 2)
    AssertionError: 0 != 2

    ----------------------------------------------------------------------
    Ran 1 test in 10.203s


Ah, not quite.  The Poll app still isn't available via the admin site. 
That's because the Django admin site doesn't automatically contain every model
you define - you need to tell it which models you want to be able to
administer. To do that, we just need to create a new file with the following
three lines inside the polls app called, ``polls/admin.py``:

.. sourcecode:: python
    :filename: mysite/polls/admin.py

    from django.contrib import admin
    from polls.models import Poll

    admin.site.register(Poll)

If you've done everything right, the polls app folder will look like this::

    `-- polls
        |-- admin.py
        |-- __init__.py
        |-- models.py
        |-- tests.py
        `-- views.py


Let's try the FT again...::

    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/tmp/mysite/fts/tests.py", line 28, in test_can_create_new_poll_via_admin_site
        self.fail('todo: finish tests')
    AssertionError: todo: finish tests

    ----------------------------------------------------------------------

Hooray! So far so good. Tune in next week, when we get into customising the
admin site, and using it to create polls.  In the meantime, why not take a look
around the site using the ``runserver`` command, and try creating some Polls of
your own.


LINKS
=====

https://docs.djangoproject.com/en/1.4/intro/tutorial02/

http://seleniumhq.org/docs/03_webdriver.html

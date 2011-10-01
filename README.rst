The Concept
-----------

This idea is to provide an introduction to test-driven web development using
Django.  Essentially, we run through the steps of the official Django tutorial,
but instead of 'just' writing code, we write tests first at each stage - both
"functional tests", in which we actually pretend to be a user, and drive a 
real web browser, as well as "unit tests", which help us to design and 
piece together the individual working parts of the code.


Why Test-Driven Development?
----------------------------

This guide probably isn't the place to evangelise in great detail about the TDD
approach.  Others have done it better, for example here and here.

Suffice to say, you can get away without writing proper tests for your web
application while it's still small.  But the moment it gets to being 
remotely complex... if you don't have tests, then you'll have no way
of knowing whether your application works or not.  With every new change
you make, you'll be terrified that you're about to break other parts of
your code.  Parts of your code will become "no-go" areas, treated with a
sort of voodoo respect.  In short, complexity will make you its bitch.


What's the approach?
--------------------

FTs first
then unit tests
then code

simple commands to run each


Some setup before we start
--------------------------

For functional testing, we'll be using the excellent Selenium
A few python modules we'll need::

    easy_install django
    easy_install selenium
    easy_install pexpect

We also need the selenium java server::

    wget -O selenium-server-standalone-2.6.0.jar http://selenium.googlecode.com/files/selenium-server-standalone-2.6.0.jar 



Setting up our Django project
-----------------------------

We set up a django project, then within that our first application. It will
be a simple application to handle polls, as per the official tutorial.

We use the django command line tools to set up the project and the app. At the
command line::

    django-admin startproject mysite
    mv selenium-server-standalone-2.6.0.jar mysite/
    cd mysite
    ./manage.py startapp polls

Let's set up the easiest possible database - sqlite.  Find the file in mysite
called ``settings.py``, and open it up in your favourite text editor...::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'database.sqlite',                      # Or path to database file if using sqlite3.


<pic>

Setting up the functional test runner
-------------------------------------

The next thing we need is a single command that will run all our FT's, 
and a place to keep them all::

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
actual user-visible part of the application:  the `django admin site`.

So, our first user story is that the user should be able to log into the django
admin site using an admin username and password, and that we can see the
"Polls" application as one of the options.

<pic>

Open up a file inside the ``fts`` directory called ``test_polls_admin.py`` and
enter the code below.

Note the nice, descriptive names for the test functions, and the comments,
which describe in human-readable text the actions that our user will take.

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
the ultra-secure  `admin` and `adm1n`.

In our `urls.py`, we'll be looking to uncomment these two lines::

    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('',
        # [...]
        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )


Our first unit tests
--------------------

The django unit test runner will automatically run any tests we put in
`tests.py`.  Later on, we might decide we want to put our tests somewhere
else, but for now, let's use that file::



Now we can setup the database::
syncdb


LINKS
=====

https://docs.djangoproject.com/en/dev/intro/tutorial02/

http://pypi.python.org/pypi/selenium
http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py
http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webelement.py

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
be a simple application to handle polls.

At the command line::

    django-admin startproject mysite
    cd mysite
    ./manage.py startapp polls

Let's set up the easiest possible database - sqlite.  Find the file in mysite called
settings.py, and open it up in your favourite text editor...::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'database.sqlite',                      # Or path to database file if using sqlite3.


<pic>

Setting up the functional test runner
-------------------------------------

The next thing we need is a single command that will run all our FT's, 
and a place to keep them all::

    mkdir functional_tests
    touch functional_tests/__init__.py

Here's one I made earlier... A little Python script that'll run all your tests
for you.::

    wget -O run_functional_tests.py https://raw.github.com/hjwp/Test-Driven-Django-Tutorial/master/run_functional_tests.py
    chmod +x run_functional_tests.py


Our first test: The django admin
--------------------------------

In our test-driven methodology, what comes first is a "user story" - a description
of our objective, in terms of what the user can do.  We have to go all the way
to the second page of the django tutorial to see an actual user-visible part
of the application:  the django admin site.

So, our first test will just check that the django admin site works, that we
can log into it using an admin username and password, and that we can see the
"Polls" application as one of the options.

<pic>

Open up a file inside the ``functional_tests`` directory called ``test_polls_admin.py``


add test_admin.py


Our first unit tests
--------------------

rm polls/tests.py
mkdir polls/tests
touch polls/tests/__init__.py

from test_models import *

test_models.py
models.py

first test 


Now we can setup the database::
syncdb


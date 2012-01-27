Welcome to part 5 - this week we'll be looking at processing user
input from forms.

Tutorial 5: Processing form submissions
=======================================

Here's the outline of what we're going to do in this tutorial:

    * handle POST requests

    * tbc!


Finishing the FT
----------------

Let's pick up from the ``TODO`` in our FT, and extend it to include viewing the
effects of submitting a vote on a poll. In ``fts/test_polls.py``:

.. sourcecode:: python

        [...] 

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # The page also says "1 vote"
        self.assertIn('1 vote', body_text)

        self.fail('TODO')

We'll leave the "TODO" in, because we'll want to exercise the site a litte
further, to make sure other votes update the counters appropriately.  But let's
see if we can get a single vote working for now.

If you run the FTs, you should see something like this::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/test_polls.py", line 126, in test_voting_on_a_new_poll
        self.assertIn('100 %: Very awesome', body_text)
    AssertionError: '100 %: Very awesome' not found in u'Poll Results\nHow awesome is Test-Driven Development?\nNo-one has voted on this poll yet\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

    ----------------------------------------------------------------------
    Ran 1 test in 5.510s

So, we'll need to wire up our view so that it deals with form submission.  Let's
open up ``tests.py``. We need to find the test that deals with our view.  At
this point, you might find it's getting a little hard to find your way around
``tests.py`` - the file is getting a little cluttered.  I think it's time to
do some *refactoring*, and move things around a bit.

Refactoring the tests
---------------------

Refactoring means making changes to your code that have no functional impact - and
you can refactor your test code as well as your production code.  The purpose of
refactoring is usually to try and make your code more legible, less complex, or 
to make the architecture neater. And the most important thing about refactoring is:
you need to make sure you don't break anything!  That's why having good tests is
absolutely essential to trouble-free refactoring

So, our objective is to separate out our tests.py into separate files for the view
tests, the model tests and the form tests - so that we have a ``test_views.py`` to
match ``views.py``, a ``test_models.py`` to match ``models.py``, and so on.

Let's start by running all our unit tests, making sure they all pass, *and making
a note of how many of them there are* - we don't want to lose any in the process!::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.016s

    OK

Right, 9. Now, although our objective is to move to spreading our tests into 3
different files, we're going to take several small steps to get there.  Then, at
each stage, we can re-run our tests to make sure everything still works.

Now, the way the django test runner works is that it runs all the tests it can find
in each application, in a python module called ``tests``. Currently, that's a file
called ``tests.py``.  But we can make it into a subfolder, by doing this:

    * create a new folder inside ``polls`` called ``tests``

    * add a ``__init__.py`` file inside the ``tests`` folder, to make it into an
      importable Python module

    * move the current ``tests.py`` into the ``tests`` folder

    * finally, ``import`` all of the tests from ``tests.py`` into the ``__init__.py``

Depending on your operating system, that could look something like this::

    mkdir polls/tests
    mv polls/tests.py polls/tests
    touch polls/tests/__init__.py

Then, edit ``polls/tests/__init__.py``, and add the ``import``:

.. sourcecode:: python

    from mysite.polls.tests.tests import *

At this point, we should be able to run the tests again. Let's do so, and check that
exactly the same number of them get run::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.033s

    OK
    Destroying test database for alias 'default'...


Hooray!  Now we have our test in a subfolder, we can start moving them out into 
different files.  Again, we do this step by step.  Let's start by moving all the
model tests into a file called ``test_models.py``.  You'll need to move the 
following classes:

    * ``TestPollsModel``

    * ``TestPollChoicesModel``

The way I chose to do it was:

    * Make a copy of ``tests.py``, and save it as ``test_models.py``

    * Delete all lines after line 81 from ``test_models.py``

    * Delete all lines after line 81 from ``test_models.py``, leaving our two
      model tests

    * The, delete lines 8-81 from ``tests.py``, leaving only non-model tests

    * Finally, tidy up a few unused imports

OK, is the job done?  Let's try re-running our tests::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.014s

    OK

Ah, no - only 4 tests.  We've lost 5 somewhere.  That's because we need to make sure
that we import all tests into the ``tests/__init__.py``

.. sourcecode:: python

    from mysite.polls.tests.tests import *
    from mysite.polls.tests.test_models import *

And now::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.016s

    OK

That's better.  Small, baby steps, with a quick check at each stage that everything 
still works... Now, if you're anything like I was when I was first introduced to this
method, you'll be screaming out, internally  - "Come on!  We could easily just do
all this stuff in one go!"... And, maybe that's even true.  But then, think back to
those times you've started off on a mission to refactor your code, and you've just
dived straight in.  You make a bunch of changes here, and then you move onto that part
there, and then you remember you also wanted to change this thing back here, and then
you just have to copy and paste these bits there, rename this, and while we're
at it we'll just do this and then, oh gosh where was I again?  Pretty soon you find
yourself at the bottom of a depth-first tree, with no idea of how to get back to where
you started, and no idea of what you need to do to get it all working again.

So think back to all those times, and maybe erring on the side of caution isn't so
bad.  Once you get used to it, you'll find you can fly through it!

Anyways - next, let's do the views tests. Here's the way I did it:

  * Save a copy of ``tests.py`` as ``test_views.py``

  * Delete ``TestPollsVoteForm`` from ``test_views.py``

  * Delete ``TestHomePageView`` and ``TestSinglePollView`` from ``tests.py``

  * add ``from mysite.polls.tests.test_views import *`` to ``polls/tests/__init__,py``

  * tidy up imports

Re-running the tests, everything looks ok::

    $ ./manage.py test polls 
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.017s

    OK

And our final step is to rename ``tests.py`` to ``test_forms.py``.  We'll need to
change the import too:

.. sourcecode:: python

    from mysite.polls.tests.test_forms import *
    from mysite.polls.tests.test_models import *
    from mysite.polls.tests.test_views import *

Re-running the tests should give us 9 tests again, and we end up with 3 much more
manageable, shorter files.  Hooray.  

At this stage your polls app should look something like this::

   templates/
        home.html
        poll.html
    tests/
        __init__.py
        test_forms.py
        test_models.py
        test_views.py
    __init__.py
    admin.py
    forms.py
    models.py
    views.py

Pretty neat and tidy!

Let's get back to what we were doing...


Dealing with POST requests in a view
------------------------------------

The normal pattern in Django is to use the view that renders your form for GET
requests, to also process form submissions via POST.  The main reason is that
it makes it easy to show form validation errors to the user...

The Django Test Client can generate POST requests as easily as GET ones, we just
need to tell it what the data should be. Let's write a new test in
``polls/tests/test_views.py``

.. sourcecode:: python



Django puts POST data into a special dictionary on the request object,
``request.POST``.  It also tells us whether a request was a GET or a POST inside
the ``method`` attribute.  That makes it pretty easy to


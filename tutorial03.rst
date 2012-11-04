Part 3 - A normal web page, using Django views and templates
============================================================

Welcome to part 3 of the tutorial!  This week we'll finally get into writing
our own web pages, rather than using the Django Admin site.  Here's a summary
of what we'll get up to:

* Write an FT that views and responds to a Poll

* Create a url, view and template for our site homepage

* Use the Django Test Client to write unit tests for the above


Let's pick up our FT where we left off - we now have the admin site set up to
add Polls, including Choices.  We now want to flesh out what the user sees.

Writing the FT as comments
--------------------------

Let's start by writing out our FT as human-readable comments, which describe
the user's actions, and the expected behaviour of the site

Create a new test method inside ``fts/tests.py``.  

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    def test_can_create_new_poll_via_admin_site(self):
        [...]
        self.assertEquals(len(new_poll_links), 1)

        # Satisfied, she goes back to sleep

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


Setting up data for the test via the admin site
-----------------------------------------------

A nice little test, but that very first comment rather glosses over a lot.
Let's split out the Gertrude bit into its own method, for tidiness, and copy
and paste in some code from the admin test.

You'll see I've changed things slightly, because in the admin test we entered
just one poll and one set of choices, whereas here we're doing several - so
you'll see there's a little loop, and I'm storing the polls' questions and
choices in a couple of namedtuples.  

(*If you've never seen a namedtuple in Python before, you should definitely
look them up! They're a neat way of specificying a structured data type - more
info here:*
http://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python)

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from collections import namedtuple
    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    PollInfo = namedtuple('PollInfo', ['question', 'choices'])
    POLL1 = PollInfo(
        question="How awesome is Test-Driven Development?",
        choices=[
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ],
    )
    POLL2 = PollInfo(
        question="Which workshop treat do you prefer?",
        choices=[
            'Beer',
            'Pizza',
            'The Acquisition of Knowledge',
        ],
    )


    class PollsTest(LiveServerTestCase):
        fixtures = ['admin_user.json']

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Gertrude opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            [...]
            self.assertEquals(len(new_poll_links), 1)

            # Satisfied, she goes back to sleep

        def _setup_polls_via_admin(self):
            # Gertrude logs into the admin site
            self.browser.get(self.live_server_url + '/admin/')
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('admin')
            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('adm1n')
            password_field.send_keys(Keys.RETURN)

            # She has a number of polls to enter.  For each one, she:
            for poll_info in [POLL1, POLL2]:
                # Follows the link to the Polls app, and adds a new Poll
                self.browser.find_elements_by_link_text('Polls')[1].click()
                self.browser.find_element_by_link_text('Add poll').click()

                # Enters its name, and uses the 'today' and 'now' buttons to set
                # the publish date
                question_field = self.browser.find_element_by_name('question')
                question_field.send_keys(poll_info.question)
                self.browser.find_element_by_link_text('Today').click()
                self.browser.find_element_by_link_text('Now').click()

                # Sees she can enter choices for the Poll on this same page,
                # so she does
                for i, choice_text in enumerate(poll_info.choices):
                    choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                    choice_field.send_keys(choice_text)

                # Saves her new poll
                save_button = self.browser.find_element_by_css_selector("input[value='Save']")
                save_button.click()

                # Is returned to the "Polls" listing, where she can see her
                # new poll, listed as a clickable link by its name
                new_poll_links = self.browser.find_elements_by_link_text(
                        poll_info.question
                )
                self.assertEquals(len(new_poll_links), 1)

                # She goes back to the root of the admin site
                self.browser.get(self.live_server_url + '/admin/')

            # She logs out of the admin site
            self.browser.find_element_by_link_text('Log out').click()


        def test_voting_on_a_new_poll(self):
            # First, Gertrude the administrator logs into the admin site and
            # creates a couple of new Polls, and their response choices
            self._setup_polls_via_admin()

            self.fail('TODO')
            # Now, Herbert the regular user goes to the homepage of the site. He
            [...]


Now, if you try running that test, you should see selenium run through and
enter the two polls, and then exit with the "TODO"::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 76, in test_voting_on_a_new_poll
        self.fail('TODO')
    AssertionError: TODO
    ----------------------------------------------------------------------

If it fails any earlier than that, you may not have completed the last couple
of tutorials in quite the same way I specified.  Figure out what's wrong!



At last! An FT for a normal page
--------------------------------

Let's write the exciting bit of our test, where Herbert the normal user opens
up our website, sees some polls and votes on them.


.. sourcecode:: python
    :filename: mysite/fts/tests.py

    def test_voting_on_a_new_poll(self): 
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(self.live_server_url)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')

        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        first_poll_title = 'How awesome is Test-Driven Development?'
        self.browser.find_element_by_link_text(first_poll_title).click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

        self.fail('TODO')

        # He clicks on the link to the first Poll, which is called
        [...]


We've started with the first bit, where Herbert goes to the main page of the
site, we check that he can see a Poll there, and that he can click on it.  Then
we look for the default 'no votes yet' message on the next page.

Let's run that, and see where we get::

    AssertionError: u'Page not found (404)' != 'PollsNoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 


URLS and view functions, and the Django Test Client
---------------------------------------------------

The FT is telling us that going to the root url (/) doesn't have any ``<h1>``
elements in - that's because we haven't created it yet! We need to tell Django
what kind of web page to return for the root of our site - the home page if you
like.

Django uses a file called ``urls.py``, to route visitors to the python function
that will deal with producing a response for them.  These functions are called
`views` in Django terminology, and they live in ``views.py``. 

(*This is essentially an MVC pattern, there's some discussion of it here:*
https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) 

Let's add a new test to ``polls/tests.py``.  I'm going to use the Django Test Client,
which has some helpful features for testing views.  More info here:

https://docs.djangoproject.com/en/1.4/topics/testing/

We'll create a new class to test our home page view:

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    [...]
    class HomePageViewTest(TestCase):

        def test_root_url_shows_all_polls(self):
            # set up some polls
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
            poll2.save()

            response = self.client.get('/')

            self.assertIn(poll1.question, response.content)
            self.assertIn(poll2.question, response.content)


Now, our first run of the tests will probably complain of a with
``TemplateDoesNotExist: 404.html``.  Django wants us to create a template for
our "404 error" page.  We'll come back to that later.  For now, let's make the
``/`` url return a real HTTP response.
 
First we'll create a dummy view in ``polls/views.py``:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def home(request):
        pass

Now let's hook up this view inside ``mysite/urls.py``:

.. sourcecode:: python
    :filename: mysite/mysite/urls.py

    from django.conf.urls import patterns, include, url
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        url(r'^$', 'polls.views.home'),
        url(r'^admin/', include(admin.site.urls)),
    )

``urls.py`` maps urls (specified as regular expressions) to views.  I've used
dotted-string notation to specify the name of the view, but you could also use
the actual view, like this:

.. sourcecode:: python
    :filename: mysite/mysite/urls.py

    from polls.views import home
    urlpatterns = patterns('',
        url(r'^$', home),
        url(r'^admin/', include(admin.site.urls)),
    )

That would have the advantage that it checks that the view exists and imports
OK.  It's a personal preference, but the official tutorial uses dot-notation,
so I thought we'd stick with that. Read more here:

https://docs.djangoproject.com/en/1.4/intro/tutorial03/#design-your-urls

Re-running our tests should show us a different error::

    ======================================================================
    ERROR: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 92, in test_root_url_shows_all_polls
        response = client.get('/')
      File "/usr/lib/pymodules/python2.7/django/test/client.py", line 445, in get
        response = super(Client, self).get(path, data=data, **extra)
      File "/usr/lib/pymodules/python2.7/django/test/client.py", line 229, in get
        return self.request(**r)
      File "/usr/lib/pymodules/python2.7/django/core/handlers/base.py", line 129, in get_response
        raise ValueError("The view %s.%s didn't return an HttpResponse object." % (callback.__module__, view_name))
    ValueError: The view polls.views.home didn't return an HttpResponse object.
    ----------------------------------------------------------------------

Let's get the view to return an HttpResponse:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    from django.http import HttpResponse

    def home(request):
        return HttpResponse()

The tests are now more instructive::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 96, in test_root_url_shows_all_polls
        self.assertIn(poll1.question, response.content)
    AssertionError: '6 times 7' not found in ''
    ----------------------------------------------------------------------

The Django Template system
--------------------------

So far, we're returning a blank page.  Now, to get the tests to pass, it would
be simple enough to just return a response that contained the questions of our
two polls as "raw" text - like this:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    from django.http import HttpResponse
    from polls.models import Poll

    def home(request):
        content = ''
        for poll in Poll.objects.all():
            content += poll.question

        return HttpResponse(content)

Sure enough, that gets our limited unit tests passing::

    $ python manage.py test polls

    Creating test database for alias 'default'...
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    OK
    Destroying test database for alias 'default'...


Now, this probably seems like a slightly artificial situation - for starters,
the two polls' names will just be concatenated together, without even a space
or a carriage return. We can't possibly leave the situation like this for real
users to see!

But the point of TDD is to be driven by the tests.  At each stage, we only
write the code that our tests require, because that makes absolutely sure that
we have tests for all of our code.

So, rather than anticipate what we might want to put in our HttpResponse, let's
go to the FT now to see what to do next.::

    python manage.py test fts
    ======================================================================
    ERROR: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 57, in test_voting_on_a_new_poll
        heading = self.browser.find_element_by_tag_name('h1')
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 306, in find_element_by_tag_name
        return self.find_element(by=By.TAG_NAME, value=name)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 637, in find_element
        {'using': by, 'value': value})['value']
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 153, in execute
        self.error_handler.check_response(response)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/errorhandler.py", line 123, in check_response
        raise exception_class(message, screen, stacktrace)
    NoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 
    ----------------------------------------------------------------------
    Ran 2 tests in 29.119s


The FT wants an ``h1`` heading tag on the page.  Now, again, we could hard-code
this into view (maybe starting with ``content = <h1>Polls</h1>`` before the
``for`` loop), but at this point it seems sensible to start to use Django's
template system - that will provide a much more natural way to write web pages.

The Django TestCase lets us check whether a response was rendered using a
template, by using a special method response called ``assertTemplateUsed``, so
let's use that.  In ``polls/tests.py``, add an extra check to our view test:

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    class HomePageViewTest(TestCase):

        def test_root_url_shows_links_to_all_polls(self):
            # set up some polls
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
            poll2.save()

            response = self.client.get('/')

            # check we've used the right template
            self.assertTemplateUsed(response, 'home.html')

            # check the poll names appear on the page
            self.assertIn(poll1.question, response.content)
            self.assertIn(poll2.question, response.content)


Testing ``python manage.py test polls``::
 
    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 94, in test_root_url_shows_all_polls
        self.assertTemplateUsed(response, 'home.html')
      File "/usr/lib/pymodules/python2.7/django/test/testcases.py", line 510, in assertTemplateUsed
        self.fail(msg_prefix + "No templates used to render the response")
    AssertionError: No templates used to render the response
    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

So let's now create our template. Templates usually live in a subfolder of each
app::

    mkdir polls/templates
    touch polls/templates/home.html

That should give us a folder structure like this::

    .
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
        |-- admin.py
        |-- __init__.py
        |-- models.py
        |-- templates
        |   `-- home.html
        |-- tests.py
        `-- views.py


Edit ``home.html`` with your favourite editor, 
    
.. sourcecode:: html+django
    :filename: mysite/polls/templates/home.html

    <html>
      <body>
        <h1>Polls</h1>
        {% for poll in polls %}
          <p>{{ poll.question }}</p>
        {% endfor %}
      </body>
    </html>

You'll probably recognise this as being essentially standard HTML, intermixed
with some special django control codes.  These are either surrounded with
``{%`` - ``%}``, for flow control - like a `for` loop in this case, and ``{{``
- ``}}`` for printing variables.  You can find out more about the Django
template language here:

https://docs.djangoproject.com/en/1.4/topics/templates/ 

Let's rewrite our code to use this template.  For this we can use the Django
``render`` function, which takes the request and the name of the template, back
in ``polls/views.py``:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    from django.shortcuts import render
    from polls.models import Poll

    def home(request):
        return render(request, 'home.html')

Our last unit test error was that we weren't using a template - let's see if
this fixes it::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------

    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 97, in test_root_url_shows_all_polls
        self.assertIn(poll1.question, response.content)
    AssertionError: '6 times 7' not found in '<html>\n  <body>\n    <h1>Polls</h1>\n    \n  </body>\n</html>\n'
    ----------------------------------------------------------------------

Sure does!  Unfortunately, we've lost our Poll questions from the response
content...

Looking at the template code, you can see that we want to iterate through a
variable called ``polls``.  The way we pass this into a template is via a
dictionary called a `context`.  The Django test client also lets us check on
what context objects were used in rendering a response, so we can write a test
for that too:

.. sourcecode:: python
    :filename: mysite/polls/tests.py

        response = self.client.get('/')

        # check we've used the right template
        self.assertTemplateUsed(response, 'home.html')

        # check we've passed the polls to the template
        polls_in_context = response.context['polls']
        self.assertEquals(list(polls_in_context), [poll1, poll2])

        # check the poll names appear on the page
        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)


Notice the way we've had to call ``list`` on ``polls_in_context`` - that's
because Django queries return special ``QuerySet`` objects, which, although
they behave like lists, don't quite compare equal like them.

Now, re-running the tests gives us::

    ======================================================================
    ERROR: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 97, in test_root_url_shows_all_polls
        polls_in_context = response.context['polls']
      File "/usr/lib/pymodules/python2.7/django/template/context.py", line 60, in __getitem__
        raise KeyError(key)
    KeyError: 'polls'
    ----------------------------------------------------------------------
    Ran 6

Essentially, we never passed any 'polls' to our template.  Let's add them,
but make them empty - again, the idea is to make the minimal change to move
the test forwards:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def home(request):
        context = {'polls': []}
        return render(request, 'home.html', context)


Now the unit tests say::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 98, in test_root_url_shows_all_polls
        self.assertEquals(list(polls_in_context), [poll1, poll2])
    AssertionError: Lists differ: [] != [<Poll: 6 times 7>, <Poll: lif...

    Second list contains 2 additional elements.
    First extra element 0:
    6 times 7

    - []
    + [<Poll: 6 times 7>, <Poll: life, the universe and everything>]
    ----------------------------------------------------------------------


Let's fix our code so the tests pass:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    from django.shortcuts import render
    from polls.models import Poll

    def home(request):
        context = {'polls': Poll.objects.all()}
        return render(request, 'home.html', context)

Ta-da!::

    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.011s

    OK

What do the FTs say now?::

    python manage.py test fts
    ======================================================================
    ERROR: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 62, in test_voting_on_a_new_poll
        self.browser.find_element_by_link_text('How awesome is Test-Driven Development?').click()
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 234, in find_element_by_link_text
        return self.find_element(by=By.LINK_TEXT, value=link_text)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 637, in find_element
        {'using': by, 'value': value})['value']
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/webdriver.py", line 153, in execute
        self.error_handler.check_response(response)
      File "/usr/local/lib/python2.7/dist-packages/selenium/webdriver/remote/errorhandler.py", line 123, in check_response
        raise exception_class(message, screen, stacktrace)
    NoSuchElementException: Message: u'Unable to locate element: {"method":"link text","selector":"How awesome is Test-Driven Development?"}' 
    ----------------------------------------------------------------------


Testing philosophy: what to test in templates
---------------------------------------------

Ah - although our page may contain the name of our Poll, it's not yet a link we
can click. The way we'd fix this is in the ``home.html`` template, by adding an ``<a href=``.

So is this something we write a unit test for as well?  Some people would tend
to say that this is one unit test too many...  Since this is a guide to
**rigorous** TDD, I'm going to say we probably should in this case. 

On the other hand, if we write a unit test for every single last bit of html
that we want to write, every last presentational detail, then making tiny
tweaks to the UI is going to be really burdensome.

At this point, a couple of rules of thumb are useful:

    * In unit tests, **Don't test constants**

    * In functional tests, **Test functionality, not presentation**

The first rule works out like this - if we have some code that says::

    wibble = 3

There's no point in writing a test that says::

    self.assertEquals(wibble, 3)

Tests are meant to check how our code behaves, not just to repeat every line of
it.

The second rule is a related rule, but it's more about how users interact with
your software.  We want our functional tests to check that the software allows
the user to accomplish certain tasks.  So, we need to check that each screen
contains elements that can guide the user towards the choices they need to make
(the link text), and also that they function in a way that moves the user
towards their goal (our link, when clicked, will take the user to the right
page).

What we definitely don't need to test in our FTs are things like - what
specific colour are the links (although the fact that they are a different
colour to something else may be relevant).  We don't need to check the
particular font they use.  We don't need to check whether they are displayed in
a ``ul`` or in a ``table`` - although we may want to check that they are
displayed in the correct order.

So, where does that leave us?  The FT currently checks the functionality of the
site - it checks the link has the correct text, and later it checks that
clicking the link takes us to the right place.  

So, what about unit testing the templates?  Well, most of what's in a template
is just a constant - we don't want to have to rewrite our unit tests just
because we want to correct a typo in a bit of blurb... The parts of a template
that aren't "just a constant" are the bits inside ``{{ }}`` or ``{%  %}`` -
bits that manipulate some of the ``context`` variables we pass into the
``render`` call.

So, in our unit tests, we need to check that the variables we pass in end up
being used - that's why we have the ``assertIn`` checks on the
``response.content`` as well as the ``assertEqual`` test on the
``response.context``.

So, what about checking that our template contains the correct hyperlinks, ``<a
href="/poll/01/``, or whatever they may be?  Well, if we were to hard-code them
into the template, then that would be a bit like testing a constant.  But we're
not going to hard-code them, because that would violate the programming `DRY`
principle - "Don't Repeat Yourself".

If we were to hard-code the URLs for links to individual polls, it would be
really tedious if we wanted to come back and change them later - say from
``/poll/1/`` to ``/poll_detail/01/`` or whatever it may be.  Django provides a
single place to define urls, in ``urls.py``, and it then provides helper tools
for retrieving them in other places - a function called ``reverse``, and a
template tag called ``{% url %}``.  So we'll use the template tag, which avoids
hard-coding the URL in the template, but it also means that the hyperlink is no
longer a constant, so we need to test it.

Phew, that was long winded!  Anyway, the upshot is, more tests - but also, we
get to learn about Django url helper functions, so it's win-win-win :-)

Let's use the ``reverse`` function in our tests.  Its first argument is the
name of the view that handles the url, and we can also specify some arguments.
We'll be making a view for seeing an individual `Poll` object, so we'll
probably find the poll using its ``id``.  Here's what that translates to in
``polls/tests.py``:

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    from django.core.urlresolvers import reverse

    class HomePageViewTest(TestCase):

        def test_root_url_shows_links_to_all_polls(self):
            # set up some polls
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
            poll2.save()

            response = self.client.get('/')

            # check we've used the right template
            self.assertTemplateUsed(response, 'home.html')

            # check we've passed the polls to the template
            polls_in_context = response.context['polls']
            self.assertEquals(list(polls_in_context), [poll1, poll2])

            # check the poll names appear on the page
            self.assertIn(poll1.question, response.content)
            self.assertIn(poll2.question, response.content)

            # check the page also contains the urls to individual polls pages
            poll1_url = reverse('polls.views.poll', args=[poll1.id,])
            self.assertIn(poll1_url, response.content)
            poll2_url = reverse('polls.views.poll', args=[poll2.id,])
            self.assertIn(poll2_url, response.content)


Note I've also changed the name of the test, from
`test_root_url_shows_all_polls` to `test_root_url_shows_links_to_all_polls`, which
is more descriptive of what we're doing now.

Running this (``python manage.py test polls``) gives::

    ======================================================================
    ERROR: test_root_url_shows_links_to_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 107, in test_root_url_shows_links_to_all_polls
        poll1_url = reverse('mysite.polls.views.poll', kwargs=dict(poll_id=poll1.id))
      File "/usr/lib/pymodules/python2.7/django/core/urlresolvers.py", line 391, in reverse
        *args, **kwargs)))
      File "/usr/lib/pymodules/python2.7/django/core/urlresolvers.py", line 337, in reverse
        "arguments '%s' not found." % (lookup_view_s, args, kwargs))
    NoReverseMatch: Reverse for 'polls.views.poll' with arguments '(1,)' and keyword arguments '{}' not found.

    ----------------------------------------------------------------------

So, the ``reverse`` function can't find a url or a view to match our request -
let's add placeholders for them:

Capturing parameters from URLs 
------------------------------

In ``mysite/urls.py``:

.. sourcecode:: python
    :filename: mysite/mysite/urls.py

    urlpatterns = patterns('',
        url(r'^$', 'polls.views.home'),
        url(r'^poll/(\d+)/$', 'polls.views.poll'),
        url(r'^admin/', include(admin.site.urls)),
    )

Our new line defines a set of urls that start with `poll/`, then a number made
up of one or more digits - the matching group ``(\d+)``. When a url has a
matching group, the captured contents are passed to the view as arguments.  So,
if you look back at what the unit test was last complaining about, we should
have fixed its problem: we've now created a url that references
``'polls.views.poll'`` and which is capable of taking an argument of ``1``. 

So now our unit tests give a different error::

    ======================================================================
    FAIL: test_root_url_shows_links_to_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 108, in test_root_url_shows_links_to_all_polls
        self.assertIn(poll1_url, response.content)
    AssertionError: '/poll/1/' not found in '<html>\n  <body>\n    <h1>Polls</h1>\n    \n      6 times 7\n    \n      life, the universe and everything\n    \n  </body>\n</html>\n'
    ----------------------------------------------------------------------


The templates don't include the hyperlinks yet. Let's add them:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/home.html

    <html>
      <body>
        <h1>Polls</h1>
        {% for poll in polls %}
          <p><a href="{% url polls.views.poll poll.id %}">{{ poll.question }}</a></p>
        {% endfor %}
      </body>
    </html>

Notice the call to ``{% url %}``, which works almost exactly like ``reverse``.  Are our unit tests any happier?::


    ======================================================================
    ERROR: test_root_url_shows_links_to_all_polls (polls.tests.HomePageViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests.py", line 99, in test_root_url_shows_links_to_all_polls
        response = client.get('/')
      File "/usr/local/lib/python2.7/dist-packages/django/test/client.py", line 439, in get
        response = super(Client, self).get(path, data=data, **extra)
      File "/usr/local/lib/python2.7/dist-packages/django/test/client.py", line 244, in get
        return self.request(**r)
      File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 111, in get_response
        response = callback(request, *callback_args, **callback_kwargs)
      File "/home/harry/workspace/mysite/polls/views.py", line 7, in home
        return render(request, 'home.html', context)
      File "/usr/local/lib/python2.7/dist-packages/django/shortcuts/__init__.py", line 44, in render
        return HttpResponse(loader.render_to_string(*args, **kwargs),
      File "/usr/local/lib/python2.7/dist-packages/django/template/loader.py", line 176, in render_to_string
        return t.render(context_instance)
      File "/usr/local/lib/python2.7/dist-packages/django/template/base.py", line 140, in render
        return self._render(context)
      File "/usr/local/lib/python2.7/dist-packages/django/test/utils.py", line 62, in instrumented_test_render
        return self.nodelist.render(context)
      File "/usr/local/lib/python2.7/dist-packages/django/template/base.py", line 823, in render
        bit = self.render_node(node, context)
      File "/usr/local/lib/python2.7/dist-packages/django/template/debug.py", line 74, in render_node
        return node.render(context)
      File "/usr/local/lib/python2.7/dist-packages/django/template/defaulttags.py", line 185, in render
        nodelist.append(node.render(context))
      File "/usr/local/lib/python2.7/dist-packages/django/template/defaulttags.py", line 411, in render
        url = reverse(view_name, args=args, kwargs=kwargs, current_app=context.current_app)
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 476, in reverse
        return iri_to_uri(resolver._reverse_with_prefix(view, prefix, *args, **kwargs))
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 363, in _reverse_with_prefix
        possibilities = self.reverse_dict.getlist(lookup_view)
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 276, in reverse_dict
        self._populate()
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 265, in _populate
        lookups.appendlist(pattern.callback, (bits, p_pattern, pattern.default_args))
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 216, in callback
        self._callback = get_callable(self._callback_str)
      File "/usr/local/lib/python2.7/dist-packages/django/utils/functional.py", line 27, in wrapper
        result = func(*args)
      File "/usr/local/lib/python2.7/dist-packages/django/core/urlresolvers.py", line 101, in get_callable
        (lookup_view, mod_name))
    ViewDoesNotExist: Could not import polls.views.poll. View does not exist in module polls.views.

    ----------------------------------------------------------------------

Phew. A long traceback, but basically all it's saying is that we need at least
a placeholder for our new "poll" view in ``mysite/views.py``.  Let's add that now:

.. sourcecode:: python
    :filename: mysite/mysite/views.py

    def home(request):
        context = {'polls': Poll.objects.all()}
        return render(request, 'home.html', context)
        

    def poll():
        pass

And run the unit tests again::

    21:08 ~/workspace/tddjango_site/source/mysite (master)$ python manage.py test polls 
    Creating test database for alias 'default'...
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.012s
    OK

What about the functional tests?::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 


Well, they get past the main page, but they fall over when they try to look at
an individual poll. Looks like it's time to start implementing our `poll` view,
which aims to show information about a particular poll...  But for this, you'll
have to tune in next week!


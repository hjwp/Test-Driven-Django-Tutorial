Welcome to part 3 of the tutorial!  This week we'll finally get into writing
our own web pages, rather than using the Django Admin site.

Let's pick up our FT where we left off - we now have the admin site set up to
add Polls, including Choices.  We now want to flesh out what the user sees.

Last time we wrote the code to get Gertrude the admin to log in and create a 
poll.  Let's write the next bit, where Herbert the normal user opens up our
website, sees some polls and votes on them.

.. sourcecode:: python

    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(ROOT)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')

        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        self.browser.find_element_by_link_text('How awesome is Test-Driven Development?').click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Poll Results')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

Let's run that, and see where we get::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/Test-Driven-Django-Tutorial/mysite/fts/test_polls.py", line 57, in test_voting_on_a_new_poll
        self.assertEquals(heading.text, 'Polls')
    AssertionError: u'Page not found (404)' != 'Polls'

    ----------------------------------------------------------------------
    Ran 2 tests in 19.772s


The FT is telling us that going to the `ROOT` url (/) produces a 404. We need to tell
Django what kind of web page to return for the root of our site - the home page if 
you like.

Django uses a file called ``urls.py``, to route visitors to the python function that
will deal with producing a response for them.  These functions are called `views` in
Django terminology, and they live in ``views.py``. (This is essentially an MVC pattern, there's some discussion of it here: https://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) 

Let's add a new test to ``tests.py``.  I'm going to use the Django Test Client, which
has some helpful features for testing views.  More info here:

https://docs.djangoproject.com/en/1.3/topics/testing/

.. sourcecode:: python

    from django.test.client import Client
    [...]

    def test_root_url_shows_all_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date='2001-01-01')
        poll2.save()

        client = Client()
        response = client.get('/')

        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)

Don't forget the import at the top!  Now, our first run of the tests will probably 
complain of a with ``TemplateDoesNotExist: 404.html``.  Django wants us to create a
template for our "404 error" page.  We'll come back to that later.  For now, let's
make the ``/`` url return a real HTTP response.
 
First we'll create a dummy view in ``views.py``:

.. sourcecode:: python

    def polls(request):
        pass

Now let's hook up this view inside ``urls.py``:

.. sourcecode:: python

    urlpatterns = patterns('',
        (r'^$', 'mysite.polls.views.polls'),
        (r'^admin/', include(admin.site.urls)),
    )

Re-running our tests should show us a different error::

    ======================================================================
    ERROR: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
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
    ValueError: The view mysite.polls.views.polls didn't return an HttpResponse object.

    ----------------------------------------------------------------------

Let's get the view to return an HttpResponse:

.. sourcecode:: python

    from django.http import HttpResponse

    def polls(request):
        return HttpResponse()

The tests are now more instructive::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 96, in test_root_url_shows_all_polls
        self.assertIn(poll1.question, response.content)
    AssertionError: '6 times 7' not found in ''

    ----------------------------------------------------------------------

So far, we're returning a blank page.  Now, to get the tests to pass, it would
be simple enough to just return a response that contained the questions of our two
polls as `raw` text - like this:

.. sourcecode:: python

    from django.http import HttpResponse
    from polls.models import Poll

    def polls(request):
        content = ''
        for poll in Poll.objects.all():
            content += poll.question

        return HttpResponse(content)

Sure enough, that gets our limited unit tests passing::

    23:06 ~/workspace/tddjango_site/source/mysite (master)$ ./manage.py test polls
    Creating test database for alias 'default'...
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

    OK
    Destroying test database for alias 'default'...


Now, this probably seems like a slightly artificial situation - for starters, the two
poll's names will just be concatenated together, without even a space or a carriage
return. We can't possibly leave the situation like this.  But the point of TDD is to
be driven by the tests.  At each stage, we only write the code that our tests require,
because that makes absolutely sure that we have tests for all of our code.

So, rather than anticipate what we might want to put in our HttpResponse, let's go to the FT now to see what to do next.::

    ./functional_tests.py
    ======================================================================
    ERROR: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/test_polls.py", line 57, in test_voting_on_a_new_poll
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


The FT wants an ``h1`` heading tag on the page.  Now, again, we could hard-code this
into view (maybe starting with ``content = <h1>Polls</h1>`` before the ``for`` loop),
but at this point it seems sensible to start to use Django's template system.

The Django Test Client lets us check whether a response was rendered using a
template, by using a special attribute of the response called ``templates``,
so let's use that.  In ``tests.py``:

.. sourcecode:: python

        template_names_used = [t.name for t in response.templates]
        self.assertIn('polls.html', template_names_used)

        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)


Testing ``./manage.py test polls``::
 
    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 94, in test_root_url_shows_all_polls
        self.assertIn('polls.html', response.templates)
    AssertionError: 'polls.html' not found in []

    ----------------------------------------------------------------------
    Ran 6 tests in 0.009s

So let's now create our template::

    mkdir mysite/polls/templates
    touch mysite/polls/templates/polls.html

Edit it with your favourite editor, 
    
.. sourcecode:: html+django

    <html>
      <body>
        <h1>Polls</h1>
        {% for poll in polls %}
          {{ poll.question }}
        {% endfor %}
      </body>
    </hml>

You'll probably recognise this as being essentially standard HTML, intermixed with
some special django control codes.  These are either surrounded with
``{%`` - ``%}``, for flow control - like a `for` loop in this case, and ``{{``
- ``}}`` for printing variables.  You can find out more about the Django template
  language here:

 https://docs.djangoproject.com/en/1.3/topics/templates/ 

 Let's rewrite our code to use this template.  For this we can use the Django
 ``render`` function, which takes the request and the name of the template:

.. sourcecode:: python

    from django.shortcuts import render
    from polls.models import Poll

    def polls(request):
        content = ''
        for poll in Poll.objects.all():
            content += poll.question

        return render(request, 'polls.html')

Our last unit test error was that we weren't using a template - let's see if this
fixes it::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/polls/tests.py", line 97, in test_root_url_shows_all_polls
        self.assertIn(poll1.question, response.content)
    AssertionError: '6 times 7' not found in '<html>\n  <body>\n    <h1>Polls</h1>\n    \n  </body>\n</hml>\n'

    ----------------------------------------------------------------------

Sure does!  Unfortunately, we've lost our Poll questions from the response
content...

Looking at the template code, you can see that we want to iterate through a
variable called ``polls``.  The way we pass this into a template is via a
special kind of dictionary called a `context`.  The Django test client also
lets us check on what context objects were used in rendering a response, so
we can write a test for that too:

.. sourcecode:: python

        client = Client()
        response = client.get('/')

        template_names_used = [t.name for t in response.templates]
        self.assertIn('polls.html', template_names_used)

        polls_in_context = response.context['polls']
        self.assertEquals(list(polls_in_context), [poll1, poll2])

        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)


Now, re-running the tests gives us::

    ======================================================================
    ERROR: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
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

    def polls(request):
        content = ''
        for poll in Poll.objects.all():
            content += poll.question

        context = {'polls': []}
        return render(request, 'polls.html', context)

Now the unit tests say::

    ======================================================================
    FAIL: test_root_url_shows_all_polls (polls.tests.TestAllPollsView)
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



Notice the way we've had to call ``list`` on ``polls_in_context`` - that's
because Django queries return special ``QuerySet`` objects, which, although
they behave like lists, don't quite compare equal like them.

Let's fix our code so the tests pass:

.. sourcecode:: python

    from django.shortcuts import render
    from polls.models import Poll

    def polls(request):
        context = {'polls': Poll.objects.all()}
        return render(request, 'polls.html', context)

Ta-da!::

    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.011s

    OK


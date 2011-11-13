Welcome to part 4 of the tutorial!  In this part at how we can let
users vote on our poll, in other words, **web forms!**. Hooray.

Let's start by extending our FT, to show Herbert voting on a poll:

.. sourcecode:: python

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(ROOT)
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

        # He also sees a form, which offers him several choices.
        choices = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        choices_text = [c.text for c in choices]
        self.assertEquals(choices_text, [
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])
        # He decided to select "very awesome"
        chosen = self.browser.find_element_by_css_selector(
                "input[type='radio', value='Very awesome']"
        )
        chosen.click()

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".

        # The page also says "1 votes"

        # Satisfied, he goes back to sleep

The functional tests are still telling us that we need to fix our polls view
though::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/test_polls.py", line 67, in test_voting_on_a_new_poll
        self.assertEquals(heading.text, 'Poll Results')
    AssertionError: u'TypeError at /poll/1/' != 'Poll Results'
    ----------------------------------------------------------------------
    Ran 2 tests in 25.927s

Let's work on the unit tests for the ``poll`` view then:

.. sourcecode:: python


    class TestSinglePollView(TestCase):

        def test_page_shows_poll_title_and_no_votes_message(self):
            # set up two polls, to check the right one is displayed
            poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
            poll1.save()
            poll2 = Poll(question='life, the universe and everything', pub_date='2001-01-01')
            poll2.save()

            client = Client()
            response = client.get('/poll/%d/' % (poll2.id, ))

            self.assertEquals(response.templates[0].name, 'poll.html')
            self.assertEquals(response.context['poll'], poll2)
            self.assertIn(poll2.question, response.content)
            self.assertIn('No-one has voted on this poll yet', response.content)

Running the tests gives::

    TypeError: poll() takes no arguments (2 given)

(I'm going to be shortening the test outputs from now on.  You're a grown-up
now, you can handle it!)

Let's make our view take two arguments:

.. sourcecode:: python

    def poll(request, poll_id):
        pass

Now we get::

    ValueError: The view mysite.polls.views.poll didn't return an HttpResponse object.

Again, a minimal fix:

.. sourcecode:: python

    def poll(request, poll_id):
        return HttpResponse()

Now we get this error::

    self.assertEquals(response.templates[0].name, 'poll.html')
    IndexError: list index out of range

A slightly unhelpful error, but essentially it's telling us that the
view didn't use a template.  Let's try fixing that - but deliberately
using the wrong template (just to check we are testing it)

.. sourcecode:: python

    def poll(request, poll_id):
        return render(request, 'polls.html')

Good, looks like we are testiing it properly::

    AssertionError: 'polls.html' != 'poll.html'

And changing it to ``poll.html`` gives us::

    TemplateDoesNotExist: poll.html

Fine and dandy, let's make one::

     touch polls/templates/poll.html    

Now the tests want us to pass a `poll` variable in the template's context::

    KeyError: 'poll'

So let's do that, again, the minimum possible change to satisfy the tests:

.. sourcecode:: python

    def poll(request, poll_id):
        return render(request, 'polls.html', {'poll': None})

And the tests get a little further on::

    AssertionError: None != <Poll: life, the universe and everything>

And they even tell us what to do next - pass in the right `Poll` object:

.. sourcecode:: python

    def poll(request, poll_id):
        poll = Poll.objects.get(pk=poll_id)
        return render(request, 'poll.html', {'poll': poll})

This is the first time we've used the Django API to fetch a single database
object, and ``objects.get`` is the helper function for this - it raises an
error if it can't find the object, or if it finds more than one. The special
keyword argument ``pk`` stands for `primary key`. In this case, Django is 
using the default for primary keys, which is an automatically genereated
integer ``id`` column.

That raises the question of what to do if a user types in a url for a poll 
that doesn't exist - ``/poll/0/`` for example.  We'll come back to this in 
a later tutorial.

In the meantime, what do the tests say::

    self.assertIn(poll2.question, response.content)
    AssertionError: 'life, the universe and everything' not found in ''

We need to get our template to include the poll's question. Let's make it 
into a page heading:

.. sourcecode:: html+django

    <html>
      <body>
        <h2>{{poll.question}}</h2>
      </body>
    </html>

Now the tests want our 'no polls yet' message::

    AssertionError: 'No-one has voted on this poll yet' not found in '<html>\n  <body>\n    <h2>life, the universe and everything</h2>\n  </body>\n</html>\n'

So let's include that:

.. sourcecode:: html+django

    <html>
      <body>
        
        <h2>{{poll.question}}</h2>

        <p>No-one has voted on this poll yet</p>
        
      </body>
    </html>

And that's enough to make the unit tests happy::

    ----------------------------------------------------------------------
    Ran 7 tests in 0.013s

    OK

Mmmh, `OK`.  Let's see what the FTs think?::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 

Ah, we forgot to include a general heading for the page

.. sourcecode:: python

        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)

So let's add an ``h1`` with "Poll Results" in it:

.. sourcecode:: html+django

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <p>No-one has voted on this poll yet</p>
        
      </body>
    </html>

Now what?::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/test_polls.py", line 82, in test_voting_on_a_new_poll
        'Moderately awesome',
    AssertionError: Lists differ: [] != ['Very awesome', 'Quite awesom...

    Second list contains 3 additional elements.
    First extra element 0:
    Very awesome

    - []
    + ['Very awesome', 'Quite awesome', 'Moderately awesome']
    ----------------------------------------------------------------------

Ah, we need to add the poll Choices as a series of radio inputs.  Now the official Django
tutorial shows you how to hard-code them in HTML, but Django can do even better than that:

https://docs.djangoproject.com/en/1.3/intro/tutorial04/

Django's forms system will generate radio buttons for us, if we can just give it the right
incantations.  Let's create a new test in ``tests.py``:


.. sourcecode:: python

    from polls.forms import PollVoteForm

    class TestPollsVoteForm(TestCase):

        def test_form_renders_poll_choices_as_radio_inputs(self):
            # set up a poll with a coup`le of choices
            poll = Poll(question='6 times 7', pub_date='2001-01-01')
            poll.save()
            choice1 = Choice(poll=poll, choice='42', votes=0)
            choice1.save()
            choice2 = Choice(poll=poll, choice='The Ultimate Answer', votes=0)
            choice2.save()

            # build a related form:
            form = PollVoteForm(poll=poll)

            # check it has a single field called 'vote', which has right choices:
            self.assertEquals(form.fields.keys(), ['vote'])
            vote_field = form.fields['vote']
            self.assertEqual(vote_field.choices, [choice1.choice, choice2.choice])

            # check it uses radio inputs to render
            self.assertIn('input type="radio"', form.as_p())

You might prefer to put the input at the top of the file.  And, for it to work, we
may as well create a dummy class for it.  Create a file called ``polls/forms.py``.

.. sourcecode:: python

    class PollVoteForm(object):
        pass
 
And let's start another test/code cycle, woo -::

    ./manage.py test polls
    [...]
        form = PollVoteForm(poll=poll)
    TypeError: object.__new__() takes no parameters

We override __init__.py to change the constructor:

.. sourcecode:: python

    class PollVoteForm(object):
        def __init__(self, poll):
            pass

::
    self.assertEquals(form.fields.keys(), ['vote'])
    AttributeError: 'PollVoteForm' object has no attribute 'fields'

to give the form a 'fields' attribute, we can make it inherit from
a real Django form class, and call its parent constructor:

.. sourcecode:: python

    from django import forms

    class PollVoteForm(forms.Form):
        def __init__(self, poll):
            super(self.__class__, self).__init__()

Now we get::

    AssertionError: Lists differ: [] != ['vote']

Django form fields are defined a bit like model fields - as inline
class attributes. There are various types of fields, in this case
we want one that has `choices` - a ``ChoiceField``.
You can find out more about form fields here:

https://docs.djangoproject.com/en/1.3/ref/forms/fields/

.. sourcecode:: python

    class PollVoteForm(forms.Form):
        vote = forms.ChoiceField()

        def __init__(self, poll):
            super(self.__class__, self).__init__()

Now we get::

    self.assertEqual(vote_field.choices, [choice1.choice, choice2.choice])
    AssertionError: Lists differ: [] != ['42', 'The Ultimate Answer']

So now let's set the choices from the ``poll`` we passed into the 
constructor:

.. sourcecode:: python

    def __init__(self, poll):
        super(self.__class__, self).__init__()
        self.fields['vote'].choices = [c.choice for c in poll.choice_set.all()]


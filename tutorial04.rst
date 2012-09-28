Welcome to part 4 of the tutorial!  In this part at how we can let users vote
on our poll, in other words, **web forms!**. Hooray.

Tutorial 4: Using a form
========================

Here's the outline of what we're going to do in this tutorial:

    * extend the FT to show Herbert voting on the poll

    * create a url, view and template to generate pages for individual polls

    * create a Django form to handle choices


Extending the FT to vote using radio buttons
--------------------------------------------

Let's start by extending our FT, to show Herbert voting on a poll. In
``fts/tests.py``:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        [...] 
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

        # He also sees a form, which offers him several choices.
        # There are three options with radio buttons
        choice_inputs = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        self.assertEquals(len(choice_inputs), 3)

        # The buttons have labels to explain them
        choice_labels = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])
        # He decided to select "very awesome", which is answer #1
        chosen = self.browser.find_element_by_css_selector(
                "input[value='1']"
        )
        chosen.click()

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        self.fail('TODO')

        # The page also says "1 votes"

        # Satisfied, he goes back to sleep


If you run them, you'll find that they are still telling us the individual poll
page isn't working::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 


That because, currently, our ``poll`` view is just a placeholder function.  We
need to make into into a real Django view, which returns information about a
poll.

Let's work on the unit tests for the ``poll`` view then. Make a new class for
them in ``polls/tests.py``:

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    class SinglePollViewTest(TestCase):

        def test_page_shows_poll_title_and_no_votes_message(self):
            # set up two polls, to check the right one is displayed
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
            poll2.save()

            response = self.client.get('/poll/%d/' % (poll2.id, ))

            # check we've used the poll template
            self.assertTemplateUsed(response, 'poll.html') 

            # check we've passed the right poll into the context
            self.assertEquals(response.context['poll'], poll2)

            # check the poll's question appears on the page
            self.assertIn(poll2.question, response.content)

            # check our 'no votes yet' message appears
            self.assertIn('No-one has voted on this poll yet', response.content)


Running the tests gives::

    TypeError: poll() takes no arguments (2 given)

(*I'm going to be shortening the test outputs from now on.  You're a TDD
veteran now, you can handle it! :-)*

Let's make our view take two arguments:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        pass

Now we get::

    ValueError: The view mysite.polls.views.poll didn't return an HttpResponse object.

Again, a minimal fix:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        return HttpResponse()

Now we get this error::

    AssertionError: No templates used to render the response


Let's try fixing that - but deliberately using the wrong template (just to
check we are testing it)

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        return render(request, 'home.html')

Good, looks like we are testiing it properly::

    AssertionError: Template 'poll.html' was not a template used to render the response. Actual template(s) used: home.html

And changing it to ``poll.html`` gives us::

    TemplateDoesNotExist: poll.html

Fine and dandy, let's make one::

     touch polls/templates/poll.html    

You might argue that an empty file, all 0 bytes of it, is a fairly minimal
template!  Still, it seems to satisfy the tests. Now they want us to pass a
``poll`` variable in the template's context::

    KeyError: 'poll'

So let's do that, again, the minimum possible change to satisfy the tests:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        return render(request, 'poll.html', {'poll': None})

And the tests get a little further on::

    AssertionError: None != <Poll: life, the universe and everything>

And they even tell us what to do next - pass in the right `Poll` object:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        poll = Poll.objects.get(pk=poll_id)
        return render(request, 'poll.html', {'poll': poll})

This is the first time we've used the Django API to fetch a single database
object, and ``objects.get`` is the helper function for this - it raises an
error if it can't find the object, or if it finds more than one. The special
keyword argument ``pk`` stands for `primary key`. In this case, Django is using
the default for primary keys, which is an automatically generated integer
``id`` column.

That raises the question of what to do if a user types in a url for a poll that
doesn't exist - ``/poll/0/`` for example.  We'll come back to this in a later
tutorial.

In the meantime, what do the tests say::

    self.assertIn(poll2.question, response.content)
    AssertionError: 'life, the universe and everything' not found in ''

We need to get our template to include the poll's question. Let's make it into
a page heading:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h2>{{poll.question}}</h2>
      </body>
    </html>

Now the tests want our 'no polls yet' message::

    AssertionError: 'No-one has voted on this poll yet' not found in '<html>\n  <body>\n    <h2>life, the universe and everything</h2>\n  </body>\n</html>\n'

So let's include that:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/home.html

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

Mmmh, `OK`. And doughnuts. Let's see what the FTs think?::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"tag name","selector":"h1"}' 

Ah, we forgot to include a general heading for the page - the FT is checking
the ``h1`` and ``h2`` headings:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)

So, in our template, let's add an ``h1`` with "Poll Results" in it:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/home.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <p>No-one has voted on this poll yet</p>
        
      </body>
    </html>


Using a Django form for poll choices
------------------------------------

Now what does the FT say?::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/fts/tests.py", line 100, in test_voting_on_a_new_poll
        self.assertEquals(len(choice_inputs), 3)
    AssertionError: 0 != 3

    ----------------------------------------------------------------------

Ah, we need to add the poll Choices as a series of radio inputs.  Now the
official Django tutorial shows you how to hard-code them in HTML:

https://docs.djangoproject.com/en/1.4/intro/tutorial04/

But Django can do even better than that - Django's forms system will generate
radio buttons for us, if we can just give it the right incantations.  Let's
create a new test in ``polls/tests.py``:


.. sourcecode:: python
    :filename: mysite/polls/tests.py

    from polls.forms import PollVoteForm

    class PollsVoteFormTest(TestCase):

        def test_form_renders_poll_choices_as_radio_inputs(self):
            # set up a poll with a couple of choices
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            choice1 = Choice(poll=poll1, choice='42', votes=0)
            choice1.save()
            choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
            choice2.save()

            # set up another poll to make sure we only see the right choices
            poll2 = Poll(question='time', pub_date=timezone.now())
            poll2.save()
            choice3 = Choice(poll=poll2, choice='PM', votes=0)
            choice3.save()

            # build a voting form for poll1
            form = PollVoteForm(poll=poll1)

            # check it has a single field called 'vote', which has right choices:
            self.assertEquals(form.fields.keys(), ['vote'])

            # choices are tuples in the format (choice_number, choice_text):
            self.assertEquals(form.fields['vote'].choices, [
                (choice1.id, choice1.choice),
                (choice2.id, choice2.choice),
            ])

            # check it uses radio inputs to render
            self.assertIn('input type="radio"', form.as_p())

You might prefer to put the import at the top of the file.  

Looking through the code, you can see we instantiate a form, passing it a poll
object. We then examine the form's ``fields`` attribute, find the one called
``vote`` (this will also be the ``name`` of the HTML input element), and we
check the ``choices`` for that field.

For the test to even get off the ground, we may as well create something
minimal for it to import! Create a file called ``polls/forms.py``.

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    class PollVoteForm(object):
        pass
 
And let's start another test/code cycle, woo -::

    python manage.py test polls

    [...]
        form = PollVoteForm(poll=poll)
    TypeError: object.__new__() takes no parameters

We override ``__init__.py`` to change the constructor:

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    class PollVoteForm(object):
        def __init__(self, poll):
            pass

... ::

    self.assertEquals(form.fields.keys(), ['vote'])
    AttributeError: 'PollVoteForm' object has no attribute 'fields'

To give the form a 'fields' attribute, we can make it inherit from a real
Django form class, and call its parent constructor:

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    from django import forms

    class PollVoteForm(forms.Form):
        def __init__(self, poll):
            forms.Form.__init__(self)

Now we get::

    AssertionError: Lists differ: [] != ['vote']

Django form fields are defined a bit like model fields - using inline class
attributes. There are various types of fields, in this case we want one that
has `choices` - a ``ChoiceField``. You can find out more about form fields
here:

https://docs.djangoproject.com/en/1.4/ref/forms/fields/

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    class PollVoteForm(forms.Form):
        vote = forms.ChoiceField()

        def __init__(self, poll):
            forms.Form.__init__(self)

Now we get::

    AssertionError: Lists differ: [] != [(1, '42'), (2, 'The Ultimate ...

So now let's set the choices from the ``poll`` we passed into the constructor
(you can read up on choices in Django here
https://docs.djangoproject.com/en/1.4/ref/models/fields/#field-choices)

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    def __init__(self, poll):
        forms.Form.__init__(self)
        self.fields['vote'].choices = [(c.id, c.choice) for c in poll.choice_set.all()]

Mmmmmh, list comprehensions... That will now get the test almost to the end -
we can instantiate a form using a poll object, and the form will automatically
generate the choices based on the poll's ``choice_set.all()`` function, which
gets related objects.

The final test is to make sure we have radio boxes as the HTML input type.
We're using ``as_p()``, a method provided on all Django forms which renders the
form to HTML for us - we can see exactly what the HTML looks like in the next
test output::

    self.assertIn('input type="radio"', form.as_p())
    AssertionError: 'input type="radio"' not found in u'<p><label for="id_vote">Vote:</label> <select name="vote" id="id_vote">\n<option value="1">42</option>\n<option value="2">The Ultimate Answer</option>\n</select></p>'

Django has defaulted to using a ``select/option`` input form.  We can change
this using a `widget`, in this case a ``RadioSelect``

.. sourcecode:: python
    :filename: mysite/polls/forms.py

    class PollVoteForm(forms.Form):
        vote = forms.ChoiceField(widget=forms.RadioSelect())

        def __init__(self, poll):
            forms.Form.__init__(self)
            self.fields['vote'].choices = [(c.id, c.choice) for c in poll.choice_set.all()]

OK so far?  Django forms have *fields*, some of which may have *choices*, and
we can choose how the field will be displayed on page using a *widget*.  Right.

And that should get the tests passing!  If you're curious to see what the form
HTML actually looks like, why not temporarily put a ``print form.as_p()`` at
the end of the test?   Print statements in tests can be very useful for
exploratory programming... You could try ``form.as_table()`` too if you like...

Right, where where we?  Let's do a quick check of the functional tests.

(*incidentally, are you rather bored of watching the FT run through the admin
test each time?  If so, you can temporarily disable it by renaming its test
method from* ``test_can_create_new_poll_via_admin_site`` *to*
``DONTtest_can_create_new_poll_via_admin_site`` *that's called "Dontifying"...
you do have to be careful not to forget about your dontified tests though!*)

    python manage.py test fts
    [...]
    AssertionError: 0 != 3

Ah yes, we still haven't actually *used* the form yet!  Let's go back to our
``SinglePollViewTest``, and a new test that checks we use our form)

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    class SinglePollViewTest(TestCase):

        def test_page_shows_poll_title_and_no_votes_message(self):
            [...]
 

        def test_page_shows_choices_using_form(self):
            # set up a poll with choices
            poll1 = Poll(question='time', pub_date=timezone.now())
            poll1.save()
            choice1 = Choice(poll=poll1, choice="PM", votes=0)
            choice1.save()
            choice2 = Choice(poll=poll1, choice="Gardener's", votes=0)
            choice2.save()

            response = self.client.get('/poll/%d/' % (poll1.id, ))

            # check we've passed in a form of the right type
            self.assertTrue(isinstance(response.context['form'], PollVoteForm))

            # and check the form is being used in the template,
            # by checking for the choice text
            self.assertIn(choice1.choice, response.content)
            self.assertIn(choice2.choice, response.content)


Now the unit tests give us::

    python manage.py test polls
    [...]
    KeyError: 'form'

So back in ``views.py``:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        poll = Poll.objects.get(pk=poll_id)
        return render(request, 'poll.html', {'poll': poll, 'form': None})

Now::

    self.assertTrue(isinstance(response.context['form'], PollVoteForm))
    AssertionError: False is not true

So:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        poll = Poll.objects.get(pk=poll_id)
        form = PollVoteForm(poll=poll)
        return render(request, 'poll.html', {'poll': poll, 'form': form})

And::

    self.assertIn(choice3.choice, response.content)
    AssertionError: 'PM' not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n\n    <h2>6 times 7</h2>\n    <p>No-one has voted on this poll yet</p>\n  </body>\n</html>\n\n'


So, in ``polls/templates/poll.html``:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/home.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <p>No-one has voted on this poll yet</p>

        <h3>Add your vote</h3>
        {{form.as_p}}

        
      </body>
    </html>

And re-running the tests - oh, a surprise!::

    self.assertIn(choice4.choice, response.content)
    AssertionError: "Gardener's" not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>time</h2>\n\n    <p>No-one has voted on this poll yet</p>\n\n    <h3>Add your vote</h3>\n    <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="3" name="vote" /> PM</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="4" name="vote" /> Gardener&#39;s</label></li>\n</ul></p>\n\n    \n  </body>\n</html>\n'

Django has converted an apostrophe (``'``) into an html-compliant ``&#39;`` for
us. I suppose that's my come-uppance for trying to include British in-jokes in
my tutorial.  Let's implement a minor hack in our test:


.. sourcecode:: python
    :filename: mysite/polls/tests.py

        self.assertIn(choice1.choice, response.content.replace('&#39;', "'"))
        self.assertIn(choice2.choice, response.content.replace('&#39;', "'"))

And now we have passination::

    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.016s

    OK

So let's ask the FTs again!::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 84, in test_voting_on_a_new_poll
        'Moderately awesome',
    AssertionError: Lists differ: [u'Vote:', u'Very awesome', u'... != ['Very awesome', 'Quite awesom...

    First differing element 0:
    Vote:
    Very awesome

    First list contains 1 additional elements.
    First extra element 3:
    Moderately awesome

    - [u'Vote:', u'Very awesome', u'Quite awesome', u'Moderately awesome']
    ?  -----------                -                 -

    + ['Very awesome', 'Quite awesome', 'Moderately awesome']

    ----------------------------------------------------------------------

Hm, not quite according to the original plan - our form has auto-generated an
extra label which says "Vote:" above the radio buttons - well, since it doesn't
do any harm, for now maybe it's easiest to just change the FT:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # He also sees a form, which offers him several choices.
        # There are three options with radio buttons
        choice_inputs = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        self.assertEquals(len(choice_inputs), 3)

        # The buttons have labels to explain them
        choice_labels = choice_inputs = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
            'Vote:', # this label is auto-generated for the whole form
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])


The FT should now get a little further::

    NoSuchElementException: Message: u'Unable to locate element: {"method":"css selector","selector":"input[type=\'submit\']"}' 

There's no submit button on our form! When Django generates a form, it only
gives you the inputs for the fields you've defined, so no submit button (and no
``<form>`` tag either for that matter).

Well, a button is easy enough to add, although it may not do much... In the
template:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <p>No-one has voted on this poll yet</p>

        <h3>Add your vote</h3>
        {{form.as_p}}
        <input type="submit" />

        
      </body>
    </html>


And now... our tests get to the end!::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 125, in test_voting_on_a_new_poll
        self.fail('TODO')
    AssertionError: TODO
    ----------------------------------------------------------------------


Tune in next week for when we finish our tests, handle POST requests, and do
super-fun form validation too...


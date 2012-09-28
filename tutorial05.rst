Welcome to part 5 - this week we'll be looking at processing user input from
forms.

Tutorial 5: Processing form submissions
=======================================

Here's the outline of what we're going to do in this tutorial:

    * wire up our vote form so we can submit votes

    * amend our view to also handle POST requests

    * use helper functions on models

    * quite a lot of fiddling with presentational stuff!


Finishing the FT
----------------

Let's pick up from the ``TODO`` in our FT, and extend it to include viewing the
effects of submitting a vote on a poll. In ``fts/tests.py``:

.. sourcecode:: python
    :filename: mysite/fts/tests.py

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

        # But not "1 votes" -- Herbert is impressed at the attention to detail
        self.assertNotIn('1 votes', body_text)

        # Herbert suspects that the website isn't very well protected
        # against people submitting multiple votes yet, so he tries
        # to do a little astroturfing
        self.browser.find_element_by_css_selector("input[value='1']").click()
        self.browser.find_element_by_css_selector("input[type='submit']").click()

        # The page refreshes, and he sees that his choice has updated the
        # results.  it still says # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # But the page now says "2 votes"
        self.assertIn('2 votes', body_text)

        # Cackling manically over his l33t haxx0ring skills, he tries
        # voting for a different choice
        self.browser.find_element_by_css_selector("input[value='2']").click()
        self.browser.find_element_by_css_selector("input[type='submit']").click()

        # Now, the percentages update, as well as the votes
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('67 %: Very awesome', body_text)
        self.assertIn('33 %: Quite awesome', body_text)
        self.assertIn('3 votes', body_text)

        # Satisfied, he goes back to sleep

If you run the FTs, you should see something like this::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 126, in test_voting_on_a_new_poll
        self.assertIn('100 %: Very awesome', body_text)
    AssertionError: '100 %: Very awesome' not found in u'Poll Results\nHow awesome is Test-Driven Development?\nNo-one has voted on this poll yet\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

    ----------------------------------------------------------------------
    Ran 1 test in 5.510s

What's happening is that clicking the submit button has no effect - we just
stay on the voting page. So, we'll need to wire up our view so that it deals
with form submission.  Let's open up ``polls/tests.py``. We need to find the test
that deals with our view.

At this point, you might find it's getting a little hard to find your way
around ``polls/tests.py`` - the file is getting a little cluttered.  I think it's
time to do some *refactoring*, and move things around a bit.


Refactoring the tests
---------------------

Refactoring means making changes to your code that have no functional impact -
and you can refactor your test code as well as your production code.  The
purpose of refactoring is usually to try and make your code more legible, less
complex, or to make the architecture neater. And the most important thing about
refactoring is: you need to make sure you don't break anything!  That's why
having good tests is absolutely essential to trouble-free refactoring

So, our objective is to separate out our tests.py into separate files for the
view tests, the model tests and the form tests - so that we have a
``test_views.py`` to match ``views.py``, a ``test_models.py`` to match
``models.py``, and so on.

Let's start by running all our unit tests, making sure they all pass, *and
making a note of how many of them there are* - we don't want to lose any in the
process!::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.016s

    OK

Right, 9 tests. Now, although our objective is to move to spreading our tests
into 3 different files, we're going to take several small steps to get there.
Then, at each stage, we can re-run our tests to make sure everything still
works.

The way the django test runner works is that it runs all the tests it can find
in each application, in a python module called ``tests``. Currently, that's a
file called ``tests.py``.  But we can change it into a subfolder, by doing
this:

    * create a new folder inside ``polls`` called ``tests``

    * add a ``__init__.py`` file inside the ``tests`` folder, to make it into
      an importable Python module

    * move the current ``polls/tests.py`` into the ``polls/tests/`` folder

    * finally, ``import`` all of the tests from ``tests.py`` into the
      ``__init__.py``

Depending on your operating system, that could look something like this::

    mkdir polls/tests
    mv polls/tests.py polls/tests
    touch polls/tests/__init__.py

Then, edit ``polls/tests/__init__.py``, and add the ``import``:

.. sourcecode:: python
    :filename: mysite/polls/tests/__init__.py

    from polls.tests.tests import *

Your tree will look something like this::

    `-- polls
        |-- admin.py
        |-- forms.py
        |-- __init__.py
        |-- models.py
        |-- templates
        |   |-- home.html
        |   `-- poll.html
        |-- tests
        |   |-- __init__.py
        |   `-- tests.py
        `-- views.py



At this point, we should be able to run the tests again. Let's do so, and check
that exactly the same number of them get run::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.033s

    OK
    Destroying test database for alias 'default'...


Hooray!  Now we have our test in a subfolder, we can start moving them out into
different files.  Again, we do this step by step.  Let's start by moving all
the model tests into a file called ``test_models.py``.  You'll need to move the
following classes:

    * ``PollModelTest``

    * ``ChoiceModelTest``

The way I chose to do it was:

    * Make a copy of ``tests.py``, and save it as ``test_models.py``

    * Delete all lines after line 81 from ``test_models.py``, leaving our two
      model tests

    * The, delete lines 8-81 from ``tests.py``, leaving only non-model tests

    * Finally, tidy up a few unused imports

OK, is the job done?  Let's try re-running our tests::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.014s

    OK

Ah, no - only 4 tests.  We've lost 5 somewhere.  That's because we need to make
sure that we import all tests into the ``tests/__init__.py``

.. sourcecode:: python
    :filename: mysite/polls/tests/__init__.py

    from mysite.polls.tests.tests import *
    from mysite.polls.tests.test_models import *

And now::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.016s

    OK

That's better.  Small, baby steps, with a quick check at each stage that everything still works... 

Now, if you're anything like I was when I was first introduced to this method,
you'll be screaming out, internally  - "Come on!  We could easily just do all
this stuff in one go!"... And, maybe that's even true.  But then, think back to
those times you've started off on a mission to refactor your code, and you've
just dived straight in.  You make a bunch of changes here, and then you move
onto that part there, and then you remember you also wanted to change this
thing back here, and then you just have to copy and paste these bits there,
rename this, and while we're at it we'll just do this and then, oh gosh where
was I again?  Pretty soon you find yourself at the bottom of a depth-first
tree, with no idea of how to get back to where you started, and no idea of what
you need to do to get it all working again.

So think back to all those times, and maybe erring on the side of caution isn't
so bad.  Once you get used to it, you'll find you can fly through it!

Anyways - next, let's do the views tests. Here's the way I did it:

  * Save a copy of ``tests.py`` as ``test_views.py``

  * Delete ``PollsVoteFormTest`` from ``test_views.py``

  * Delete ``HomePageViewTest`` and ``SinglePollViewTest`` from ``tests.py``

  * add ``from mysite.polls.tests.test_views import *`` to ``polls/tests/__init__,py``

  * tidy up imports

Re-running the tests, everything looks ok::

    $ python manage.py test polls 
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.017s

    OK

And our final step is to rename ``tests.py`` to ``test_forms.py``.  We'll need
to change the import too:

.. sourcecode:: python
    :filename: mysite/polls/tests/__init__.py

    from mysite.polls.tests.test_forms import *
    from mysite.polls.tests.test_models import *
    from mysite.polls.tests.test_views import *

Re-running the tests should give us 9 tests again, and we end up with 3 much
more manageable, shorter files.  Hooray.  

At this stage your polls app should look something like this::

    `-- polls
        |-- __init__.py
        |-- admin.py
        |-- forms.py
        |-- models.py
        |-- templates
        |   |-- home.html
        |   `-- poll.html
        |-- tests
        |   |-- __init__.py
        |   |-- test_forms.py
        |   |-- test_models.py
        |   `-- test_views.py
        `-- views.py

Pretty neat and tidy! Let's get back to what we were doing...


Dealing with POST requests in a view
------------------------------------

The normal pattern in Django is to use the view that renders your form for GET
requests, to also process form submissions via POST.  The main reason is that
it makes it easy to show form validation errors to the user...

The Django Test Client can generate POST requests as easily as GET ones, we
just need to tell it what the data should be. Let's write a new test in
``polls/tests/test_views.py`` - we can copy a fair bit from the one above it...

.. sourcecode:: python
    :filename: mysite/polls/tests/test_views.py


    class SinglePollViewTest(TestCase):

        def test_page_shows_choices_using_form(self):
            [...]

        def test_view_can_handle_votes_via_POST(self):
            # set up a poll with choices
            poll1 = Poll(question='6 times 7', pub_date=timezone.now())
            poll1.save()
            choice1 = Choice(poll=poll1, choice='42', votes=1)
            choice1.save()
            choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=3)
            choice2.save()

            # set up our POST data - keys and values are strings
            post_data = {'vote': str(choice2.id)}

            # make our request to the view
            poll_url = '/poll/%d/' % (poll1.id,)
            response = self.client.post(poll_url, data=post_data)

            # retrieve the updated choice from the database
            choice_in_db = Choice.objects.get(pk=choice2.id)

            # check it's votes have gone up by 1
            self.assertEquals(choice_in_db.votes, 4)

            # always redirect after a POST - even if, in this case, we go back
            # to the same page.
            self.assertRedirects(response, poll_url)

Right, let's see how it fails, first::

    ======================================================================
    FAIL: test_view_can_handle_votes_via_POST (mysite.polls.tests.test_views.SinglePollViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/../mysite/polls/tests/test_views.py", line 98, in test_view_can_handle_votes_via_POST
        self.assertEquals(choice_in_db.votes, 4)
    AssertionError: 3 != 4

    ----------------------------------------------------------------------

So, the first thing to do is increase the "votes" counter on the appropriate
Choice object... Django puts POST data into a special dictionary on the request
object, ``request.POST``, so let's use that - I'm adding three new lines at the
beginning of the view:


.. sourcecode:: python
    :filename: mysite/polls/views.py

    from polls.models import Choice, Poll
    [...]

    def poll(request, poll_id):
        choice = Choice.objects.get(id=request.POST['vote'])
        choice.votes += 1
        choice.save()

        poll = Poll.objects.get(pk=poll_id)
        form = PollVoteForm(poll=poll)
        return render(request, 'poll.html', {'poll': poll, 'form': form})


Let's see what the tests think::

    $ ./manage.py test polls
    Creating test database for alias 'default'...
    .......EEF
    ======================================================================
    ERROR: test_page_shows_choices_using_form (polls.tests.test_views.SinglePollViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/mysite/polls/tests/test_views.py", line 76, in test_page_shows_choices_using_form
        response = client.get('/poll/%d/' % (poll1.id, ))
      File "/usr/local/lib/python2.7/dist-packages/django/test/client.py", line 439, in get
        response = super(Client, self).get(path, data=data, **extra)
      File "/usr/local/lib/python2.7/dist-packages/django/test/client.py", line 244, in get
        return self.request(**r)
      File "/usr/local/lib/python2.7/dist-packages/django/core/handlers/base.py", line 111, in get_response
        response = callback(request, *callback_args, **callback_kwargs)
      File "/home/harry/workspace/mysite/polls/views.py", line 13, in poll
        choice = Choice.objects.get(id=request.POST['vote'])
      File "/usr/local/lib/python2.7/dist-packages/django/utils/datastructures.py", line 258, in __getitem__
        raise MultiValueDictKeyError("Key %r not found in %r" % (key, self))
    MultiValueDictKeyError: "Key 'vote' not found in <QueryDict: {}>"

    ======================================================================
    ERROR: test_page_shows_poll_title_and_no_votes_message (mysite.polls.tests.test_views.SinglePollViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/../mysite/polls/tests/test_views.py", line 57, in test_page_shows_poll_title_and_no_votes_message
      [...]
    MultiValueDictKeyError: "Key 'vote' not found in <QueryDict: {}>"

    ======================================================================
    ERROR: test_view_can_handle_votes_via_POST (mysite.polls.tests.test_views.SinglePollViewTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/../mysite/polls/tests/test_views.py", line 105, in test_view_can_handle_votes_via_POST
        self.assertRedirects(response, poll_url)
        AssertionError: Response didn't redirect as expected: Response code was 200 (expected 302)

    ----------------------------------------------------------------------
    Ran 9 tests in 0.031s

Oh dear - although we've got our POST test a little bit further along, we seem
to have broken 2 other tests.  You might argue, it was pretty obvious that was
going to happen, because I've introduced code to upvote choices which is
applied for both GET and POST requests - I should have checked whether the
request was a POST or a GET, and used an ``if``.  And, in fact, it was pretty
obvious - I was being deliberately stupid, and made that mistake on purpose.
The point was to demonstrate how TDD can save you from your own stupidity, by
telling you immediately when you break anything...  Save those brain cells for
the *really* hard problems.

So, Django tells us whether a request was a GET or a POST inside the ``method``
attribute.  Let's add an ``if``:

.. sourcecode:: python
    :filename: mysite/polls/views.py

    def poll(request, poll_id):
        if request.method == 'POST':
            choice = Choice.objects.get(id=request.POST['vote'])
            choice.votes += 1
            choice.save()

        poll = Poll.objects.get(pk=poll_id)
        form = PollVoteForm(poll=poll)
        return render(request, 'poll.html', {'poll': poll, 'form': form})

And testing...::

    ERROR: test_view_can_handle_votes_via_POST (mysite.polls.tests.test_views.SinglePollViewTest)
    AssertionError: Response didn't redirect as expected: Response code was 200 (expected 302)


Right, now we need to do our redirect (*Always redirect after a POST* -
http://www.theserverside.com/news/1365146/Redirect-After-Post).  Django has a
class called ``HttpResponseRedirect`` for this, which takes a URL.  We'll use
the ``reverse`` function from the last tutorial to get the right URL...

.. sourcecode:: python
    :filename: mysite/polls/views.py

    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect
    [...]

    def poll(request, poll_id):
        if request.method == 'POST':
            choice = Choice.objects.get(id=request.POST['vote'])
            choice.votes += 1
            choice.save()
            return HttpResponseRedirect(reverse('polls.views.poll', args=[poll_id,]))

        poll = Poll.objects.get(pk=poll_id)
        form = PollVoteForm(poll=poll)
        return render(request, 'poll.html', {'poll': poll, 'form': form})

Lovely!  let's see that at work::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    .........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.023s

    OK

Hooray!  Let's see if it gets the FT any further::

    $ python manage.py test fts
    [...]

    AssertionError: '100 %: Very awesome' not found in u'Poll Results\nHow awesome is Test-Driven Development?\nNo-one has voted on this poll yet\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

Nope.  We still have to get our page to reflect the percentage of votes.  Let's
make a quick test in ``test_views``:

.. sourcecode:: python
    :filename: mysite/polls/tests/test_views.py

    def test_view_shows_percentage_of_votes(self):
        # set up a poll with choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=1)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=2)
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll1.id, ))

        # check the percentages of votes are shown, sensibly rounded
        self.assertIn('33 %: 42', response.content)
        self.assertIn('67 %: The Ultimate Answer', response.content)

        # and that the 'no-one has voted' message is gone
        self.assertNotIn('No-one has voted', response.content)


    def test_view_can_handle_votes_via_POST(self):
        [...]

Running it gives::

    AssertionError: '33 %: 42' not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>6 times 7</h2>\n\n    <p>No-one has voted on this poll yet</p>\n\n    <h3>Add your vote</h3>\n    <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n    <input type="submit" />\n\n    \n  </body>\n</html>\n'


Which is all very well - but, actually, the view (or the template) aren't
really the right place to calculate percentage figures.  Let's hang that off
the model, as a custom function instead.  This test should make my intentions
clear.  In ``polls/tests/test_models.py``:

.. sourcecode:: python
    :filename: mysite/polls/tests/test_models.py

    def test_choice_can_calculate_its_own_percentage_of_votes(self):
        poll = Poll(question='who?', pub_date=timezone.now())
        poll.save()
        choice1 = Choice(poll=poll,choice='me',votes=2)
        choice1.save()
        choice2 = Choice(poll=poll,choice='you',votes=1)
        choice2.save()

        self.assertEquals(choice1.percentage(), 67)
        self.assertEquals(choice2.percentage(), 33)

Self-explanatory?  Let's implement.  We should now get a new test error::

    $ python manage.py test polls
    .E........F
    AttributeError: 'Choice' object has no attribute 'percentage'


Let's give ``Choice`` a percentage function. In ``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py


    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def percentage(self):
            pass

Re-running the tests::

    self.assertEquals(choice1.percentage(), 66)
    AssertionError: None != 67

And implementing:

.. sourcecode:: python
    :filename: mysite/polls/models.py

    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        return 100 * self.votes / total_votes_on_poll

Ah, not quite::

    self.assertEquals(choice1.percentage(), 67)
    AssertionError: 66 != 67

Darn that integer division! Let's try this:

.. sourcecode:: python
    :filename: mysite/polls/models.py

    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        return round(100.0 * self.votes / total_votes_on_poll)


That gets down from 2 failing tests to 1 failing test. Now let's use our new
percentage function in our template, ``polls/templates/poll.html``
            
.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <ul>
        {% for choice in poll.choice_set.all %}
          <li>{{ choice.percentage }} %: {{ choice.choice }}</li>
        {% endfor %}
        </ul>

        <p>No-one has voted on this poll yet</p>

        <h3>Add your vote</h3>
        {{form.as_p}}
        <input type="submit" />

        
      </body>
    </html>


Let's try re-running our tests now::

    ........E.F
    [...]
    TemplateSyntaxError: Caught ZeroDivisionError while rendering: float division by zero
    [...]
    AssertionError: '33 %: 42' not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>6 times 7</h2>\n\n    <ul>\n    \n      <li>33.0 %: 42</li>\n    \n      <li>67.0 %: The Ultimate Answer</li>\n    \n    </ul>\n\n    <p>No-one has voted on this poll yet</p>\n\n    <h3>Add your vote</h3>\n    <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n    <input type="submit" />\n\n    \n  </body>\n</html>\n'

    FAILED (failures=1, errors=1)


Oh no!  Bad to worse!  Our percentage function really is refusing to make our
lives easy - it's susceptible to zero-division errors, and it's producing
floats rather than nice printable percentages... Let's fix that.  (but, again,
notice the way it's the tests picking up all these little bugs for us, rather
than us having to try and anticipate them all in advance, or test all the edge
cases manually...)

So, let's make our percentage function return a proper, accurate float
representation of the percentage (or as accurate as floating-point arithmetic
will allow), and we'll handle the presentation issues in the template. We'll
also make it handle the 0-case.

.. sourcecode:: python
    :filename: mysite/polls/tests/test_models.py

    def test_choice_can_calculate_its_own_percentage_of_votes(self):
        poll = Poll(question='who?', pub_date=timezone.now())
        poll.save()
        choice1 = Choice(poll=poll,choice='me',votes=2)
        choice1.save()
        choice2 = Choice(poll=poll,choice='you',votes=1)
        choice2.save()

        self.assertEquals(choice1.percentage(), 100 * 2 / 3.0)
        self.assertEquals(choice2.percentage(), 100 * 1 / 3.0)

        # also check 0-votes case
        choice1.votes = 0
        choice1.save()
        choice2.votes = 0
        choice2.save()
        self.assertEquals(choice1.percentage(), 0)
        self.assertEquals(choice2.percentage(), 0)

Re-run the tests::

    self.assertEquals(choice1.percentage(), 100 * 2 / 3.0)
    AssertionError: 67.0 != 66.66666666666667

Removing the ``round()``...

.. sourcecode:: python
    :filename: mysite/polls/models.py

        def percentage(self):
            total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
            return 100.0 * self.votes / total_votes_on_poll


And now we get the 0-case error::

    return 100.0 * self.votes / sum(c.votes for c in self.poll.choice_set.all())
    ZeroDivisionError: float division by zero

Which we can fix with a ``try/except`` (*Better to ask for forgiveness than for
permission*)
 
.. sourcecode:: python
    :filename: mysite/polls/models.py

    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        try:
            return 100.0 * self.votes / total_votes_on_poll
        except ZeroDivisionError:
            return 0


Phew.  That takes us down to just one final test error::

    ..........F
    ======================================================================
    FAIL: test_view_shows_percentage_of_votes (mysite.polls.tests.test_views.SinglePollViewTest)
    self.assertNotIn('No-one has voted', response.content)
    AssertionError: 'No-one has voted' unexpectedly found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>6 times 7</h2>\n\n    <ul>\n    \n      <li>33.3333333333 %: 42</li>\n    \n      <li>66.6666666667 %: The Ultimate Answer</li>\n    \n    </ul>\n\n    <p>No-one has voted on this poll yet</p>\n\n    <h3>Add your vote</h3>\n    <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n    <input type="submit" />\n\n    \n  </body>\n</html>\n'

Now, how are we going to decide on whether to show or hide this "no votes yet"
message?  Ideally, we want to be able to ask the Poll object its total number
of votes... That might come in useful elsewhere too...

Let's hope this test/code cycle is self-explanatory. Start with
``test_models.py``:

.. sourcecode:: python
    :filename: mysite/polls/tests/test_models.py

    class PollModelTest(TestCase):
        [...]

        def test_poll_can_tell_you_its_total_number_of_votes(self):
            p = Poll(question='where',pub_date=timezone.now())
            p.save()
            c1 = Choice(poll=p,choice='here',votes=0)
            c1.save()
            c2 = Choice(poll=p,choice='there',votes=0)
            c2.save()

            self.assertEquals(p.total_votes(), 0)

            c1.votes = 1000
            c1.save()
            c2.votes = 22
            c2.save()
            self.assertEquals(p.total_votes(), 1022)

tests::

    AttributeError: 'Poll' object has no attribute 'total_votes'

``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

        def __unicode__(self):
            return self.question


        def total_votes(self):
            pass

tests::

    AssertionError: None != 0

``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

        def total_votes(self):
            return 0

(oh yeah, TDD.  You love it).  Tests::

    AssertionError: 0 != 1022

Good. ``models.py``

.. sourcecode:: python
    :filename: mysite/polls/models.py

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())

And that's a pass.  Now, does that ``sum`` remind you of anything.  Let's
refactor::


    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def percentage(self):
            try:
                return 100.0 * self.votes / self.poll.total_votes()
            except ZeroDivisionError:
                return 0

Re-running the tests, all the right ones still pass.  Another one of the reasons
that TDD is so great is that it encourages you to refactor at will - because
your code is well tested, you can always know whether or not your refactor
has gone correctly, or whether anything was broken.

Let's finally get onto our little message. Back in our template,
``polls/templates/poll.html``:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <ul>
        {% for choice in poll.choice_set.all %}
          <li>{{ choice.percentage }} %: {{ choice.choice }}</li>
        {% endfor %}
        </ul>


        {% if poll.total_votes == 0 %}
          <p>No-one has voted on this poll yet</p>
        {% endif %}

        <h3>Add your vote</h3>
        {{form.as_p}}
        <input type="submit" />

        
      </body>
    </html>

And re-run the tests::

    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 0.043s
    OK

At last!  What about the FT?::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/tddjango_site/source/mysite/fts/tests.py", line 126, in test_voting_on_a_new_poll
        self.assertIn('100 %: Very awesome', body_text)
    AssertionError: '100 %: Very awesome' not found in u'Poll Results\nHow awesome is Test-Driven Development?\n0 %: Very awesome\n0 %: Quite awesome\n0 %: Moderately awesome\nNo-one has voted on this poll yet\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

    ----------------------------------------------------------------------
    Ran 1 test in 5.677s

Hmm, not quite.  What is missing?  The "submit" button doesn't seem to be
working... Ah! Yes - we haven't actually wired up our form yet.  Django's
``form.as_p()`` function doesn't actually give you a ``<form>`` tag - you have
to do that yourself, which gives you the choice over where the form sends its
data.  Let's do that, in the template, ``polls/templates/poll.html``:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <ul>
        {% for choice in poll.choice_set.all %}
          <li>{{ choice.percentage }} %: {{ choice.choice }}</li>
        {% endfor %}
        </ul>


        {% if poll.total_votes == 0 %}
          <p>No-one has voted on this poll yet</p>
        {% endif %}

        <h3>Add your vote</h3>
        <form method="POST" action="">
          {{form.as_p}}
          <input type="submit" />
        </form>

        
      </body>
    </html>

Re-running the FT, we get::

    AssertionError: '100 %: Very awesome' not found in u'Forbidden (403)\nCSRF verification failed. Request aborted.\nMore information is available with DEBUG=True.'

Pretty helpful, as error messages go.  Let's add an amazing Django voodoo CSRF
tag:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <form method="POST" action="">
      {% csrf_token %}
      {{form.as_p}}
      <input type="submit" />
    </form>

And now?::

    AssertionError: '100 %: Very awesome' not found in u'Poll Results\nHow awesome is Test-Driven Development?\n100.0 %: Very awesome\n0.0 %: Quite awesome\n0.0 %: Moderately awesome\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

Still not quite, arg! Just a tiny formatting error though.  We can fix this
using one of Django's built-in template filters:

https://docs.djangoproject.com/en/1.4/ref/templates/builtins/

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <ul>
    {% for choice in poll.choice_set.all %}
      <li>{{ choice.percentage|floatformat }} %: {{ choice.choice }}</li>
    {% endfor %}
    </ul>


Now what?::

    FAIL: test_voting_on_a_new_poll (tests.TestPolls)
    AssertionError: '1 vote' not found in u'Poll Results\nHow awesome is Test-Driven Development?\n100 %: Very awesome\n0 %: Quite awesome\n0 %: Moderately awesome\nAdd your vote\nVote:\nVery awesome\nQuite awesome\nModerately awesome'

Aha, looks like that ``total_votes`` function is going to come in useful again!

Let's add a tiny test to our ``test_views.py``:

.. sourcecode:: python 
    :filename: mysite/polls/tests/test_views.py

    def test_view_shows_total_votes(self):
        # set up a poll with choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=1)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=2)
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll1.id, ))
        self.assertIn('3 votes', response.content)

        # also check we only pluralise "votes" if necessary. details!
        choice2.votes = 0
        choice2.save()
        response = self.client.get('/poll/%d/' % (poll1.id, ))
        self.assertIn('1 vote', response.content)
        self.assertNotIn('1 votes', response.content)


Running those tests::

    FAIL: test_view_shows_percentage_of_votes_and_total_votes (mysite.polls.tests.test_views.SinglePollViewTest)
    AssertionError: '33 %: 42' not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>6 times 7</h2>\n\n    <ul>\n    \n      <li>33.3 %: 42</li>\n    \n      <li>66.7 %: The Ultimate Answer</li>\n    \n    </ul>\n\n\n    \n\n    <h3>Add your vote</h3>\n    <form method="POST" action="">\n      <div style=\'display:none\'><input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'ac03d928c29ccbfe6fd0828aec8ede4e\' /></div>\n      <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n      <input type="submit" />\n    </form>\n\n    \n  </body>\n</html>\n'

    FAIL: test_view_shows_total_votes (mysite.polls.tests.test_views.SinglePollViewTest)
    AssertionError: '3 votes' not found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    \n    <h2>6 times 7</h2>\n\n    <ul>\n    \n      <li>33.3 %: 42</li>\n    \n      <li>66.7 %: The Ultimate Answer</li>\n    \n    </ul>\n\n\n    \n\n    <h3>Add your vote</h3>\n    <form method="POST" action="">\n      <div style=\'display:none\'><input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'d9fd2b61be1299d84b48f4c378b15ec3\' /></div>\n      <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n      <input type="submit" />\n    </form>\n\n    \n  </body>\n</html>\n'


Ah, aside from our expected failure, it looks like we also have a minor
regression. Getting this presentational stuff right is fiddly!  Still, the fix
isn't too difficult, back in our template, let's tweak the ``floatformat``, and
also add in the ``total_votes``:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

    <html>
      <body>
        <h1>Poll Results</h1>
        
        <h2>{{poll.question}}</h2>

        <ul>
        {% for choice in poll.choice_set.all %}
          <li>{{ choice.percentage|floatformat:0 }} %: {{ choice.choice }}</li>
        {% endfor %}
        </ul>


        {% if poll.total_votes != 0 %}
          <p>{{ poll.total_votes }} votes</p>
        {% else %}
          <p>No-one has voted on this poll yet</p>
        {% endif %}

        <h3>Add your vote</h3>
        <form method="POST" action="">
          {% csrf_token %}
          {{form.as_p}}
          <input type="submit" />
        </form>

        
      </body>
    </html>

Another unit test run::

    AssertionError: '1 votes' unexpectedly found in '<html>\n  <body>\n    <h1>Poll Results</h1>\n    <h2>6 times 7</h2>\n    <ul>\n      \n        <li>100 %: 42</li>\n      \n        <li>0 %: The Ultimate Answer</li>\n      \n    </ul>\n\n    \n      <p>1 votes</p>\n    \n\n    <h3>Add your vote</h3>\n    <form method="POST" action="">\n      <div style=\'display:none\'><input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'kXRyayBw8agkbj2vgTXM1OEyMQjMzXWY\' /></div>\n      <p><label for="id_vote_0">Vote:</label> <ul>\n<li><label for="id_vote_0"><input type="radio" id="id_vote_0" value="1" name="vote" /> 42</label></li>\n<li><label for="id_vote_1"><input type="radio" id="id_vote_1" value="2" name="vote" /> The Ultimate Answer</label></li>\n</ul></p>\n      <input type="submit" />\n    </form>\n\n\n  </body>\n</html>\n\n'

Ah yes, we want it to say "1 vote", not "1 votes".  Django's template system
has a helpful ``pluralize`` function for this:

.. sourcecode:: html+django
    :filename: mysite/polls/templates/poll.html

        <p>{{ poll.total_votes }} vote{{ poll.total_votes|pluralize }}</p>

Unit tests snow pass::

    $ python manage.py test polls
    Creating test database for alias 'default'...
    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 0.061s

Now, how about those functional tests?::

    $ python manage.py test fts

    AssertionError: TODO


That looks good. How about our fts?::

    $ python manage.py test fts
    Ran 2 tests in 9.606s
    OK


Well, that feels like a nice place to break until next time.  See you soon!


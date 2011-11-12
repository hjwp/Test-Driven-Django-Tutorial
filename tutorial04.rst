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
            self.assertIn(poll2.name, response.content)
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


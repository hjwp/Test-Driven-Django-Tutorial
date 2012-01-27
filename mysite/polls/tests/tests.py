from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from polls.forms import PollVoteForm
from polls.models import Choice, Poll


class TestHomePageView(TestCase):

    def test_root_url_shows_links_to_all_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date='2001-01-01')
        poll2.save()

        client = Client()
        response = client.get('/')

        # check we've used the "home.html" template
        template_names_used = [t.name for t in response.templates]
        self.assertIn('home.html', template_names_used)

        # check we've passed the polls to the template
        polls_in_context = response.context['polls']
        self.assertEquals(list(polls_in_context), [poll1, poll2])

        # check the poll names appear on the page
        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)

        # check the page also contains the urls to individual polls pages
        poll1_url = reverse('mysite.polls.views.poll', args=[poll1.id,])
        self.assertIn(poll1_url, response.content)
        poll2_url = reverse('mysite.polls.views.poll', args=[poll2.id,])
        self.assertIn(poll2_url, response.content)


class TestSinglePollView(TestCase):

    def test_page_shows_poll_title_and_no_votes_message(self):
        # set up two polls, to check the right one gets used
        poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
        choice2.save()
        poll2 = Poll(question='time', pub_date='2001-01-01')
        poll2.save()
        choice3 = Choice(poll=poll2, choice='PM', votes=0)
        choice3.save()
        choice4 = Choice(poll=poll2, choice="Gardener's", votes=0)
        choice4.save()

        client = Client()
        response = client.get('/poll/%d/' % (poll2.id, ))

        # check we use the right template
        self.assertEquals(response.templates[0].name, 'poll.html')

        # check we've passed the right poll into the context
        self.assertEquals(response.context['poll'], poll2)

        # check the poll's question appears on the page
        self.assertIn(poll2.question, response.content)

        # check our 'no votes yet' message appears
        self.assertIn('No-one has voted on this poll yet', response.content)

        # check we've passed in a form of the right type
        self.assertTrue(isinstance(response.context['form'], PollVoteForm))

        # and check the check the form is being used in the template,
        # by checking for the choice text
        self.assertIn(choice3.choice, response.content)
        self.assertIn(choice4.choice, response.content.replace('&#39;', "'"))


    def test_view_can_handle_votes_via_POST(self):
        pass


class TestPollsVoteForm(TestCase):

    def test_form_renders_poll_choices_as_radio_inputs(self):
        # set up a poll with a couple of choices
        poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
        choice2.save()

        # set up another poll to make sure we only see the right choices
        poll2 = Poll(question='time', pub_date='2001-01-01')
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


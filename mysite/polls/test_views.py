from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from polls.forms import PollVoteForm
from polls.models import Choice, Poll


class TestAllPollsView(TestCase):

    def test_root_url_shows_links_to_all_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date='2001-01-01')
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date='2001-01-01')
        poll2.save()

        # get the root URL
        client = Client()
        response = client.get('/')

        # check the right template was used
        template_names_used = [t.name for t in response.templates]
        self.assertIn('polls.html', template_names_used)

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

        # get the url for poll 2
        client = Client()
        response = client.get('/poll/%d/' % (poll2.id, ))

        # check we used the right template
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
        self.assertIn(choice4.choice, response.content.replace('&#39;', "'")) # little hack for html-escaping


from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll
from polls.views import home_page

class PollModelTest(TestCase):

    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        # start by creating a new Poll object with its "question" set
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()

        # check we can save it to the database
        poll.save()

        # now check we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)

        # and check that it's saved its two attributes: question and pub_date
        self.assertEquals(only_poll_in_database.question, "What's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)


    def test_string_representation(self):
        poll = Poll()
        poll.question = "Why?"
        self.assertEqual(unicode(poll), "Why?")



class ChoiceModelTest(TestCase):

    def test_creating_some_choices_for_a_poll(self):
        # start by creating a new Poll object
        poll = Poll()
        poll.question="What's up?"
        poll.pub_date = timezone.now()
        poll.save()

        # now create a Choice object
        choice = Choice()

        # link it with our Poll
        choice.poll = poll

        # give it some text
        choice.choice = "doin' fine..."

        # and let's say it's had some votes
        choice.votes = 3

        # save it
        choice.save()

        # try retrieving it from the database, using the poll object's reverse
        # lookup
        poll_choices = poll.choice_set.all()
        self.assertEquals(poll_choices.count(), 1)

        # finally, check its attributes have been saved
        choice_from_db = poll_choices[0]
        self.assertEquals(choice_from_db, choice)
        self.assertEquals(choice_from_db.choice, "doin' fine...")
        self.assertEquals(choice_from_db.votes, 3)

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)



class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_renders_home_template_with_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()
        request = HttpRequest()

        response = home_page(request)
        expected_html = render_to_string('home.html')

        # check template rendered correctly
        expected_html = render_to_string('home.html', {'current_polls': [poll1, poll2]})
        self.assertMultiLineEqual(response.content, expected_html)

        # check template includes all polls
        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)



class SinglePollViewTest(TestCase):

    def test_template_rendered_with_poll_and_choice_radio_buttons_and_no_votes(
            self
    ):
        # set up two polls, to check the right one is displayed
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        # add a couple of choices
        choice1 = Choice(poll=poll2, choice="42")
        choice1.save()
        choice2 = Choice(poll=poll2, choice="the Spice")
        choice2.save()

        response = self.client.get('/poll/%d/' % (poll2.id, ))

        # check we've used the poll template
        self.assertTemplateUsed(response, 'poll.html')

        # check we've passed the right poll into the context
        self.assertEquals(response.context['poll'], poll2)

        # check the poll's question appears on the page
        self.assertIn(poll2.question, response.content)

        # check our 'no votes yet' message appears
        self.assertIn('No-one has voted on this poll yet', response.content)

        # check the choices appear as radio buttons, with the
        # correct 'name' and 'value'
        self.assertIn(
            '<input type="radio" name="vote" value="%d" />' % (choice1.id,),
            response.content
        )
        self.assertIn(
            '<input type="radio" name="vote" value="%d" />' % (choice2.id,),
            response.content
        )
        # check there are labels too
        self.assertIn('<label>%s' % (choice1.choice,), response.content)
        self.assertIn('<label>%s' % (choice2.choice,), response.content)


    def test_poll_has_vote_form_which_posts_to_correct_url(self):
        poll = Poll.objects.create(question='question', pub_date=timezone.now())

        response = self.client.get('/poll/%d/' % (poll.id, ))

        self.assertIn(
            '<form method="POST" action="/poll/%d/vote">' % (poll.id,),
            response.content
        )
        self.assertIn(
            '<input type="submit"',
            response.content
        )

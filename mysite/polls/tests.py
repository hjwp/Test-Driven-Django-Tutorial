from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils import timezone
from polls.models import Choice, Poll
from polls.views import home_page
from polls import views

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
        self.assertEquals(choice_from_db.id, choice.id)
        self.assertEquals(choice_from_db.choice, "doin' fine...")
        self.assertEquals(choice_from_db.votes, 3)

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)



class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_renders_home_template_with_current_polls(self):
        # set up some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()
        request = HttpRequest()
        response = home_page(request)
        # render template with polls
        expected_html = render_to_string('home.html', {'current_polls': [poll1, poll2]})
        self.assertMultiLineEqual(response.content, expected_html)


    def test_url_for_individual_poll(self):
        # set up some polls
        poll = Poll(question='6 times 7', pub_date=timezone.now())
        poll.save()
        found = resolve('/poll/%d/' % (poll.id,))
        self.assertEqual(found.func, views.poll)
        self.assertEqual(found.args, (str(poll.id),))



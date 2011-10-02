import datetime
from django.test import TestCase
from polls.models import Poll

class TestPollsModel(TestCase):

    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        # start by creating a new Poll object and setting its 'question'
        poll = Poll()
        poll.question="What's up?"

        # check we can save it to the database
        poll.save()

        # check we can adjust its publication date
        poll.pub_date = datetime.datetime(2012, 12, 25)
        poll.save()

        # now check we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)

        # and check that it's saved its two attributes: question and pub_date
        self.assertEquals(only_poll_in_database.question, "What's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)



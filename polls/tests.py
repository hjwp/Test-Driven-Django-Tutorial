from django.test import TestCase
from polls.models import Poll

class TestPollsModel(TestCase):

    def test_creating_a_poll(self):
        poll = Poll()
        poll.save()
        self.assertEquals(poll.name, '')


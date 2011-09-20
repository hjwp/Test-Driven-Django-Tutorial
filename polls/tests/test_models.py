from django.test import TestCase
from polls.models import Poll

class TestPollsModel(TestCase):

    def test_init(self):
        poll = Poll()
        self.assertEquals(poll.name, '')


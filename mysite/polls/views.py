from django.shortcuts import render

from polls.forms import PollVoteForm
from polls.models import Poll

def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)


def poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    form = PollVoteForm(poll=poll)
    return render(request, 'poll.html', {'poll': poll, 'form': form})

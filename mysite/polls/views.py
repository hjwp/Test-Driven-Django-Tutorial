from django.shortcuts import render
from polls.models import Poll

def home_page(request):
    return render(request, 'home.html', {'current_polls': Poll.objects.all()})


def poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    return render(request, 'poll.html', {'poll': poll})

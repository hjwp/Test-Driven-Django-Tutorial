from django.shortcuts import render
from django.http import HttpResponse
from polls.models import Poll

def polls(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'polls.html', context)

def poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    return render(request, 'poll.html', {'poll': poll})

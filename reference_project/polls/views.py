from django.shortcuts import redirect, render
from polls.models import Choice, Poll

def home_page(request):
    return render(request, 'home.html', {'current_polls': Poll.objects.all()})


def poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    return render(request, 'poll.html', {'poll': poll})

def vote(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    choice = Choice.objects.get(id=request.POST['vote'])
    choice.votes += 1
    choice.save()
    return redirect('/poll/%d/' % (poll.id,))

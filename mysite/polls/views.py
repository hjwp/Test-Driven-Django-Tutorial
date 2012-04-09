from polls.models import Poll
from django.shortcuts import render

def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)


def poll():
    pass

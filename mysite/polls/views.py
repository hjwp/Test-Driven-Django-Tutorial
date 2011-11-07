from django.shortcuts import render
from polls.models import Poll

def polls(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'polls.html', context)

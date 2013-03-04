from django.shortcuts import render
from polls.models import Poll

def home_page(request):
    return render(request, 'home.html', {'current_polls': Poll.objects.all()})

def poll(request):
    pass

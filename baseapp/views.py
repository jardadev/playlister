from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    context = {'message': 'Hello, Django'}
    return render(request, 'baseapp/index.html', context)


def home(request):
    return HttpResponse("Welcome to home page!")

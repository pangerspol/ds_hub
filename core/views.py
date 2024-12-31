from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, welcome to Dressler Strickland Hub!")

# Create your views here.

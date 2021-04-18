from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, 'gausscourse/login.html')

@login_required
def home(request):
    return render(request, 'gausscourse/home.html')

def index(request):
    """return HttpResponse("Hello, world. You're at the polls index.")"""
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'gausscourse/index.html', context)

def test(request):
    """return HttpResponse("Hello, world. You're at the polls index.")"""
    course_list = [{'name':'name', 'start_date':'start_date', "finish_date":"finish_date" },
                   {'name':'sfjh', 'start_date':'rrrrrrrrrr', "finish_date":"dfjdjdyjdyj" },
                   {'name':'gjfj', 'start_date':'ggggggffff', "finish_date":"cvmn4565676" }]
    context = {'course_list': course_list}
    return render(request, 'gausscourse/test.html', context)

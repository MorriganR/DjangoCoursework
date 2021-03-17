from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Course
from django.contrib.auth.models import User

def index(request):
    """return HttpResponse("Hello, world. You're at the polls index.")"""
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'gausscourse/index.html', context)

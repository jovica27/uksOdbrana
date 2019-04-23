import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from django.views.generic import CreateView

from .models import Project
from .models import User
from .models import UserProject
from .models import Branch
from .models import Commit
from .models import Issue
from .models import IssueLabel
from .models import IssueAssignment
from .models import Milestone
from .models import Label
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


def index(request):
    return HttpResponse("Index");


def home(request):
    template = loader.get_template('uks/home.html')
    context = {}

    return HttpResponse(template.render(context, request))


def register(request):
    template = loader.get_template('uks/register.html')
    context = {}

    return HttpResponse(template.render(context, request))


def register_user(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']

    try:
        user = User.objects.get(username=username)
        messages.info(request, 'User with that username already exists!')
        return HttpResponseRedirect(reverse('uks:register'))

    except User.DoesNotExist:
        u = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        u.save()
        return HttpResponseRedirect(reverse('uks:login'))


def login(request):
    template = loader.get_template('uks/login.html')
    context = {}

    return HttpResponse(template.render(context, request))


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username, password=password)
        request.session['id'] = user.id
        return HttpResponseRedirect(reverse('uks:projects'))

    except User.DoesNotExist:
        messages.info(request, 'Wrong credentials!')
        return HttpResponseRedirect(reverse('uks:login'))


def logout(request):
    request.session['id'] = ''
    template = loader.get_template('uks/home.html')
    context = {}

    return HttpResponse(template.render(context, request))


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


def projects(request):
    user = User.objects.get(id=request.session['id'])

    p = list()
    user_projects = UserProject.objects.all()

    for up in user_projects:
        if up.user == user:
            p.append(up.project)

    template = loader.get_template('uks/projects.html')
    context = {
        'projects': p
    }

    return HttpResponse(template.render(context, request))


def project_create(request):
    project_name = request.POST['project_name']
    project_description = request.POST['project_description']

    p = Project(name=project_name, description=project_description)
    p.save()

    u = User.objects.get(id=request.session['id'])
    up = UserProject(project=p, user=u)
    up.save()

    return HttpResponseRedirect(reverse('uks:projects'))


def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    branches = Branch.objects.filter(project=project)
    issues = Issue.objects.filter(project=project)
    template = loader.get_template('uks/project_details.html')

    userProjects = UserProject.objects.filter(project=project.id)
    members = []

    for up in userProjects:
        members.append(up.user.username)

    context = {
        'project': project,
        'branches': branches,
        'members': members,
        'issues': issues
    }
    return HttpResponse(template.render(context, request))


def project_update(request, project_id):
    if request.method == 'POST':
        project_name = request.POST['project_name']
        project = Project.objects.get(id=project_id)
        project.name = project_name
        project.save()
        # return HttpResponseRedirect(reverse('uks:projects'))
        return project_details(request, project_id)


def project_delete(request, project_id):
    if request.method == 'POST':
        Project.objects.filter(id=project_id).delete()
        return HttpResponseRedirect(reverse('uks:projects'))


def project_add_member(request, project_id):
    if request.method == 'POST':
        member_username = request.POST['member_username']
        project = get_object_or_404(Project, id=project_id)
        print(member_username)
        u = get_object_or_404(User, username=member_username)

        found = UserProject.objects.filter(project=project.id, user=u.id).count()
        if found != 0:
            return HttpResponse("This member is already added")

        up = UserProject(project=project, user=u)
        up.save()
        # return HttpResponseRedirect(reverse('uks:projects'))
        return project_details(request, project_id)


def branch_details(request, project_id, branch_id):

    project = Project.objects.get(id=project_id)
    branch = Branch.objects.get(id=branch_id)
    template = loader.get_template('uks/branch_details.html')
    commits = Commit.objects.filter(branch=branch)
    context = {
        'project': project,
        'branch': branch,
        'commits': commits
    }
    return HttpResponse(template.render(context, request))


def branch_create(request, project_id):
    branch_name = request.POST['branch_name']
    p = get_object_or_404(Project, id=project_id)
    branch = Branch(name=branch_name, project=p)
    branch.save()
    return HttpResponseRedirect(reverse('uks:project_details', kwargs={'project_id':project_id}))


def branch_update(request, project_id, branch_id):
    if request.method == 'POST':
        branch_name = request.POST['branch_name']
        branch = Branch.objects.get(id=branch_id)
        branch.name = branch_name
        branch.save()
        # return HttpResponseRedirect(
        #     reverse('uks:project_details', kwargs={'project_id':project_id})
        # )
        return branch_details(request, project_id, branch_id)


def branch_delete(request, project_id, branch_id):
    if request.method == 'POST':
        Branch.objects.filter(id=branch_id).delete()
        return HttpResponseRedirect(reverse('uks:project_details', kwargs={'project_id':project_id}))
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
        project_description = request.POST['project_description']
        project = Project.objects.get(id=project_id)
        project.name = project_name
        project.project_description = project_description
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
	
	
def commit_details(request, project_id, branch_id, commit_id):

    project = Project.objects.get(id=project_id)
    branch = Branch.objects.get(id=branch_id)
    commit = Commit.objects.get(id=commit_id)

    template = loader.get_template('uks/commit_details.html')
    context = {
        'project': project,
        'branch': branch,
        'commit': commit
    }
    return HttpResponse(template.render(context, request))


def commit_create(request, project_id, branch_id):
    commit_message = request.POST['commit_message']
    p = get_object_or_404(Project, id=project_id)
    b = get_object_or_404(Branch, id=branch_id)
    commit_hash = get_random_string(length=32)
    creation_date = datetime.datetime.now()
    user = User.objects.get(id=request.session['id'])

    commit = Commit(
        message=commit_message,
        hash=commit_hash,
        creation_date=creation_date,
        branch=b,
        user=user
    )
    commit.save()
    return HttpResponseRedirect(
        reverse('uks:branch_details', kwargs={'project_id': project_id, 'branch_id': branch_id})
    )

def commit_delete(request, project_id, branch_id, commit_id):

    if request.method == 'POST':
        Commit.objects.filter(id=commit_id).delete()
        return HttpResponseRedirect(
            reverse('uks:branch_details',kwargs={'project_id':project_id, 'branch_id': branch_id})
        )

def issue_details(request, project_id, issue_id):
    project = Project.objects.get(id=project_id)
    issue = Issue.objects.get(id=issue_id)
    template = loader.get_template('uks/issue_details.html')
    milestones = Milestone.objects.filter(issue=issue)

    issue_labels = IssueLabel.objects.filter(issue=issue)
    labels = []

    all_labels = Label.objects.all()

    for issue_label in issue_labels:
        labels.append(issue_label.label)

    issue_assignments = IssueAssignment.objects.filter(issue=issue)
    assignees = []

    for issue_assignment in issue_assignments:
        assignees.append(issue_assignment.user)

    userProjects = UserProject.objects.filter(project=project.id)
    members = []

    for up in userProjects:
        members.append(up.user)

    context = {
        'project': project,
        'issue': issue,
        'milestones': milestones,
        'labels': labels,
        'all_labels': all_labels,
        'assignees': assignees,
        'members': members
    }
    return HttpResponse(template.render(context, request))


def issue_create(request, project_id):
    issue_name = request.POST['issue_name']
    issue_description = request.POST['issue_description']
    p = get_object_or_404(Project, id=project_id)
    issue = Issue(name=issue_name, description=issue_description, project=p)
    issue.save()
    return HttpResponseRedirect(reverse('uks:project_details', kwargs={'project_id':project_id}))


def issue_update(request, project_id, issue_id):
    if request.method == 'POST':
        issue_name = request.POST['issue_name']
        issue_description = request.POST['issue_description']
        issue = Issue.objects.get(id=issue_id)
        issue.name = issue_name
        issue.description = issue_description
        issue.save()
        # return HttpResponseRedirect(
        #     reverse('uks:project_details', kwargs={'project_id':project_id})
        # )
        return issue_details(request, project_id, issue_id)


def issue_delete(request, project_id, issue_id):
    if request.method == 'POST':
        Issue.objects.filter(id=issue_id).delete()
        return HttpResponseRedirect(reverse('uks:project_details',kwargs={'project_id':project_id}))

def issue_add_label(request, project_id, issue_id):
    if request.method == 'POST':
        label_name = request.POST['label_name']

        issue = get_object_or_404(Issue, id=issue_id)
        label = get_object_or_404(Label, name=label_name)

        found = IssueLabel.objects.filter(issue=issue.id, label=label.id).count()
        if found != 0:
            return HttpResponse("This label is already added")

        issue_label = IssueLabel(issue=issue, label=label)
        issue_label.save()
        return HttpResponseRedirect(reverse('uks:issue_details', kwargs={'project_id':project_id, 'issue_id': issue_id}))


def issue_add_assignee(request, project_id, issue_id):
    if request.method == 'POST':
        assignee_username = request.POST['assignee_username']
        issue = get_object_or_404(Issue, id=issue_id)

        assignee = get_object_or_404(User, username=assignee_username)

        found = IssueAssignment.objects.filter(issue=issue.id, user=assignee.id).count()
        if found != 0:
            return HttpResponse("This assignee is already added")

        assignment = IssueAssignment(issue=issue, user=assignee)
        assignment.save()
        return HttpResponseRedirect(reverse('uks:issue_details', kwargs={'project_id':project_id, 'issue_id': issue_id}))

def milestone_create(request, project_id, issue_id):
    milestone_name = request.POST['milestone_name']
    milestone_description = request.POST['milestone_description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    i = get_object_or_404(Issue, id=issue_id)
    milestone = Milestone(
        name=milestone_name,
        description=milestone_description,
        start_date=start_date,
        end_date=end_date,
        issue=i
    )
    milestone.save()
    return HttpResponseRedirect(
        reverse('uks:issue_details', kwargs={'project_id': project_id, 'issue_id': issue_id})
    )


def milestone_details(request, project_id, issue_id, milestone_id):
    project = Project.objects.get(id=project_id)
    issue = Issue.objects.get(id=issue_id)
    milestone = Milestone.objects.get(id=milestone_id)

    template = loader.get_template('uks/milestone_details.html')
    context = {
        'project': project,
        'issue': issue,
        'milestone': milestone
    }
    return HttpResponse(template.render(context, request))


def milestone_update(request, project_id, issue_id, milestone_id):
    if request.method == 'POST':
        milestone_name = request.POST['milestone_name']
        milestone_description = request.POST['milestone_description']
        end_date = request.POST['end_date']
        milestone = Milestone.objects.get(id=milestone_id)
        milestone.name = milestone_name
        milestone.description = milestone_description
        milestone.end_date = end_date
        milestone.save()
        # return HttpResponseRedirect(
        #     reverse('uks:issue_details', kwargs={'project_id':project_id, 'issue_id': issue_id})
        # )
        return milestone_details(request, project_id, issue_id, milestone_id)


def milestone_delete(request, project_id, issue_id, milestone_id):
    if request.method == 'POST':
        Milestone.objects.filter(id=milestone_id).delete()
        return HttpResponseRedirect(
            reverse('uks:issue_details',kwargs={'project_id':project_id, 'issue_id': issue_id})
)


def label_create(request):
    label_name = request.POST['label_name']
    label_description = request.POST['label_description']
    label_color = request.POST['label_color']
    label = Label(
        name=label_name,
        description=label_description,
        color=label_color
    )
    label.save()
    return HttpResponseRedirect(reverse('uks:label_list'))


def label_list(request):
    labels = Label.objects.all()
    template = loader.get_template('uks/label_list.html')
    context = {
        'labels': labels,
    }
    return HttpResponse(template.render(context, request))


def label_details(request, label_id):
    label = Label.objects.get(id=label_id)
    template = loader.get_template('uks/label_details.html')

    context = {
        'label': label,
    }
    return HttpResponse(template.render(context, request))


def label_update(request, label_id):
    if request.method == 'POST':
        label_name = request.POST['label_name']
        label_description = request.POST['label_description']
        label_color = request.POST['label_color']

        label = Label.objects.get(id=label_id)

        label.name = label_name
        label.description = label_description
        label.color = label_color
        label.save()
        return label_details(request, label_id)
        # return HttpResponseRedirect(reverse('vsc:label_list'))


def label_delete(request, label_id):
    if request.method == 'POST':
        Label.objects.filter(id=label_id).delete()
        return HttpResponseRedirect(reverse('uks:label_list'))

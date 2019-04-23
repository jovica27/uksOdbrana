from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^projects$', views.projects, name='projects'),
    url(r'^projects/create$', views.project_create, name='project_create'),
    url(r'^register$', views.register, name='register'),
    url(r'^register_user$', views.register_user, name='register_user'),
    url(r'^login$', views.login, name='login'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^logout$', views.logout, name='logout'),

    url(r'^projects/(?P<project_id>[0-9]+)$', views.project_details, name='project_details'),
    url(r'^projects/(?P<project_id>[0-9]+)/update', views.project_update, name="project_update"),
    url(r'^projects/(?P<project_id>[0-9]+)/delete', views.project_delete, name="project_delete"),
    url(r'^projects/(?P<project_id>[0-9]+)/add_member', views.project_add_member, name="project_add_member"),

    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)$', views.branch_details, name="branch_details"),
    url(r'^projects/(?P<project_id>[0-9]+)/branches$', views.branch_create, name="branch_create"),
    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/update', views.branch_update,
        name="branch_update"),
    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/delete', views.branch_delete,
        name="branch_delete"),

    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits/(?P<commit_id>[0-9]+)$',
        views.commit_details, name="commit_detail"),
    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits$', views.commit_create,
        name="commit_create"),
    # url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits/(?P<commit_id>[0-9]+)/update$',
    #     views.commit_update, name="commit_update"),
    url(r'^projects/(?P<project_id>[0-9]+)/branches/(?P<branch_id>[0-9]+)/commits/(?P<commit_id>[0-9]+)/delete$',
        views.commit_delete, name="commit_delete"),

    url(r'^projects/(?P<project_id>[0-9]+)/issues$', views.issue_create, name="issue_create"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)$', views.issue_details, name="issue_details"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/update$', views.issue_update, name="issue_update"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/delete$', views.issue_delete, name="issue_delete"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/add_label', views.issue_add_label,
        name="issue_add_label"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/add_assignee', views.issue_add_assignee,
        name="issue_add_assignee"),

    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/milestones$', views.milestone_create,
        name="milestone_create"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/milestones/(?P<milestone_id>[0-9]+)$',
        views.milestone_details, name="milestone_detail"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/milestones/(?P<milestone_id>[0-9]+)/update$',
        views.milestone_update, name="milestone_update"),
    url(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/milestones/(?P<milestone_id>[0-9]+)/delete$',
        views.milestone_delete, name="milestone_delete"),

    url(r'^labels/create$', views.label_create, name="label_create"),
    url(r'^labels$', views.label_list, name="label_list"),
    url(r'^labels/(?P<label_id>[0-9]+)$', views.label_details, name="label_detail"),
    url(r'^labels/(?P<label_id>[0-9]+)/update$', views.label_update, name="label_update"),
    url(r'^labels/(?P<label_id>[0-9]+)/delete$', views.label_delete, name="label_delete"),

]
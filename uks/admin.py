from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Project
from .models import User
from .models import UserProject
from .models import Branch
from .models import Commit
from .models import Milestone
from .models import Issue
from .models import IssueAssignment
from .models import Label
from .models import IssueLabel

# Register your models here.

admin.site.register(Project)
admin.site.register(User)
admin.site.register(UserProject)
admin.site.register(Branch)
admin.site.register(Commit)
admin.site.register(Milestone)
admin.site.register(Issue)
admin.site.register(IssueAssignment)
admin.site.register(Label)
admin.site.register(IssueLabel)

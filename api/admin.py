# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProfile, SkillSet, Project, Team

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SkillSet)
admin.site.register(Project)
admin.site.register(Team)

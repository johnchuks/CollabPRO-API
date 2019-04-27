# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class SkillSet(models.Model):
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    position = models.CharField(max_length=200, blank=True)
    skills = models.ManyToManyField(SkillSet)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=500, blank=False)
    skills = models.ManyToManyField(SkillSet)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=200, blank=False)
    members = models.ManyToManyField(User)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def get_user_from_object(pk):
    user = User.objects.get(pk=pk)
    if not user:
        return 'User not found'
    return user

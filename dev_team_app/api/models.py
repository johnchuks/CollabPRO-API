# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	position = models.CharField(max_length=200, blank=True)

	# @receiver(post_save, sender=User)
	# def create_user_profile(sender, instance, created, **kwargs):
    # 		if created:
    #     		UserProfile.objects.create(user=instance)

	# @receiver(post_save, sender=User)
	# def save_user_profile(sender, instance, **kwargs):
    # 		user = instance
	# 		if

class SkillSet(models.Model):
	title = models.CharField(max_length=200, blank=True)
	profile = models.ManyToManyField(UserProfile)

	def __str__(self):
		return self.title

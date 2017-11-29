# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .serializer import UserProfileSerializer, SkillSetSerializer, UserSerializer
from .models import UserProfile, SkillSet

# Create your views here.

class CreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserProfileView(generics.ListCreateAPIView):
    queryset =  UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  UserProfile.objects.all()
    serializer_class = UserProfileSerializer




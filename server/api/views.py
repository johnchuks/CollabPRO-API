# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework import exceptions
from rest_framework.response import Response
from .serializer import UserProfileSerializer, SkillSetSerializer
from .serializer import UserSerializer, ProjectSerializer, TeamSerializer, LoginSerializer
from .models import UserProfile, SkillSet, Project, Team
from api.utils.generate_jwt_token import generate_jwt_token

# Create your views here.


class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """ create a user """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token = generate_jwt_token(serializer.data)
            response = {
                'token': token,
                'id': serializer.data['id'],
                'username': serializer.data['username'],
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
                'email': serializer.data['email']
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ Persist a username and password during login for authentication """
    permission_classes = [permissions.AllowAny]

    def validate_username_password(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = 'Must include an email and password to login'
            raise exceptions.ValidationError(msg)
        return user

    def post(self, request):
        """ Login a registered user """
        authenticated_user = self.validate_username_password(request.data)
        if authenticated_user:
            serializer = LoginSerializer(authenticated_user)
            token = generate_jwt_token(serializer.data)
            response = {
                'token': token,
                'id': serializer.data['id'],
                'username': serializer.data['username'],
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
                'email': serializer.data['email']
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)


class DashboardView(TemplateView):
    template_name = 'base.html'
    def get(self, request):
        template = get_template('base.html')
        return HttpResponse(template.render())

class CreateUserProfileView(generics.ListCreateAPIView):
    """ creates a userprofile for an authenticated user """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CreateSkillSetView(generics.ListCreateAPIView):
    """ creates a skillset for application """
    queryset = SkillSet.objects.all()
    serializer_class = SkillSetSerializer


class CreateProjectView(APIView):
    """ create a new project and get projects"""

    def existing_project(self, title):
        """ Helper function for checking if project exist """
        try:
            Project.objects.get(title=title)
            return True
        except Project.DoesNotExist:
            return False

    def get(self, request):
        """ Gets all projects """
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Creates a new project"""
        if not request.data['title']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        existing_project = self.existing_project(request.data['title'])
        if not existing_project:
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_409_CONFLICT)


class CreateTeamView(APIView):
    """ creates a new team gets all teams """

    def existing_team(self, name):
        """ Helper function for checking if a team exist """
        try:
            Team.objects.get(name=name)
            return True
        except Team.DoesNotExist:
            return False

    def get(self, request):
        """ gets all teams """
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ creates a team """
        existing_team = self.existing_team(request.data['name'])

        if not existing_team:
            serializer = TeamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_409_CONFLICT)


class UserProfileDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ updates,deletes and get the profile of an existing user """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class SkillSetDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """ updates, deletes and get a particular skill with primary key """
    queryset = SkillSet.objects.all()
    serializer_class = SkillSetSerializer


class ProjectDetailsView(APIView):
    """ Retrieve, update and delete a project """

    def get_project_by_id(self, pk):
        """ Helper function to get project based on the primary key"""
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Gets a project """
        project = self.get_project_by_id(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """ Updates a project """
        project = self.get_project_by_id(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Deletes a project """
        project = self.get_project_by_id(pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamDetailsView(APIView):
    """ Retrieve, update, and delete a project """

    def get_team_by_id(self, pk):
        """ Helper function to get project based on the primary key"""
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ gets a team by id """
        team = self.get_team_by_id(pk=pk)
        team_serializer = TeamSerializer(team)
        return Response(team_serializer.data)

    def put(self, request, pk):
        """ updates a team by id """
        team = self.get_team_by_id(pk=pk)
        team_serializer = TeamSerializer(team, data=request.data)
        if team_serializer.is_valid():
            team_serializer.save()
            return Response(team_serializer.data)
        return Response(team_serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ delete a team by id """
        team = self.get_team_by_id(pk=pk)
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

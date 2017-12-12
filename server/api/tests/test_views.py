# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import SkillSet, UserProfile
from ..serializer import UserSerializer
import json

# Initialize the APIClient app
client = Client()


class CreateUserSignup(TestCase):
    """ Test module fot inserting a new user """

    def setUp(self):
        """ Test module fot inserting a new user """
        self.valid_payload = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.invalid_payload = dict(
            username='',
            first_name='ohia',
            last_name='mustard',
            email='email@test.com',
            password=''
        )
        self.existing_user_payload = dict(
            username='johnchuks21',
            first_name="john",
            last_name="johnwest",
            email="johnb@test.com",
            password="test"
        )

    def test_create_valid_user(self):
        """
        Ensure we can a new user object
        """
        url = reverse('create_user')
        response = client.post(url,
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'johnchuks21')

    def test_create_invalid_user(self):
        """
        Ensure we can check the user payload is correct
        """
        url = reverse('create_user')
        response = client.post(url,
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], [
                         'This field may not be blank.'])
        self.assertEqual(response.data['password'], [
                         'This field may not be blank.'])


class LoginInUser(TestCase):
    """ Test module for checking a user is authenticated upon login """

    def setUp(self):
        """ Setup for different test cases """
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.user = User.objects.create_user(**self.user_credentials)

        self.valid_login_credentials = {
            'username': 'johnchuks21',
            'password': 'kibana'
        }

        self.invalid_login_credentials = {
            'username': 'johnchuks34',
            'password': 'password'
        }

    def test_successful_login(self):
        """ Ensures a registered user is authenticated upon login """
        url = reverse('login_user')
        response = client.post(url,
                               data=json.dumps(self.valid_login_credentials),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, response.data['username'])
        self.assertEqual(self.user.first_name, response.data['first_name'])
        self.assertEqual(self.user.last_name, response.data['last_name'])
        self.assertEqual(self.user.email, response.data['email'])

    def test_unsuccessful_login(self):
        """ Ensure an error status is returned if user is not registered 
        upon logging in
        """
        url = reverse('login_user')
        response = client.post(url,
                               data=json.dumps(self.invalid_login_credentials),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Login failed')


class CreateUserProfile(APITestCase):
    """ Test module for creating userprofile for an existing user """

    def setUp(self):
        self.skill_payload = {
            "title": "AWS"
        }
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        url_user = reverse('create_user')
        self.create_user = self.client.post(url_user,
                                       data=json.dumps(self.user_credentials),
                                       content_type='application/json')
        self.skill = SkillSet.objects.create(**self.skill_payload)
        self.valid_user_profile = dict(
            user_id=self.create_user.data['id'],
            bio="I am a devops engineer with over seven years experience",
            position="senior devops engineer",
            skills=[self.skill.id]
        )
        self.invalid_user_profile_payload = dict(
            user_id=self.create_user.data['id'],
            bio="fjfofjfaoidfjvaoi",
            position='dsjldcnjsd',
            skills=''
        )
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.create_user.data['token']))

    def test_successful_create_userprofile(self):
        """ Ensure a userprofile is created for an existing user """
        url = reverse('create_userprofile')
        response = self.client.post(url,
                               data=json.dumps(self.valid_user_profile),
                               content_type="application/json"
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['position'], 'senior devops engineer')
        self.assertEqual(response.data['bio'], "I am a devops engineer with over seven years experience")

    def test_unsuccessful_create_userprofile(self):
        """ Ensure an error is thrown if all information is not provided """
        url = reverse('create_userprofile')
        response = self.client.post(url,
        data=json.dumps(self.invalid_user_profile_payload),
        content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserProfile(APITestCase):
    """ Test module for updating profile of registered user """
    def setUp(self):
        """ Setup parameters for test case """
        self.skill_payload = {
            "title": "AWS"
        }
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        url_user = reverse('create_user')
        self.create_user = self.client.post(url_user,
                                       data=json.dumps(self.user_credentials),
                                       content_type='application/json')
        self.skill = SkillSet.objects.create(**self.skill_payload)
        self.valid_user_profile = dict(
            user_id=self.create_user.data['id'],
            bio="I am a devops engineer with over seven years experience",
            position="senior devops engineer",
            skills=[self.skill.id]
        )

        self.update_profile = {
            "user_id": self.create_user.data['id'],
            "bio": "I am software engineer with 10 years experience",
            "skills": [self.skill.id]
        }
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.create_user.data['token']))
        url_profile = reverse('create_userprofile')
        self.create_userprofile = self.client.post(url_profile,
                               data=json.dumps(self.valid_user_profile),
                               content_type="application/json"
                               )

    def test_update_userprofile(self):
        """ Ensures userprofiles can be updated """
        url = reverse('update_get_delete_userprofile', kwargs={'pk': self.create_userprofile.data['id'] })
        response = self.client.put(url, 
        data=json.dumps(self.update_profile),
        content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], "I am software engineer with 10 years experience")

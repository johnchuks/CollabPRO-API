# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
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

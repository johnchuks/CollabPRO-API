# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import SkillSet, UserProfile, Project
from ..serializer import UserSerializer, UserProfileSerializer, ProjectSerializer
import json
from .test_utils import create_user, create_user_profile

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
                                            data=json.dumps(
                                                self.user_credentials),
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
        self.assertEqual(
            response.data['bio'], "I am a devops engineer with over seven years experience")

    def test_unsuccessful_create_userprofile(self):
        """ Ensure an error is thrown if all information is not provided """
        url = reverse('create_userprofile')
        response = self.client.post(url,
                                    data=json.dumps(
                                        self.invalid_user_profile_payload),
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
                                            data=json.dumps(
                                                self.user_credentials),
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
                                                   data=json.dumps(
                                                       self.valid_user_profile),
                                                   content_type="application/json"
                                                   )

    def test_update_userprofile(self):
        """ Ensures userprofiles can be updated """
        url = reverse('update_get_delete_userprofile', kwargs={
                      'pk': self.create_userprofile.data['id']})
        response = self.client.put(url,
                                   data=json.dumps(self.update_profile),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['bio'], "I am software engineer with 10 years experience")


class GetUserProfile(APITestCase):
    """ Test module for getting profile of a registered user """

    def setUp(self):
        self.user_payload = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.skills_payload = {
            "title": "Javascript"
        }
        self.profile_payload = dict(
            bio="I am a devops engineer with over seven years experience",
            position="senior devops engineer"
        )

        self.create_profile = create_user_profile(
            self.user_payload,
            self.skills_payload,
            self.profile_payload
        )
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.create_profile['token']))
        url_profile = reverse('create_userprofile')
        self.create_userprofile = self.client.post(url_profile,
                                                   data=json.dumps(
                                                       self.create_profile['profile']),
                                                   content_type="application/json"
                                                   )
        self.invalid_profile = {
            'id': 343
        }

    def test_get_userprofile(self):
        """ Ensures a user profile is got by its primary key """
        get_url = reverse('update_get_delete_userprofile', kwargs={
            'pk': self.create_userprofile.data['id']
        })
        response = self.client.get(get_url, kwargs={
            'pk': self.create_userprofile.data['id']
        })
        profile = UserProfile.objects.get(
            pk=self.create_userprofile.data['id'])
        serializer = UserProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_no_existing_userprofile(self):
        profile_url = reverse('update_get_delete_userprofile', kwargs={
            'pk': self.invalid_profile['id']
        })
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 404)


class DeleteUserProfile(APITestCase):

    def setUp(self):
        self.user_payload = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.skills_payload = {
            "title": "Javascript"
        }
        self.profile_payload = dict(
            bio="I am a devops engineer with over seven years experience",
            position="senior devops engineer"
        )

        self.create_profile = create_user_profile(
            self.user_payload,
            self.skills_payload,
            self.profile_payload
        )
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.create_profile['token']))
        url_profile = reverse('create_userprofile')
        self.create_userprofile = self.client.post(url_profile,
                                                   data=json.dumps(
                                                       self.create_profile['profile']),
                                                   content_type="application/json"
                                                   )

    def test_delete_userprofile(self):
        profile_url = reverse('update_get_delete_userprofile', kwargs={
            'pk': self.create_userprofile.data['id']
        })
        response = self.client.delete(profile_url)
        self.assertEqual(response.status_code, 204)


class CreateProjectView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )

        self.created_user = create_user(self.user_credentials)
        self.skills_payload = {
            "title": "javascript"
        }
        self.skills = SkillSet.objects.create(**self.skills_payload)
        self.project_payload = {
            "title": "NPM for blockchain",
            "description": "Create NPM module for blockchain",
            "skills": [self.skills.id],
            "author": self.created_user.data['id']
        }
        self.invalid_project_payload = {
            "title": "",
            "description": "",
            "skills": self.skills.id,
            "author": self.created_user.data['id']
        }

        self.auth = self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))

    def test_create_project(self):
        project_url = reverse('create_project')
        response = self.client.post(project_url,
                                    data=json.dumps(self.project_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['title'], "NPM for blockchain")
        self.assertEqual(response.data['description'],
                         "Create NPM module for blockchain")

    def test_invalid_create_project(self):
        project_url = reverse('create_project')
        response = self.client.post(project_url,
                                    data=json.dumps(
                                        self.invalid_project_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)


class GetProjectView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )

        self.created_user = create_user(self.user_credentials)
        self.skills_payload = {
            "title": "javascript"
        }
        self.skills = SkillSet.objects.create(**self.skills_payload)
        self.project_payload = {
            "title": "NPM for blockchain",
            "description": "Create NPM module for blockchain",
            "skills": [self.skills.id],
            "author": self.created_user.data['id']
        }
        self.auth = self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))
        url = reverse('create_project')
        self.new_project = self.client.post(url, data=json.dumps(
            self.project_payload), content_type="application/json")

        self.invalid_project_id = 2

    def test_get_project_by_id(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': self.new_project.data['id']})
        response = self.client.get(project_url)

        project = Project.objects.get(pk=self.new_project.data['id'])
        serializer = ProjectSerializer(project)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_no_existing_project(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': self.invalid_project_id
        })
        response = self.client.get(project_url)
        self.assertEqual(response.status_code, 404)


class UpdateProjectView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )

        self.created_user = create_user(self.user_credentials)
        self.skills_payload = {
            "title": "javascript"
        }
        self.skills = SkillSet.objects.create(**self.skills_payload)
        self.project_payload = {
            "title": "NPM for blockchain",
            "description": "Create NPM module for blockchain",
            "skills": [self.skills.id],
            "author": self.created_user.data['id']
        }
        self.auth = self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))
        url = reverse('create_project')
        self.new_project = self.client.post(url, data=json.dumps(
            self.project_payload), content_type="application/json")

        self.update_project_payload = {
            "title": "blockchain with javascript",
            "description": "Tutorial for implementing blockchain",
            "skills": [self.skills.id]
        }
        self.invalid_project_id = 2

    def test_update_project_by_id(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': self.new_project.data['id']
        })
        response = self.client.put(project_url, data=json.dumps(self.update_project_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "blockchain with javascript")

    def test_invalid_update_project_by_id(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': self.invalid_project_id
        })
        response = self.client.put(project_url, data=json.dumps(self.update_project_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)


class DeleteProjectView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )

        self.created_user = create_user(self.user_credentials)
        self.skills_payload = {
            "title": "javascript"
        }
        self.skills = SkillSet.objects.create(**self.skills_payload)
        self.project_payload = {
            "title": "NPM for blockchain",
            "description": "Create NPM module for blockchain",
            "skills": [self.skills.id],
            "author": self.created_user.data['id']
        }
        self.auth = self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))
        url = reverse('create_project')
        self.new_project = self.client.post(url, data=json.dumps(
            self.project_payload), content_type="application/json")

    def test_successsful_delete_project(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': self.new_project.data['id']
        })
        response = self.client.delete(project_url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_delete_project(self):
        project_url = reverse('update_get_delete_project', kwargs={
            'pk': 2345
        })
        response = self.client.delete(project_url)
        self.assertEqual(response.status_code, 404)


class CreateSkillSetView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.created_user = create_user(self.user_credentials)
        self.skill_payload = dict(title="AWS EC2")

        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))

    def test_successful_create_skillset(self):
        skill_url = reverse('create_skill')
        response = self.client.post(skill_url, data=json.dumps(self.skill_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'AWS EC2')

    def test_invalid_create_skillset(self):
        skill_url = reverse('create_skill')
        response = self.client.post(skill_url, data=json.dumps(
            dict(title="")), content_type="application/json")
        self.assertEqual(response.status_code, 400)


class UpdateSkillSetView(APITestCase):

    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.created_user = create_user(self.user_credentials)
        self.skill_payload = dict(title="AWS EC2")

        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))

        create_skill_url = reverse('create_skill')
        self.new_skill = self.client.post(create_skill_url, data=json.dumps(
            self.skill_payload), content_type='application/json')
        self.update_skill_payload = dict(title="python django")

    def test_update_skill(self):
        skill_url = reverse('update_get_delete_skill', kwargs={
            'pk': self.new_skill.data['id']
        })

        response = self.client.put(skill_url, data=json.dumps(
            self.update_skill_payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "python django")


class GetSkillSetView(APITestCase):
    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.created_user = create_user(self.user_credentials)
        self.skill_payload = dict(title="AWS EC2")

        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))

        create_skill_url = reverse('create_skill')
        self.new_skill = self.client.post(create_skill_url, data=json.dumps(
            self.skill_payload), content_type='application/json')

    def test_get_skill_by_id(self):
        skill_url = reverse('update_get_delete_skill', kwargs={
            'pk': self.new_skill.data['id']
        })
        response = self.client.get(skill_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'AWS EC2')


class DeleteSkillSetView(APITestCase):
    def setUp(self):
        self.user_credentials = dict(
            username="johnchuks21",
            first_name="john",
            last_name="ohia",
            email="johnc@gmail.com",
            password="kibana"
        )
        self.created_user = create_user(self.user_credentials)
        self.skill_payload = dict(title="AWS EC2")

        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(
            self.created_user.data['token']))

        create_skill_url = reverse('create_skill')
        self.new_skill = self.client.post(create_skill_url, data=json.dumps(
            self.skill_payload), content_type='application/json')

    def test_delete_skill_by_id(self):
        skill_url = reverse('update_get_delete_skill', kwargs={
            'pk': self.new_skill.data['id']
        })
        response = self.client.delete(skill_url)
        self.assertEqual(response.status_code, 204)



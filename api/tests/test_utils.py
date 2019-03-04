from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..models import SkillSet, UserProfile
import json

client = Client()

def create_user(user_credentials):
    """ utility test function for creating a user in testing environment """
    url = reverse('create_user')
    user = client.post(url,
                       data=json.dumps(user_credentials),
                       content_type='application/json')
    return user


def create_user_profile(user_credentials, skills_payload, profile_payload):
    """ utility function for creating user profile in testing environment """

    skill = SkillSet.objects.create(**skills_payload)
    user = create_user(user_credentials)
    user_profile = dict(
        user_id=user.data['id'],
        bio=profile_payload['bio'],
        position=profile_payload['position'],
        skills=[skill.id]
    )
    obj = {
        "profile": user_profile,
        "token": user.data['token']
    }
    return obj

from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from .models import UserProfile, SkillSet, Project, Team


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to map user model to json format """
    # projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    def create(self, validated_data):
        """ Create user upon signup """
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'password')


class LoginSerializer(serializers.ModelSerializer):
    """ serializer for handling login authentication """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'password')


class SkillSetSerializer(serializers.ModelSerializer):
    """ Serializer maps the skillset model into a json format """
    id = serializers.IntegerField(source='pk', read_only=True)

    def perform_create(self, validated_data):
        skill_set = SkillSet.objects.create(**validated_data)
        return skill_set

    class Meta:
        db_table = 'skill_set'
        model = SkillSet
        fields = ('id', 'title')


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer maps the user profile model into a json format """
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(
        source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    skills = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=SkillSet.objects.all())

    def create(self, validated_data):
        """ serializer method for creating user profile """
        user = User.objects.get(pk=validated_data['user']['id'])
        skills = validated_data.pop('skills')
        profile = UserProfile.objects.create(user=user, **validated_data)
        profile.skills.add(*skills)
        return profile

    def update(self, instance, validated_data):
        """ serializer method for updating user profile"""
        user = instance.user
        user.email = validated_data.get('user.email', user.email)
        user.first_name = validated_data.get(
            'user.first_name', user.first_name)
        user.last_name = validated_data.get('user.last_name', user.last_name)
        user.save()
        instance.bio = validated_data.get('bio', instance.bio)
        instance.position = validated_data.get('position', instance.position)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.save()
        return instance

    class Meta:
        db_table = 'user_profile'
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'bio', 'position', 'user_id', 'skills')


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer maps the project model into a json format """

    def create(self, validated_data):
        """ serializer method for creating a project """
        author_details = validated_data.pop('author')
        user = User.objects.get(pk=author_details.id)
        return Project.objects.create(author=user, **validated_data)

    def update(self, instance, validated_data):
        """ serializer method for updating a project """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.save()
        return instance

    class Meta:
        """ Maps the project model to json """
        model = Project
        fields = ('id', 'title', 'description', 'skills', 'author')


class TeamSerializer(serializers.ModelSerializer):
    """ Serializer maps the team model into a json format """

    def create(self, validated_data):
        """ serializer method for creating a team """
        members = validated_data.pop("members")
        team = Team.objects.create(**validated_data)
        team.members.add(*members)
        return team

    def update(self, instance, validated_data):
        """ serializer method for updating a team """
        instance.name = validated_data.get('name', instance.name)
        instance.members = validated_data.get('members', instance.members)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance

    class Meta:
        """ Maps the team model to json """
        model = Team
        fields = ('id', 'name', 'members', 'project')

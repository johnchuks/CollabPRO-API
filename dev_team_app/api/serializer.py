from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from  .models import UserProfile, SkillSet


class UserSerializer(serializers.ModelSerializer):
    """ Serializer to map user model to json format """

    class Meta:
        model=User
        fields=('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')



class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer maps the model into a json format """
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    def create(self, validated_data):
        user = User.objects.get(pk=validated_data['user']['id'])
        user_data = validated_data.pop('user')
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        #user = User.objects.get(pk = instance.user.pk);
        user = instance.user
        user.email = validated_data.get('user.email', user.email)
        user.first_name = validated_data.get('user.first_name', user.first_name)
        user.last_name = validated_data.get('user.last_name', user.last_name)
        user.save()
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


    class Meta:
        db_table='user_profile'
        model=UserProfile
        fields=('id', 'username', 'first_name','last_name','email', 'bio', 'position', 'user_id')




class SkillSetSerializer(serializers.ModelSerializer):
    class Meta:
        db_table='skill_set'
        model=SkillSet
        fields=('id', 'title')




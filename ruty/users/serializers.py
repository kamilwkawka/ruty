from rest_framework import serializers
from .models import User, surveyResponse, Group, GroupMembership, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "age", "bio"]

class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = surveyResponse
        fields = ['user', 'question_1', 'question_2', 'question_3']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'created_at']

class GroupMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'group', 'joined_at']

class GroupDetailSerializer(serializers.ModelSerializer):
    members = GroupMembershipSerializer(source='group_membership', many=True)
    
    class Meta:
        model=Group
        fields = ['id', 'name', 'created_at', 'members']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Skill, UserSkill, Match, Message

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar']

# --- Register Serializer ---
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# --- Skill Serializer ---
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

# --- UserSkill Serializer ---
class UserSkillSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = UserSkill
        fields = ['id', 'user', 'skill', 'skill_name', 'role']

# --- Match Serializer ---
class MatchSerializer(serializers.ModelSerializer):
    teacher_username = serializers.ReadOnlyField(source='teacher.username')
    learner_username = serializers.ReadOnlyField(source='learner.username')
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = Match
        fields = ['id', 'teacher', 'teacher_username', 'learner', 'learner_username', 'skill', 'skill_name', 'created_at']

# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'match', 'sender', 'sender_username', 'content', 'timestamp']

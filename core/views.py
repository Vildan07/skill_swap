# core/views.py

from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Skill, UserSkill, Match, Message
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    SkillSerializer,
    UserSkillSerializer,
    MatchSerializer,
    MessageSerializer
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

# --- Регистрация ---
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# --- Получить текущего пользователя ---
class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# --- Skill List ---
class SkillListAPIView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- UserSkill: список и добавление ---
class UserSkillListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_skill = serializer.save(user=request.user)

        matches_created = self._try_create_matches(user_skill)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                'message': 'UserSkill created successfully.',
                'user_skill': serializer.data,
                'matches_created': matches_created,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def _try_create_matches(self, user_skill):
        from .models import Match, UserSkill

        matches = []

        if user_skill.role == 'learn':
            opposite_role = 'teach'
            field_as_learner = True
        else:
            opposite_role = 'learn'
            field_as_learner = False

        potential_matches = UserSkill.objects.filter(
            skill=user_skill.skill,
            role=opposite_role
        ).exclude(user=user_skill.user)

        for other in potential_matches:
            teacher = other.user if field_as_learner else user_skill.user
            learner = user_skill.user if field_as_learner else other.user

            if not Match.objects.filter(teacher=teacher, learner=learner, skill=user_skill.skill).exists():
                Match.objects.create(teacher=teacher, learner=learner, skill=user_skill.skill)
                matches.append(f"@{other.user.username}")

        return matches

# --- Match List (все совпадения текущего пользователя) ---
class MatchListAPIView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(teacher=user) | Match.objects.filter(learner=user)


# --- Message ListCreate (чат внутри матча) ---
class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        return Message.objects.filter(match_id=match_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


# --- 👤 User: Получить и обновить свои данные ---
class UserDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# --- 🧠 UserSkill: CRUD ---
class UserSkillListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)


# --- 🧩 Skill: Только List/Create (CRUD не нужен обычному пользователю) ---
class SkillListCreateAPIView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- 🔁 Match: List, Delete ---
class MatchListAPIView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(teacher=user) | Match.objects.filter(learner=user)


class MatchDeleteAPIView(generics.DestroyAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(teacher=user) | Match.objects.filter(learner=user)


# --- 💬 Message: List/Create (CRUD не нужен) ---
class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        return Message.objects.filter(match_id=match_id)

    def perform_create(self, serializer):
        match_id = self.kwargs['match_id']
        serializer.save(sender=self.request.user, match_id=match_id)

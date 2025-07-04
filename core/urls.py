from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
 # Авторизация
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User
    path('user/', UserDetailUpdateAPIView.as_view(), name='me'),

    # Skills
    path('skills/', SkillListCreateAPIView.as_view(), name='skills'),

    # UserSkill
    path('my-skills/', UserSkillListCreateAPIView.as_view(), name='user_skill_list_create'),
    path('my-skills/<int:pk>/', UserSkillDetailAPIView.as_view(), name='user_skill_detail'),

    # Match
    path('matches/', MatchListAPIView.as_view(), name='matches'),
    path('matches/<int:pk>/delete/', MatchDeleteAPIView.as_view(), name='match_delete'),

    # Messages
    path('matches/<int:match_id>/messages/', MessageListCreateAPIView.as_view(), name='messages'),
]
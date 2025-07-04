from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Skill, UserSkill, Match, Message

User = get_user_model()


# --- Пользователь ---
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('bio', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )


# --- Навыки ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


# --- Навыки пользователя ---
@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'skill', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'skill__name')
    autocomplete_fields = ('user', 'skill')


# --- Матчи ---
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'learner', 'skill', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('teacher__username', 'learner__username', 'skill__name')
    autocomplete_fields = ('teacher', 'learner', 'skill')


# --- Сообщения ---
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'sender', 'timestamp')
    search_fields = ('sender__username', 'content')
    list_filter = ('timestamp',)
    autocomplete_fields = ('match', 'sender')

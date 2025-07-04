from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    ROLE_CHOICES = [
        ('teach', 'Can Teach'),
        ('learn', 'Wants to Learn'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'skill', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.skill.name}"

class Match(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_teacher')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_learner')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'learner', 'skill')

    def __str__(self):
        return f"{self.learner.username} ↔ {self.teacher.username} ({self.skill.name})"

class Message(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

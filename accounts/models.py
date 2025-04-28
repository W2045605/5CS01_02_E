from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User

class Session(models.Model):
    title = models.CharField(max_length=100)

class Card(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

class UserCardProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    vote = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'session', 'card')

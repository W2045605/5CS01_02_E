from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class HealthCard(models.Model):
    card_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.card_name

VOTE_CHOICES = [
    ('green', 'Green'),
    ('amber', 'Amber'),
    ('red', 'Red'),
]

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    vote_status = models.CharField(max_length=6, choices=VOTE_CHOICES)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.card.card_name} - {self.vote_status}"

ROLE_CHOICES = [
    ('engineer', 'Engineer'),
    ('team_leader', 'Team Leader'),
    ('dep_leader', 'Department Leader'),
    ('manager', 'Senior Manager'),
    ('admin', 'Administrator'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=100)
    team_id = models.IntegerField(null=True, blank=True)
    dept_id = models.IntegerField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name

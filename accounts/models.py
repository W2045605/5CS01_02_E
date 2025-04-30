from django.db import models
from django.contrib.auth.models import User

# ----------------------------
# Session Model
# ----------------------------
class Session(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

# ----------------------------
# HealthCard Model (formerly just Card)
# ----------------------------
class HealthCard(models.Model):
    card_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.card_name

# ----------------------------
# Vote Model (User progress and voting)
# ----------------------------
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
        return f"{self.user.username} voted {self.vote_status} on {self.card.card_name}"

# ----------------------------
# UserCardProgress (Separate from Vote for tracking progress)
# ----------------------------
STATUS_CHOICES = [
    ('not_started', 'Not Started'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

class UserCardProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCard, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'session', 'card')

    def __str__(self):
        return f"{self.user.username} - {self.card.card_name} ({self.status})"

# ----------------------------
# UserProfile Model
# ----------------------------
ROLE_CHOICES = [
    ('engineer', 'Engineer'),
    ('team_leader', 'Team Leader'),
    ('dep_leader', 'Department Leader'),
    ('manager', 'Senior Manager'),
    ('admin', 'Administrator'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    team_id = models.IntegerField(null=True, blank=True)
    dept_id = models.IntegerField(null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name

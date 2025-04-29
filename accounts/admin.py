from django.contrib import admin
from .models import Session, HealthCard, Vote, UserProfile

admin.site.register(Session)
admin.site.register(HealthCard)
admin.site.register(Vote)
admin.site.register(UserProfile)


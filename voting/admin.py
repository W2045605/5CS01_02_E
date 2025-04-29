
from django.contrib import admin


from django.contrib import admin
from .models import Session, HealthCard, Vote

admin.site.register(Session)
admin.site.register(HealthCard)
admin.site.register(Vote)


from django.urls import path
from . import views

urlpatterns = [
    path('submit-vote/', views.submit_vote, name='submit_vote'),
]

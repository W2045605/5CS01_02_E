
from django.urls import path
from . import views

urlpatterns = [
    path('submit-vote/', views.submit_vote, name='submit_vote'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('my-sessions/', views.session_list, name='session_list'),
    path('my-sessions/<int:session_id>/chart/', views.user_vote_chart, name='user_vote_chart'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_role, name='edit_role'),
]

urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
]

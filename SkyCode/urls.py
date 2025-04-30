"""SkyCode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('',views.userlogin),
    path('logout/',views.userlogout , name='logout'),
    path('login/', views.userlogin, name="login"),
    path('signup/', views.usersignup, name = "signup"),
    path('profile/',views.profile, name = 'profile')
    
=======
    path('', include('accounts.urls')),
>>>>>>> 1557ccb5bd7588f8001811d0b15a85c5d3b6a1bb
]


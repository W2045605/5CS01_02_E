from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sessions/', include('sessions.urls')),   # Session/voting/progress app
    path('accounts/', include('accounts.urls')),   # Login/signup app (if you have one)
    # You can add more app includes here as needed
]

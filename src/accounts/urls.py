# accounts/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('registrarse/', views.SignUp.as_view(), name='signup'),
]

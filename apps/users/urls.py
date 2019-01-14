from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

app_name = 'users'
# <a href="{% url 'users:index' %}" > </a>

urlpatterns = [
    # path('register/', views.register, name="register"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

]
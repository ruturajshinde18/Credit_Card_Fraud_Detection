from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name = 'account-login'),
    path('register/', views.register, name = 'account-register'),
    path('logout/', views.logout, name='account-logout'),
]
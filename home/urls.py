from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('prediction', views.prediction, name='predict'),
    path('about', views.about, name='about'),
]
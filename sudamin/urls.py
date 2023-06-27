from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name = 'su-index'),
    path('dataset', views.dataset, name = 'su-dataset'),
    path('prediction', views.prediction, name = 'su-predict'),
]
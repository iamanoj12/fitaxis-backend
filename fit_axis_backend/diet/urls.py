from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_diet, name='generate_diet'),
]
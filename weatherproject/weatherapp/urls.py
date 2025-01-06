from django.urls import path
from . import views  # Importing the views module

urlpatterns = [
    path('', views.home),  # Referencing the home view function
]

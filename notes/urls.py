from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/register/', RegisterUser.as_view() ),
    path('notes/', NotesAPI.as_view()),
    path('notes/<id>', NotesAPIByID.as_view()),
]
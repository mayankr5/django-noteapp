from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/signup/', RegisterUser.as_view() ),
    # path('auth/login/', LoginUser.as_view()),
    # path('auth/logout/', LogoutUser.as_view()),
    path('notes/', NotesAPI.as_view()),
    path('notes/<id>', NotesAPIByID.as_view()),
]
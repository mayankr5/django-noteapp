from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner']
        read_only_fields = ['user']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password']
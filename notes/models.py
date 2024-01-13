import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)


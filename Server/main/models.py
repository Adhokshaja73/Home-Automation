
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HomeBoardTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    topic = models.CharField(max_length=100)


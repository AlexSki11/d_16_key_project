from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_board(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
class message_board(models.Model):
    author = models.ForeignKey(User_board,models.CASCADE)

    header = models.CharField(max_length=64)
    text = models.TextField(max_length=1000)

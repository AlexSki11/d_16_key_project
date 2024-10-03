from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

class UserBoard(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class MessageBoard(models.Model):
    author = models.ForeignKey(UserBoard,models.CASCADE)
    data_create = models.DateTimeField(auto_now_add=True)
    message_category = models.ManyToManyField(Category, through='MessageCategory')
    
    content = RichTextField()

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})
    

class MessageCategory(models.Model):
    message = models.ForeignKey(MessageBoard, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name}'
    

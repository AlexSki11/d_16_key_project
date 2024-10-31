from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.shortcuts import render
#from django.contrib

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
    
    header = models.CharField(max_length=64)
    content = RichTextUploadingField(config_name='awesome_ckeditor')

   
    def get_response(self):
        return Response.objects.filter()

    def __str__(self) -> str:
        return f'{self.header}'

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})
    

class MessageCategory(models.Model):
    message = models.ForeignKey(MessageBoard, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='MessageCategory')

    

    def __str__(self):
        return f'{self.category.name}'
    
class Response(models.Model):
    text = models.TextField(max_length=1000)
    data_create = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(UserBoard, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, related_name='MessageResponse')
    
    def get_absolute_url(self):
        print(self.message.id)
        return reverse("message_detail", kwargs={'pk':self.message.id})

    def __str__(self):
        return f'{self.text}'
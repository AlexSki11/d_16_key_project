from typing import Any
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MessageBoard
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from allauth.account.forms import SignupForm
from .models import UserBoard
from django.contrib.auth.models import Group

class MessageBoardForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='awesome_ckeditor'))
    class Meta:
        model = MessageBoard
        fields = ['header','content','message_category']


class MessageBoardAdmin(admin.ModelAdmin):
    form = MessageBoardForm

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user_board = UserBoard.objects.create(user=user)
        group = Group.objects.get(name='users_board')
        user.groups.add(group)
        return user
    
    class Meta:
        fields = '__all__'
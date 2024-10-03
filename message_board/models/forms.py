from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MessageBoard
from ckeditor.widgets import CKEditorWidget
from allauth.account.forms import SignupForm
from .models import UserBoard

class MessageBoardForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget)
    class Meta:
        model = MessageBoard
        fields = '__all__'

class MessageBoardAdmin(admin.ModelAdmin):
    form = MessageBoardForm

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user_board = UserBoard.objects.create(user=user)
        
        return user
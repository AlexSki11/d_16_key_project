from django.contrib import admin
from .models import MessageBoard, Category, MessageCategory, UserBoard
from .forms import MessageBoardAdmin
# Register your models here.

admin.site.register(MessageBoard, MessageBoardAdmin)
admin.site.register(Category)
admin.site.register(MessageCategory)
admin.site.register(UserBoard)
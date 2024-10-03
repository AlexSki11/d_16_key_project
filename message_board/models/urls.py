
from django.urls import path
from .views import (MessageCreate, MessageEdit, MessageDelete, MessageList, MessageDetail)

urlpatterns = [
    
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('edit/', MessageEdit.as_view(), name='message_edit'),
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>', MessageDetail.as_view(), name='message_detail'),
    path('delete/<int:pk>',MessageDelete.as_view(), name='message_delete'),


]
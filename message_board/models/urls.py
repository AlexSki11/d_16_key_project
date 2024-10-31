
from django.urls import path
from .views import (MessageCreate, MessageEdit, MessageDelete, MessageList, MessageDetail,
                    ResponseCreate, ResponseEdit, ResponseDelete)


urlpatterns = [
    
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('edit/<int:pk>/', MessageEdit.as_view(), name='message_edit'),
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetail.as_view(), name='message_detail'),
    path('delete/<int:pk>/',MessageDelete.as_view(), name='message_delete'),

    path('create_response/', ResponseCreate.as_view(), name='response_create'),
    path('edit_response/<int:pk>/', ResponseEdit.as_view(), name='response_edit'),
    path('delete_response/<int:pk>/', ResponseDelete.as_view(), name='response_delete'),

]
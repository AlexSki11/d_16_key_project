from django.shortcuts import render
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic import (ListView, DetailView)
from django.contrib.auth.models import User
from .forms import MessageBoardForm
from .models import MessageBoard
from django.urls import reverse_lazy

# Create your views here.

class MessageList(ListView):
    model = MessageBoard
    
    template_name = 'message_list.html'
    ordering = '-data_create'
    paginate_by = 10
    context_object_name = 'messages'

class MessageDetail(DetailView):
    model = MessageBoard
    template_name = 'message_detail.html'
    context_object_name = 'message'

class MessageCreate(CreateView):
    form_class = MessageBoardForm
    model = MessageBoard
    template_name = 'message_create.html'

class MessageEdit(UpdateView):
    form = MessageBoardForm
    model = MessageBoard
    template_name = 'message_create.html'

class MessageDelete(DeleteView):
    model = MessageBoard
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')
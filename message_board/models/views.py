from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic import (ListView, DetailView)
from django.contrib.auth.models import User, Permission
from .forms import MessageBoardForm
from .models import MessageBoard, UserBoard
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


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

class MessageCreate(LoginRequiredMixin, CreateView):
    form_class = MessageBoardForm
    model = MessageBoard
    template_name = 'message_create.html'
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.author = UserBoard.objects.get(user=self.request.user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    
    

class MessageEdit(LoginRequiredMixin, UpdateView):
    form_class = MessageBoardForm
    model = MessageBoard
    template_name = 'message_create.html'

    def get_queryset(self):
        queryset = MessageBoard.objects
        message = self.get_object(queryset)
        
        if (message.author != UserBoard.objects.get(user=self.request.user) and not
            self.request.user.has_perm('models.change_messageboard')) :
            raise PermissionDenied

        return super().get_queryset()
    
        

class MessageDelete(LoginRequiredMixin, DeleteView):
    model = MessageBoard
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')

    def get_queryset(self):
        queryset = MessageBoard.objects
        message = self.get_object(queryset)
        
        if (message.author != UserBoard.objects.get(user=self.request.user) and not
            self.request.user.has_perm('models.change_messageboard')) :
            raise PermissionDenied

        return super().get_queryset()
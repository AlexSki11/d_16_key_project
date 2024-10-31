from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic import (ListView, DetailView)
from django.contrib.auth.models import User, Permission
from .forms import MessageBoardForm, ResponseForm
from .models import MessageBoard, UserBoard, Response
from django.urls import reverse_lazy, reverse
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

    def render_to_response(self, context, **response_kwargs):

        render = super().render_to_response(context, **response_kwargs)
        
        return render

    

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

class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print('begin')
        print(self.request)
        message_id=self.request.GET.copy()
        print(message_id.__getitem__('id'))
        self.object = form.save(commit=False)
        self.object.user = UserBoard.objects.get(user=self.request.user)
        self.object.message = MessageBoard.objects.get(id=message_id.__getitem__('id'))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
class ResponseEdit(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

class ResponseList(ListView):
    model = Response
    template_name = 'none'
    context_object_name = 'response'

class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = '/'

    def get_success_url(self):

        pk = self.request.GET.get('id')
        return reverse('message_detail', kwargs={'pk':pk})
    

    def get_queryset(self):
        queryset = Response.objects
        response = self.get_object(queryset)
        
        if ( response.user != UserBoard.objects.get(user=self.request.user) and not
            self.request.user.has_perm('models.change_response')) :
            raise PermissionDenied

        return super().get_queryset()
    

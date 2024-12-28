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
from django.core.mail import send_mail
from .filters import ResponseFilter, MessageFilter
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .templatetags.custom_filters import in_groups

# Create your views here.

class MessageList(ListView):
    model = MessageBoard
    
    template_name = 'message_list.html'
    ordering = '-data_create'
    paginate_by = 10
    context_object_name = 'messages'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = MessageFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context
    


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
        form.save_m2m()
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
        message_id=self.request.GET.get('id')
        self.object = form.save(commit=False)
        self.object.user = UserBoard.objects.get(user=self.request.user)
        self.object.message = MessageBoard.objects.get(id=message_id)
        if Response.objects.filter(user = self.object.user, message=self.object.message):
            raise PermissionDenied
        self.object.save()
        send_mail(f'Отлклик на ваше объявление от {self.request.user.username}',
                  from_email=None,
                  message=f'{self.object.text}',
                  recipient_list=[self.object.message.author.user.email])
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = MessageBoard.objects.get(id=self.request.GET.get('id'))
        if message.author.user == self.request.user:
            raise PermissionDenied
        return context
    

class ResponseEdit(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'

class ResponseList(LoginRequiredMixin,ListView):
    model = Response
    template_name = 'response_list.html'
    context_object_name = 'responses'
    ordering = ['data_create']
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        
        
        print(request.POST)
        print(request.POST.get('response_id'))
        return HttpResponseRedirect('/board/response/')
    

    def get_queryset(self):
        user = UserBoard.objects.get(user=self.request.user)
        queryset = Response.objects.filter(message__author = user)
        queryset = queryset.order_by('data_create')
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

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
    
@login_required
@csrf_protect
def accept_response(request):
    text = request.POST.get('text')
    response_id = request.GET.get('id')
    if not response_id:
        raise PermissionDenied
    try:
        response = Response.objects.get(id=response_id)
    except ObjectDoesNotExist:
        raise PermissionDenied
    if response.message.author.user != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        result = request.GET.get('result')
        email = response.user.user.email
        if result=='accept':
            response.status = True
            response.save()
            
            send_mail(f'Ответ на ваш отклик', f'{response.message} {text}', from_email=None,
                      recipient_list=[email])
        else:
            response.status = False
            response.save()
            send_mail(f'Ответ на ваш отклик', f'{response.message} {text}', from_email=None,
                      recipient_list=[email])
            
        return HttpResponseRedirect('/board/response/')

    return render(request,'response.html',{})

@login_required
@permission_required(['perms.admin', 'perms.managers'])
@csrf_protect
def send_news(request):
    if not in_groups(request.user, 'managers'):
        raise PermissionDenied
    
    if request.method == 'POST' and request.POST.get('action') == 'accept':
        subject = request.POST.get('subject')
        text = request.POST.get('text')
        emails = User.objects.filter(groups__name='users_board').values_list('email', flat=True)
        send_mail(subject,text,from_email=None,recipient_list=emails)
        return HttpResponseRedirect('/board')
    
    return render(request, 'send_news.html')
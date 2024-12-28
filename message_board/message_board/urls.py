"""
URL configuration for message_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from models.views import StartView

def is_in_groupe(user):
    return user.groups.filter(name='users_board').exists()

@login_required
@user_passes_test(is_in_groupe)
@csrf_exempt
def my_upload(request):
    return views.upload(request)


@login_required
@user_passes_test(is_in_groupe)
@csrf_exempt
def my_browse(request):
    return views.browse(request)

urlpatterns = [
    path('', StartView.as_view(), name='start'),

    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls'), name='account'),
    path('board/', include('models.urls')),
    path('ckeditor/upload/', my_upload, name='ckeditor_upload'),
    path('ckeditor/browse/', my_browse, name='ckeditor_browse')
   #path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




'''
ckeditor_url = [
    path("ckeditor/upload/", views.upload, name="ckeditor_upload"),
    path(
        "ckeditor/browse/",
        views.browse,
        name="ckeditor_browse",
    ),
]

'''
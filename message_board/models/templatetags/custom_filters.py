from django import template
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

register = template.Library()

@register.filter()
def get_response(objects, user=None):

    if isinstance(user, AnonymousUser):
        return None
    
    obj = objects.filter(user__user=user)

    if obj:
        return obj
    else:
        return None

@register.filter()
def in_groups(user, group:str):
    return user.groups.filter(name=group).exists()


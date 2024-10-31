from django import template

register = template.Library()

"""
@register.simple_tag(takes_context=True)
def edit_context(context, **kwargs):
   d = context['request'].GET.copy()
   print(context['object'].id)
   kwargs['id']=1
   print(kwargs)
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

   """
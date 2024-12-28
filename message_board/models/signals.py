from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from .models import Category

@receiver(post_migrate)
def create_start_category(sender, **kwargs):
    if sender.name == 'models':
        start_category = [ "Танки", "Хилы", "ДД", "Торговцы", "Гилдмастеры", 
                         "Квестгиверы", "Кузнецы", "Кожевники", "Зельевары", "Мастера заклинаний" ]
        if not Category.objects.filter(name__in=start_category).exists():
            for category in start_category:
                Category.objects.create(name=category)
        if not Group.objects.filter(name='users_board').exists():
            Group.objects.create(name='users_board')
           

import django_filters
from .models import MessageBoard, Response, Category


def messages(request):
    if request is None:
        return MessageBoard.objects.none()

    queryset = MessageBoard.objects.filter(author__user = request.user)
    return queryset

class ResponseFilter(django_filters.FilterSet):

    message = django_filters.ModelChoiceFilter(field_name='message', queryset = messages, label = 'Ваши объявления', empty_label='Все',)

    class Meta:
        model = Response
        fields = {}

    
        



class MessageFilter(django_filters.FilterSet):

    message_category = django_filters.ModelMultipleChoiceFilter(field_name='message_category', queryset=Category.objects.all(), label='Категории', )

    class Meta:
        model = MessageBoard
        fields = {
            'header':['icontains'],
            'author__user__username':['icontains'],
        }
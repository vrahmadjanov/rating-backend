from django.db.models import OuterRef, Subquery, Prefetch
from rest_framework import viewsets
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        # Оптимизация запроса: добавляем последнее сообщение
        last_message_subquery = Message.objects.filter(
            chat=OuterRef('pk')
        ).order_by('-timestamp').values('content', 'timestamp', 'sender__first_name', 'sender__last_name')[:1]

        return Chat.objects.annotate(
            last_message_content=Subquery(last_message_subquery.values('content')),
            last_message_timestamp=Subquery(last_message_subquery.values('timestamp')),
            last_message_sender=Subquery(last_message_subquery.values('sender__first_name')),
        ).select_related('participant1', 'participant2')

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

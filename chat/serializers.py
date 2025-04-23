from rest_framework import serializers
from .models import Chat, Message
from core.models import CustomUser

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'middle_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = ChatUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['sender', 'content', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    participant1 = ChatUserSerializer(read_only=True)
    participant2 = ChatUserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()  # Добавляем последнее сообщение

    class Meta:
        model = Chat
        fields = ['id', 'participant1', 'participant2', 'created_at', 'last_message']

    def get_last_message(self, obj):
        # Получаем последнее сообщение из чата
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None
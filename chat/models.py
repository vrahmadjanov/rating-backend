from django.db import models
from django.db.models import Q, UniqueConstraint
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    """
    Модель для хранения чата между двумя пользователями.
    """
    participant1 = models.ForeignKey(User, related_name='chats_as_participant1', on_delete=models.CASCADE, db_index=True)
    participant2 = models.ForeignKey(User, related_name='chats_as_participant2', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['participant1', 'participant2'],
                name='unique_chat_participants'
            ),
            UniqueConstraint(
                fields=['participant2', 'participant1'],
                name='unique_chat_participants_reverse'
            ),
        ]

    def __str__(self):
        return f"Chat between {self.participant1} and {self.participant2}"

    @classmethod
    def get_chat_between_users(cls, user1, user2):
        """
        Возвращает чат между двумя пользователями, если он существует.
        """
        return cls.objects.filter(
            (Q(participant1=user1) & Q(participant2=user2)) |
            (Q(participant1=user2) & Q(participant2=user1))
        ).first()


class Message(models.Model):
    """
    Модель для хранения сообщений в чате.
    """
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, db_index=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, db_index=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Message from {self.sender} in chat {self.chat.id}"
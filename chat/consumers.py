import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from channels.exceptions import DenyConnection
from .models import Chat, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Обрабатывает подключение пользователя к WebSocket.
        """
        # Получаем токен из query string
        token = self.scope.get('query_string', b'').decode('utf-8').split('token=')[-1]
        if not token:
            # Если токен не передан, закрываем соединение
            await self.close(code=4000)  # Пользовательский код закрытия
            return

        try:
            # Проверяем токен
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Получаем user_id из токена
            self.user = await self.get_user(user_id)  # Получаем пользователя
            if not self.user:
                raise DenyConnection("User not found")

        except (TokenError, InvalidToken) as e:
            # Если токен недействителен, закрываем соединение
            await self.close(code=4001)  # Пользовательский код закрытия
            return

        # Получаем ID чата из URL
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'  # Название группы для чата

        # Проверяем, существует ли чат
        self.chat = await self.get_chat(self.chat_id)
        if not self.chat:
            await self.close()  # Закрываем соединение, если чат не существует
            return

        # Проверяем, что пользователь является участником чата
        participant1 = await sync_to_async(lambda: self.chat.participant1)()
        participant2 = await sync_to_async(lambda: self.chat.participant2)()
        if self.user != participant1 and self.user != participant2:
            await self.close(code=4002)  # Пользовательский код закрытия
            return

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        # Принимаем соединение
        await self.accept()

    async def disconnect(self, close_code):
        """
        Обрабатывает отключение пользователя от WebSocket.
        """
        # Проверяем, существует ли атрибут chat_group_name
        if hasattr(self, 'chat_group_name'):
            # Покидаем группу чата
            await self.channel_layer.group_discard(
                self.chat_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Обрабатывает получение сообщения от пользователя.
        """
        # Парсим JSON-сообщение
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']  # ID отправителя

        # Проверяем, что отправитель совпадает с текущим пользователем
        if str(self.user.id) != str(sender_id):
            await self.send(json.dumps({'error': 'Invalid sender ID'}))
            return

        # Сохраняем сообщение в базе данных
        await self.save_message(self.user, message)

        # Отправляем сообщение в группу чата
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.first_name,
            }
        )

    async def chat_message(self, event):
        """
        Отправляет сообщение всем участникам чата.
        """
        message = event['message']
        sender = event['sender']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

    @sync_to_async
    def get_chat(self, chat_id):
        """
        Получает чат по ID.
        """
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    @sync_to_async
    def get_user(self, user_id):
        """
        Получает пользователя по ID.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, sender, message):
        """
        Сохраняет сообщение в базе данных.
        """
        Message.objects.create(
            chat=self.chat,
            sender=sender,
            content=message
        )
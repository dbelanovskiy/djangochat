from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .models import Room, Message
from .consumers import ChatConsumer


class RoomViewsAndModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.room = Room.objects.create(name='Общий чат', slug='general')
        self.room.members.add(self.user)

    def test_room_and_message_creation(self):
        msg = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Тестовое сообщение'
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(msg.content, 'Тестовое сообщение')
        self.assertIn(self.user, self.room.members.all())

    def test_rooms_list_redirects_anonymous_user(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 302)

    def test_rooms_list_accessible_for_authenticated_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Общий чат')

    def test_single_room_page_accessible(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('room', kwargs={'slug': self.room.slug}))
        self.assertEqual(response.status_code, 200)


class ChatConsumerTest(TransactionTestCase):
    async def test_chat_consumer_send_and_save_message(self):
        # Создаем пользователя и комнату в асинхронном контексте
        user = await database_sync_to_async(User.objects.create_user)(
            username='wsuser', password='password123'
        )
        room = await database_sync_to_async(Room.objects.create)(
            name='WS Room', slug='ws-room'
        )

        # Подключаемся к консьюмеру
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/{room.slug}/")
        communicator.scope['url_route'] = {'kwargs': {'room_name': room.slug}}

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Отправляем сообщение (как это делает ваш фронтенд)
        await communicator.send_json_to({
            'message': 'Привет через WebSocket!',
            'username': user.username,
            'room': room.slug
        })

        # Проверяем ответ от сервера в сокет
        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Привет через WebSocket!')
        self.assertEqual(response['username'], user.username)

        # Проверяем, что save_message действительно сохранил запись в БД
        messages_count = await database_sync_to_async(Message.objects.count)()
        self.assertEqual(messages_count, 1)

        await communicator.disconnect()

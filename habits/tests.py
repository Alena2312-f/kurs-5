from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Habit
from datetime import time


class HabitTests(APITestCase):
    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            tg_chat_id='123456789'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """
        Тест для проверки создания привычки.
        """
        url = reverse('habits:habit_create')
        data = {
            'place': 'Home',
            'time': '10:00:00',
            'action': 'Read a book',
            'is_pleasant': False,
            'periodicity': 1,
            'reward': 'Watch a movie',
            'execution_time': 60,
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)

    def test_get_habit(self):
        """
        Тест для проверки получения привычки.
        """
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(10, 0, 0),
            action='Read a book',
            is_pleasant=False,
            periodicity=1,
            reward='Watch a movie',
            execution_time=60,
            is_public=True
        )
        url = reverse('habits:habit_retrieve', kwargs={'pk': habit.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'Home')

    def test_update_habit(self):
        """
        Тест для проверки обновления привычки.
        """
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(10, 0, 0),
            action='Read a book',
            is_pleasant=False,
            periodicity=1,
            reward='Watch a movie',
            execution_time=60,
            is_public=True
        )
        url = reverse('habits:habit_update', kwargs={'pk': habit.pk})
        data = {
            'place': 'Work',
            'time': '11:00:00',
            'action': 'Write code',
            'is_pleasant': False,
            'periodicity': 1,
            'reward': 'Listen to music',
            'execution_time': 120,
            'is_public': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get().place, 'Work')

    def test_delete_habit(self):
        """
        Тест для проверки удаления привычки.
        """
        habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(10, 0, 0),
            action='Read a book',
            is_pleasant=False,
            periodicity=1,
            reward='Watch a movie',
            execution_time=60,
            is_public=True
        )
        url = reverse('habits:habit_delete', kwargs={'pk': habit.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from habits.tasks import send_telegram_notification


@pytest.mark.django_db
def test_send_telegram_message():
    """
    Тест для Celery задачи send_telegram_notification.
    """
    # Создаем тестового пользователя с tg_chat_id
    user = User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='test@example.com',
        first_name='Test',
        last_name='User',
        tg_chat_id='123456789'
    )

    with patch("telegram_bot.tasks.requests.post") as mock_post:
        # Мокируем успешный ответ от Telegram API
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ok": True}

        user_id = user.id
        message = "Test message"
        result = send_telegram_notification(user_id, message)

        assert result is True  # Задача должна возвращать True при успехе
        mock_post.assert_called_once()  # Проверяем, что requests.post был вызван один раз

        # Получаем аргументы, с которыми был вызван mock_post
        args, kwargs = mock_post.call_args
        # Проверяем, что chat_id и text были переданы в requests.post
        assert kwargs['data']['chat_id'] == '123456789'
        assert kwargs['data']['text'] == message

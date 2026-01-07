from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Habit
from datetime import time


class HabitTests(APITestCase):
    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
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
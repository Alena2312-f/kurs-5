from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Тест для проверки регистрации пользователя.
        """
        User = get_user_model()
        url = reverse('users:register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'tg_chat_id': '123456789'  # Добавляем tg_chat_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertEqual(User.objects.get().first_name, 'Test')
        self.assertEqual(User.objects.get().last_name, 'User')
        self.assertEqual(User.objects.get().tg_chat_id, '123456789')  # Проверяем tg_chat_id

    def test_get_token(self):
        """
        Тест для проверки получения JWT токена.
        """
        User = get_user_model()
        User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            tg_chat_id='123456789'  # Добавляем tg_chat_id
        )
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Проверяем, что tg_chat_id есть в токене
        refresh = RefreshToken(response.data['refresh'])
        self.assertEqual(refresh.payload['username'], 'testuser')
        self.assertEqual(refresh.payload['email'], 'test@example.com')
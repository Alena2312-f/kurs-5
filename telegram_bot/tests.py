from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from telegram_bot.tasks import send_telegram_notification


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

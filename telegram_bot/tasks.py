import os

import requests
from celery import shared_task
from django.conf import settings

chat_id = os.getenv("TELEGRAM_CHAT_ID")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


@shared_task
def send_telegram_notification(user_id, message):
    """
    Отправляет сообщение в Telegram.
    """

    from users.models import (
        User,
    )  # Импортируем модель User здесь, чтобы избежать циклических зависимостей

    user = User.objects.get(pk=user_id)
    chat_id = user.tg_chat_id
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return None
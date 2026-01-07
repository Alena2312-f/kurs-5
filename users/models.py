from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя с добавлением поля tg_chat_id.
    """

    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



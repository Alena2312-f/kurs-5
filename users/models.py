from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя с добавлением поля tg_chat_id.
    """

    username = models.CharField(max_length=50, blank=True, null=True, verbose_name="Username")
    password = models.CharField(max_length=50, verbose_name="Password")
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="First_name")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Last_name")
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Telegram Chat ID"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


    def __str__(self):
        return self.email



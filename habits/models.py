from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import (
    validate_execution_time,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit_and_reward,
    validate_reward_or_related_habit_for_pleasant,
)


class Habit(models.Model):
    """
    Модель привычки.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    place = models.CharField(max_length=150, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=250, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.IntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        validators=[MinValueValidator(1), MaxValueValidator(7), validate_periodicity],
    )
    reward = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Вознаграждение"
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время на выполнение (в секундах)",
        validators=[validate_execution_time],
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        """
        Переопределенный метод clean для валидации модели.
        """
        validate_related_habit_and_reward(self)
        validate_reward_or_related_habit_for_pleasant(self)
        if self.related_habit:
            validate_pleasant_habit(self.related_habit)

    def save(self, *args, **kwargs):
        """
        Переопределенный метод save для вызова clean перед сохранением.
        """
        self.clean()
        super().save(*args, **kwargs)
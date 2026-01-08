from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from habits.models import Habit
from habits.tasks import send_telegram_notification


@receiver(post_save, sender=Habit)
def habit_post_save(sender, instance, created, **kwargs):
    """
    Сигнал, который отправляет уведомление в Telegram при создании или изменении привычки.
    """
    if created:
        message = f"Создана новая привычка: {instance.action} в {instance.time} в {instance.place}"
    else:
        message = f"Обновлена привычка: {instance.action} в {instance.time} в {instance.place}"

    # Рассчитываем время до выполнения привычки (в секундах)
    now = timezone.now().time()
    habit_time = instance.time

    # Если время выполнения привычки уже прошло сегодня, то планируем на завтра
    if habit_time <= now:
        return

    # Планируем отправку уведомления
    send_telegram_notification.apply_async(args=[instance.user__id, message])
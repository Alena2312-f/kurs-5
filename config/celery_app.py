import os

from celery import Celery
from django.conf import settings

# Установите Django settings module для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создайте экземпляр приложения Celery
app = Celery("config")  # Имя приложения Celery (обычно имя проекта)

# Загрузите настройки Celery из Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживайте задачи Celery в файлах tasks.py всех приложений Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

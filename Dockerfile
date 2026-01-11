# Dockerfile (для Celery)

FROM python:3.13

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Устанавливаем переменные окружения (можно переопределить в docker-compose.yml)
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONUNBUFFERED=1

# Команда для запуска Celery worker
CMD ["celery", "-A", "config.celery_app", "worker", "-l", "info"]
# Habit Tracker

## Описание проекта

Это проект Habit Tracker, который помогает пользователям формировать и отслеживать свои привычки, напоминая о них через Telegram. Проект разработан с использованием Django REST Framework, JWT аутентификации, Celery, Redis и PostgreSQL.

## Функциональность

*   **Регистрация и аутентификация:** Пользователи могут регистрироваться и получать JWT токены для доступа к API.
*   **Управление привычками:** Пользователи могут создавать, просматривать, редактировать и удалять свои привычки.
*   **Публичные привычки:** Пользователи могут просматривать список публичных привычек других пользователей.
*   **Уведомления Telegram:** Пользователи получают уведомления в Telegram о необходимости выполнения привычек.
*   **Валидация данных:** Введенные данные проходят валидацию на соответствие заданным правилам.
*   **Пагинация:** Списки привычек разбиты на страницы для удобства просмотра.
*   **Документация API:** Доступна документация API, сгенерированная с помощью drf-yasg (Swagger UI и ReDoc).

## Технологии

*   Python 3.9+
*   Django 4.2+
*   Django REST Framework
*   djangorestframework-simplejwt
*   django-cors-headers
*   psycopg2-binary (PostgreSQL)
*   celery
*   redis
*   python-dotenv
*   drf-yasg
*   pytest
*   pytest-django
*   flake8
*   requests

## Установка

1.  **Клонирование репозитория:**

    ```bash
    git clone <your_repository_url>
    cd habit_tracker
    ```

2.  **Создание и активация виртуального окружения Poetry:**

    ```bash
    poetry install
    poetry shell
    ```

3.  **Установка зависимостей:**

    ```bash
    poetry install
    ```

4.  **Настройка переменных окружения:**

    Создайте файл `.env` в корневой директории проекта и добавьте необходимые переменные:

    ```
    SECRET_KEY=<your_secret_key>
    DEBUG=True  # Или False в production
    DATABASE_URL=postgres://<user>:<password>@<host>:<port>/<database>
    REDIS_URL=redis://<host>:<port>/0
    TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
    TELEGRAM_CHAT_ID=<your_telegram_chat_id>
    ALLOWED_HOSTS=* # Список разрешенных хостов, разделенных запятыми
    ```

    *   `SECRET_KEY`: Секретный ключ Django. Сгенерируйте случайный ключ и вставьте его сюда.  Пример: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    *   `DEBUG`: Режим отладки. `True` для разработки, `False` для production.
    *   `DATABASE_URL`: URL для подключения к базе данных PostgreSQL. Пример: `postgres://user:password@localhost:5432/habit_tracker_db`. Замените `<user>`, `<password>`, `<host>`, `<port>` и `<database>` на ваши значения.  Убедитесь, что база данных PostgreSQL создана.
    *   `REDIS_URL`: URL для подключения к Redis. Пример: `redis://localhost:6379/0`.  Если Redis требует пароль, добавьте его в URL, например: `redis://:password@localhost:6379/0`. Убедитесь, что Redis сервер запущен.
    *   `TELEGRAM_BOT_TOKEN`: Токен вашего Telegram бота.  Укажите токен, полученный от BotFather.
    *   `TELEGRAM_CHAT_ID`:  ID чата с вашим Telegram ботом.  Отправьте любое сообщение боту и используйте `https://api.telegram.org/bot<your_telegram_bot_token>/getUpdates` для получения `chat_id`.
    *   `ALLOWED_HOSTS`: Список разрешенных хостов. В production укажите домены, с которых будет доступен ваш сайт.

5.  **Миграции:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Создание суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Запуск сервера:**

    ```bash
    python manage.py runserver
    ```

8.  **Запуск Celery worker:**

    В отдельном терминале:

    ```bash
    celery -A config worker -l info
    ```

## Использование

1.  **Регистрация пользователя:**

    *   Отправьте `POST` запрос на `/api/users/register/` с данными пользователя (username, password, email, first_name, last_name).

2.  **Получение JWT токена:**

    *   Отправьте `POST` запрос на `/api/token/` с username и password.
    *   Используйте полученный access token в заголовке `Authorization: Bearer <access_token>` для доступа к защищенным эндпоинтам.

3.  **Создание привычки:**

    *   Отправьте `POST` запрос на `/api/habits/create/` с данными привычки (place, time, action, is_pleasant, periodicity, reward, execution_time, is_public).

4.  **Просмотр привычек:**

    *   Отправьте `GET` запрос на `/api/habits/list/` для просмотра списка своих привычек.
    *   Используйте параметр `page` для пагинации (например, `/api/habits/list/?page=2`).

5.  **Просмотр публичных привычек:**

    *   Отправьте `GET` запрос на `/api/habits/public/` для просмотра списка публичных привычек.

6.  **Редактирование и удаление привычек:**

    *   Отправьте `PUT` запрос на `/api/habits/<id>/update/` для редактирования привычки.
    *   Отправьте `DELETE` запрос на `/api/habits/<id>/delete/` для удаления привычки.

## Запуск тестов

```bash
pytest
```

## Документация API
Документация API доступна по адресу:

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/

## Интеграция с Telegram
Для работы с Telegram необходимо:

Создать бота и получить токен от BotFather.
Указать токен в переменной окружения TELEGRAM_BOT_TOKEN.
Узнать chat_id пользователя и указать его в переменной окружения TELEGRAM_CHAT_ID.
Запустить Celery worker для обработки отложенных задач.
Зависимости
Файл pyproject.toml содержит полный список зависимостей проекта.

## Авторы
[Здесь можете указать информацию об авторах проекта]

## Лицензия
[Здесь можете указать информацию о лицензии проекта]
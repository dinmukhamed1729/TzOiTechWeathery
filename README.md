# Weather API

## Описание
Этот проект представляет собой Django REST API для получения информации о погоде. 
Пользователь может зарегистрироваться, войти в систему и получать данные о погоде в своём городе. 
API использует JWT-аутентификацию, кэширование данных о погоде и интеграцию с OpenWeather API.

## Установка и настройка

### 1. Клонирование репозитория
```sh
git clone https://github.com/dinmukhamed1729/TzOiTechWeathery.git
```

### 2. Создание виртуального окружения и установка зависимостей
```sh
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

### 3. Установка необходимых библиотек
Для работы с JWT:
```sh
pip install djangorestframework-simplejwt
```

Для работы с геолокацией (широта и долгота):
```sh
pip install geopy
```

Для работы с PostgreSQL:
```sh
pip install psycopg2-binary
```

### 4. Настройка базы данных PostgreSQL
По умолчанию используется SQLite, но рекомендуется использовать PostgreSQL.
Создайте базу данных `weather_db` и измените настройки в `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'weather_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Создайте базу данных с помощью:
```sh
psql -U your_db_user -c "CREATE DATABASE weather_db;"
```

### 5. Применение миграций и создание суперпользователя
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Запуск сервера
```sh
python manage.py runserver
```

## Использование API

### 1. Регистрация
```http
POST /api/register/
```
Пример тела запроса:
```json
{
    "username": "user1",
    "password": "securepassword",
    "city": "Moscow"
}
```

### 2. Авторизация и получение JWT-токена
```http
POST /api/login
```
Пример тела запроса:
```json
{
    "username": "user1",
    "password": "securepassword"
}
```
Пример ответа:
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

### 3. Получение погоды
Перед запросом замените `your_access_token` на полученный `access_token`.
```http
GET /api/weather/
Authorization: Bearer your_access_token
```

Пример ответа:
```json
{
    "city": "Moscow",
    "temperature": "5",
    "description": "ясно"
}
```

## Дополнительная информация
- Для нахождения широты и долготы города используется `geopy`.
- JWT-токены используются для аутентификации.
- Используется PostgreSQL, но можно заменить на SQLite.
- В файле `views.py` оставлен API_KEY для упрощения тестирования:
  ```python
  API_KEY = 'e6e0d834b2611a5214a3c804278438e0'
  ```
- В корне проекта есть папка `test`, содержащая файл `test.http` с примерами HTTP-запросов.

## Автор
Dinmukhammed


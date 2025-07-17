# Maritime — онлайн-сервис бронирования базы отдыха 🏕️

Maritime — это веб-приложение для онлайн-бронирования номеров и туристических маршрутов. Сайт разработан на Python с использованием фреймворка Flask, с поддержкой как HTML-интерфейса (на Flask-WTF + Bootstrap), так и REST API (на Flask-RESTful + JWT).

## 🚀 Возможности

- Регистрация и вход (по email или телефону)
- Роли пользователей: `guest`, `user`, `manager`, `admin`
- Просмотр и фильтрация номеров по дате и количеству гостей
- Модальные окна с подробностями по номерам
- Бронирование номеров (в том числе без регистрации)
- Личный кабинет и список бронирований
- REST API для бронирования и авторизации

## 🏗️ Архитектура проекта

- **models/** — SQLAlchemy модели (User, Room, Booking, Route и др.)
- **services/** — бизнес-логика (например, BookingService)
- **repositories/** — работа с базой данных (UserRepository и др.)
- **blueprints/** — HTML-интерфейс (user_views, booking_views)
- **api/resources/** — REST API (user_resource, booking_resource, room_resource)
- **forms/** — Flask-WTF формы (LoginForm, RegisterForm, BookingForm)
- **templates/** — Jinja2-шаблоны для страниц
- **static/** — стили, JS, изображения

## 🧪 Технологии

- Python 3.11
- Flask / Flask-Login / Flask-WTF / Flask-RESTful
- SQLAlchemy
- JWT (Flask-JWT-Extended)
- SQLite
- Bootstrap 5
- Flatpickr

## 📦 Установка и запуск

1. Клонируйте репозиторий:

```bash
git clone https://github.com/GRFLD9/Maritime.git
cd Maritime
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/macOS
.venv\Scripts\activate   # для Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` и укажите переменные:

```ini
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/resort.db
JWT_SECRET_KEY=your-jwt-key
ADMIN_EMAIL=admin@example.com
ADMIN_INITIAL_PASSWORD=TempPass123!
```

5. Запустите приложение:

```bash
flask run
```

Откройте в браузере: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔐 Авторизация

- HTML-интерфейс использует Flask-Login
- API использует JWT (в заголовке `Authorization: Bearer <token>`)

## 🔌 Примеры URL-ов

### HTML-интерфейс
- `/login` — вход
- `/register` — регистрация
- `/rooms` — список номеров
- `/bookings` — мои бронирования
- `/profile` — личный кабинет

### REST API (через `api/`)
- `POST /api/login` — вход и получение JWT
- `GET /api/rooms` — список номеров с фильтрацией
- `POST /api/bookings` — создание бронирования

## ✅ Статус проекта

- ✔ Реализовано:
  - Регистрация и вход
  - Просмотр и бронирование номеров
  - HTML + API интерфейсы
  - Личный кабинет

- 🔧 В процессе:
  - Разграничение доступа по ролям
  - Панель администратора
  - Финализация API

## 📌 Репозиторий

[🔗 GitHub: github.com/GRFLD9/Maritime](https://github.com/GRFLD9/Maritime)
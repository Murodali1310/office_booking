# Office Booking CLI

Простой CLI-инструмент для бронирования кабинетов в офисе с хранением данных в SQLite и отправкой уведомлений по Email и SMS.

## Возможности

* Хранение информации о 5 кабинетах и их бронях в базе SQLite.
* Проверка доступности кабинета в заданный промежуток времени (`check`).
* Бронирование кабинета с указанием имени, Email и телефона пользователя (`book`).
* Отправка уведомлений:

  * Email через SMTP с поддержкой STARTTLS.
  * SMS (заглушка, можно подключить реальный API через `requests`).
* Защита от двойного бронирования: при попытке забронировать занятый кабинет выводится информация, кем и до какого времени он занят.

## Требования

* Python 3.8 и выше
* SQLite (встроено в стандартную библиотеку Python)
* `requests` для отправки SMS (если используется реальный API)
* `pytest` для запуска тестов
* `black`, `flake8` для автоформатирования и линтинга

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone git@github.com:Murodali1310/office_booking.git
   cd office_booking
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # или venv\Scripts\activate на Windows
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. (Опционально) Для удобства можете добавить переменные в `~/.bashrc` или `~/.zshrc`:

   ```bash
   export SMTP_HOST=localhost
   export SMTP_PORT=1025
   export EMAIL_FROM="bot@localhost"
   export SMTP_USER=""
   export SMTP_PASS=""
   ```

## Переменные окружения

* `SMTP_HOST` — адрес SMTP-сервера.
* `SMTP_PORT` — порт SMTP-сервера.
* `SMTP_USER` — логин для SMTP (если требуется).
* `SMTP_PASS` — пароль для SMTP (если требуется).
* `EMAIL_FROM` — адрес отправителя в поля From.

## Отладочный SMTP-сервер

Для тестирования Email-уведомлений можно поднять локальный Debug-сервер:

```bash
pip install aiosmtpd         # если ещё не установлен
aiosmtpd -n -l localhost:1025
```

## Использование

### Через `main.py`

```bash
# Проверка доступности
python main.py check \
  --room 1 \
  --start "2025-08-07 09:00" \
  --end   "2025-08-07 10:00"

# Бронирование
python main.py book \
  --room 2 \
  --start "2025-08-07 11:00" \
  --end   "2025-08-07 12:00" \
  --user  "Иван Иванов" \
  --email ivan@example.com \
  --phone +70000000000
```

### Через `python -m booking`

```bash
python -m booking check --room 1 --start "..." --end "..."
python -m booking book  --room 2 --start "..." --end "..." --user "..." --email "..." --phone "..."
```

## Тесты

```bash
pytest -q
```

## .gitignore

```
venv/
booking.db
__pycache__/
*.py[cod]
.pytest_cache/
.vscode/
.idea/
.DS_Store
```

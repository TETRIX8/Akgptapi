# G4F API Server для Vercel

Этот API-сервер предоставляет доступ к различным моделям искусственного интеллекта через библиотеку g4f с помощью RESTful API. Оптимизирован для размещения на Vercel.

## Особенности

- **Множество моделей ИИ**: Доступ к GPT-3.5, GPT-4, Claude, Gemini и другим
- **Управление сессиями**: Создание, получение, обновление и удаление сессий чата
- **Управление историей**: Сохранение и получение истории диалогов
- **Настраиваемые параметры**: Изменение модели, температуры и длины ответа

## Размещение на Vercel

### Предварительные требования

- Аккаунт на [Vercel](https://vercel.com)
- Git (опционально, для деплоя через GitHub)

### Вариант 1: Деплой через GitHub

1. **Создайте репозиторий на GitHub**:
   - Загрузите все файлы из этого архива в репозиторий

2. **Импортируйте проект в Vercel**:
   - Войдите в Vercel
   - Нажмите "Add New" -> "Project"
   - Выберите ваш GitHub репозиторий
   - Нажмите "Import"
   - Настройки по умолчанию подходят для этого проекта
   - Нажмите "Deploy"

### Вариант 2: Деплой через Vercel CLI

1. **Установите Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Войдите в Vercel**:
   ```bash
   vercel login
   ```

3. **Разверните проект**:
   ```bash
   cd /путь/к/проекту
   vercel
   ```

## Структура проекта

- `app.py` - Основной код API-сервера
- `vercel.json` - Конфигурация для Vercel
- `requirements.txt` - Зависимости Python

## API Endpoints

### Основные эндпоинты

- **GET /** - Проверка работоспособности API
- **GET /api/health** - Расширенная проверка работоспособности

### Модели

- **GET /api/models** - Получение списка доступных моделей

### Сессии

- **GET /api/sessions** - Список всех активных сессий
- **POST /api/sessions** - Создание новой сессии
- **GET /api/sessions/{session_id}** - Информация о сессии
- **DELETE /api/sessions/{session_id}** - Удаление сессии

### Настройки сессии

- **PUT /api/sessions/{session_id}/settings** - Обновление настроек сессии

### История диалога

- **GET /api/sessions/{session_id}/history** - Получение истории диалога
- **DELETE /api/sessions/{session_id}/history** - Очистка истории диалога

### Чат

- **POST /api/sessions/{session_id}/chat** - Отправка сообщения и получение ответа

## Примеры использования

### Создание новой сессии

```bash
curl -X POST https://ваш-проект.vercel.app/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"settings": {"model": "gpt-4o-mini", "temperature": 0.7}}'
```

### Отправка сообщения

```bash
curl -X POST https://ваш-проект.vercel.app/api/sessions/YOUR_SESSION_ID/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Привет, как дела?"}'
```

### Изменение модели

```bash
curl -X PUT https://ваш-проект.vercel.app/api/sessions/YOUR_SESSION_ID/settings \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4"}'
```

### Получение истории диалога

```bash
curl -X GET https://ваш-проект.vercel.app/api/sessions/YOUR_SESSION_ID/history
```

## Важные замечания

- В serverless-окружении Vercel сессии хранятся в памяти и будут сбрасываться при каждом холодном старте
- Для продакшн-использования рекомендуется подключить внешнюю базу данных (например, MongoDB Atlas или Supabase)
- Vercel автоматически предоставляет HTTPS для всех приложений
- Бесплатный план Vercel имеет ограничения на время выполнения функций (10 секунд)

## Преимущества Vercel

- Бесплатный план с хорошими лимитами
- Автоматический HTTPS
- Интеграция с Git для непрерывного деплоя
- Глобальная CDN для быстрого доступа из любой точки мира
- Serverless функции - ваш API запускается по требованию
- Нет "засыпания" как на бесплатном плане Heroku

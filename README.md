# API-сервер G4F - Документация

API-сервер доступен по адресу: https://akgptapi.vercel.app/

## Основные эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/` | Проверка работоспособности API |
| GET | `/api/models` | Получение списка доступных моделей |
| GET | `/api/sessions` | Список всех активных сессий |
| POST | `/api/sessions` | Создание новой сессии |
| GET | `/api/sessions/{session_id}` | Информация о сессии |
| DELETE | `/api/sessions/{session_id}` | Удаление сессии |
| PUT | `/api/sessions/{session_id}/settings` | Обновление настроек сессии |
| GET | `/api/sessions/{session_id}/history` | Получение истории диалога |
| DELETE | `/api/sessions/{session_id}/history` | Очистка истории диалога |
| POST | `/api/sessions/{session_id}/chat` | Отправка сообщения и получение ответа |
| GET | `/api/health` | Расширенная проверка работоспособности |

## Примеры запросов и ответов

### 1. Проверка работоспособности API

**Запрос:**
```
GET https://akgptapi.vercel.app/
```

**Ответ:**
```json
{
  "success": true,
  "message": "G4F API Server is running",
  "version": "1.0.0",
  "timestamp": "2025-05-26T19:33:00.000Z"
}
```

### 2. Получение списка моделей

**Запрос:**
```
GET https://akgptapi.vercel.app/api/models
```

**Ответ:**
```json
{
  "success": true,
  "models": [
    {
      "id": "gpt-3.5-turbo",
      "name": "GPT-3.5 Turbo",
      "description": "Fast and efficient"
    },
    {
      "id": "gpt-4",
      "name": "GPT-4",
      "description": "Advanced reasoning"
    },
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "description": "Latest GPT-4 version"
    },
    {
      "id": "gpt-4o-mini",
      "name": "GPT-4o Mini",
      "description": "Compact but powerful"
    },
    {
      "id": "claude-3-opus",
      "name": "Claude-3 Opus",
      "description": "Anthropic's flagship model"
    },
    {
      "id": "claude-3-sonnet",
      "name": "Claude-3 Sonnet",
      "description": "Balanced Claude model"
    },
    {
      "id": "gemini-pro",
      "name": "Gemini Pro",
      "description": "Google's AI model"
    }
  ]
}
```

### 3. Создание новой сессии

**Запрос:**
```
POST https://akgptapi.vercel.app/api/sessions
Content-Type: application/json

{
  "settings": {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "web_search": false
  }
}
```

**Ответ:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "settings": {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
    "web_search": false
  }
}
```

### 4. Отправка сообщения и получение ответа

**Запрос:**
```
POST https://akgptapi.vercel.app/api/sessions/550e8400-e29b-41d4-a716-446655440000/chat
Content-Type: application/json

{
  "message": "Расскажи о квантовой физике"
}
```

**Ответ:**
```json
{
  "success": true,
  "response": "Квантовая физика — это раздел физики, изучающий свойства и поведение материи и энергии на атомном и субатомном уровнях. Она возникла в начале XX века и произвела революцию в нашем понимании микромира...",
  "history": [
    {
      "role": "user",
      "content": "Расскажи о квантовой физике"
    },
    {
      "role": "assistant",
      "content": "Квантовая физика — это раздел физики, изучающий свойства и поведение материи и энергии на атомном и субатомном уровнях. Она возникла в начале XX века и произвела революцию в нашем понимании микромира..."
    }
  ]
}
```

### 5. Получение истории диалога

**Запрос:**
```
GET https://akgptapi.vercel.app/api/sessions/550e8400-e29b-41d4-a716-446655440000/history
```

**Ответ:**
```json
{
  "success": true,
  "history": [
    {
      "role": "user",
      "content": "Расскажи о квантовой физике"
    },
    {
      "role": "assistant",
      "content": "Квантовая физика — это раздел физики, изучающий свойства и поведение материи и энергии на атомном и субатомном уровнях. Она возникла в начале XX века и произвела революцию в нашем понимании микромира..."
    }
  ]
}
```

### 6. Изменение настроек сессии

**Запрос:**
```
PUT https://akgptapi.vercel.app/api/sessions/550e8400-e29b-41d4-a716-446655440000/settings
Content-Type: application/json

{
  "model": "gpt-4",
  "temperature": 0.9
}
```

**Ответ:**
```json
{
  "success": true,
  "settings": {
    "model": "gpt-4",
    "temperature": 0.9,
    "max_tokens": 1000,
    "web_search": false
  }
}
```

### 7. Очистка истории диалога

**Запрос:**
```
DELETE https://akgptapi.vercel.app/api/sessions/550e8400-e29b-41d4-a716-446655440000/history
```

**Ответ:**
```json
{
  "success": true,
  "message": "History cleared"
}
```

### 8. Удаление сессии

**Запрос:**
```
DELETE https://akgptapi.vercel.app/api/sessions/550e8400-e29b-41d4-a716-446655440000
```

**Ответ:**
```json
{
  "success": true,
  "message": "Session 550e8400-e29b-41d4-a716-446655440000 deleted"
}
```

## Параметры запросов

### Параметры создания сессии
- `model` - ID модели (gpt-3.5-turbo, gpt-4, gpt-4o, gpt-4o-mini, claude-3-opus, claude-3-sonnet, gemini-pro)
- `temperature` - Температура генерации (0.0-1.0), влияет на креативность ответов
- `max_tokens` - Максимальная длина ответа в токенах
- `web_search` - Включение/отключение поиска в интернете (true/false)

### Параметры отправки сообщения
- `message` - Текст сообщения для отправки модели

## Важные замечания

- В serverless-окружении Vercel сессии хранятся в памяти и будут сбрасываться при каждом холодном старте
- Для продакшн-использования рекомендуется подключить внешнюю базу данных
- Бесплатный план Vercel имеет ограничения на время выполнения функций (10 секунд)
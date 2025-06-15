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
| POST | `/api/sessions/{session_id}/chat` | Отправка сообщения и получение ответа (непотоковый) |
| POST | `/api/sessions/{session_id}/chat/stream` | Отправка сообщения и получение потокового ответа |
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
  


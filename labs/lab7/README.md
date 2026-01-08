# Lab7 — Интеграция с мобильными приложениями (Telegram) + LLM (Ollama)

## Что сделано
Telegram-бот на Python, который принимает текст и возвращает ответ от локальной LLM через Ollama API.

## Файлы
- `bot.py` — логика Telegram-бота (polling)
- `model.py` — Model: вызов Ollama API (`/api/chat`)
- `.env.example` — пример переменных окружения (секреты не коммитить)
- `.gitignore` — исключает `.env`, `venv`, `__pycache__`
- `requirements.txt` — зависимости

## Запуск (Windows PowerShell)
1) Установи Ollama и скачай модель (пример):
```powershell
ollama pull gemma3:4b
```

2) Создай виртуальное окружение и поставь зависимости:
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

3) Создай файл `.env` (скопируй из `.env.example`) и вставь токен бота.

4) Запуск:
```powershell
py bot.py
```

## Проверка
Открой бота в Telegram → `/start` → отправь любой текст.

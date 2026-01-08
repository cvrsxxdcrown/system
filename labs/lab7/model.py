import os
import requests

SYSTEM_PROMPT = (
    "Ты полезный ассистент. Отвечай кратко и по делу на русском языке."
)

def _get_temperature() -> float:
    try:
        return float(os.getenv("TEMPERATURE", "0.7"))
    except ValueError:
        return 0.7


class LLMService:
    """Model: сервис LLM (Ollama)."""

    def __init__(self):
        base = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
        self.url = f"{base}/api/chat"
        self.model = os.getenv("OLLAMA_MODEL", "gemma3:4b").strip()
        self.temperature = _get_temperature()

    def generate(self, prompt: str) -> str:
        prompt = (prompt or "").strip()
        if not prompt:
            return "Пустой запрос. Напиши сообщение 🙂"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "options": {"temperature": self.temperature},
            "stream": False,
        }

        try:
            r = requests.post(self.url, json=payload, timeout=120)
            r.raise_for_status()
            data = r.json()
            return data.get("message", {}).get("content", "").strip() or "Пустой ответ от модели."
        except Exception as e:
            return (
                "Ошибка Ollama API: " + str(e) + "\n"
                "Проверь, что Ollama запущена и модель скачана (например: ollama pull gemma3:4b)."
            )

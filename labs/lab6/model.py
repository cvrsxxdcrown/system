import requests

class LLMService:
    """
    Model: LLM service.
    Реальная версия вызывает локальное API Ollama.
    """

    def __init__(self, model: str = "gemma3:4b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        prompt = (prompt or "").strip()
        if not prompt:
            return "Пустой запрос. Введите текст и попробуйте снова."

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            r = requests.post(self.url, json=payload, timeout=180)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "(пустой ответ от модели)")
        except Exception as e:
            return f"Ошибка вызова Ollama API: {e}"

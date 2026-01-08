async function sendPrompt() {
  const promptEl = document.getElementById("prompt");
  const modelEl = document.getElementById("model");
  const tempEl = document.getElementById("temperature");
  const responseBox = document.getElementById("response");
  const status = document.getElementById("status");

  const prompt = promptEl.value.trim();
  const model = modelEl.value.trim() || "gemma3:4b";
  const temperature = Number(tempEl.value);

  if (!prompt) {
    responseBox.textContent = "Введите текст запроса.";
    return;
  }

  status.textContent = "Отправка...";
  responseBox.textContent = "Ожидание ответа...";

  try {
    const res = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, model, temperature })
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`HTTP ${res.status}: ${text}`);
    }

    const data = await res.json();
    // Ollama /api/generate возвращает поле response
    responseBox.textContent = data.response ?? JSON.stringify(data, null, 2);
    status.textContent = "Готово ✅";
  } catch (e) {
    status.textContent = "Ошибка ❌";
    responseBox.textContent =
      "Не удалось получить ответ.\n\n" +
      "Проверь:\n" +
      "1) Запущена ли Ollama\n" +
      "2) Запущен ли server.py (порт 5000)\n\n" +
      "Текст ошибки:\n" + e;
  }
}

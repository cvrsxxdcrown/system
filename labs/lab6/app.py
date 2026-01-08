from flask import Flask, render_template, request
from model import LLMService

app = Flask(__name__)
llm = LLMService()


@app.route("/", methods=["GET", "POST"])
def index():
    """Controller: принимает HTTP-запрос и возвращает View."""
    answer = None
    prompt = ""
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        answer = llm.generate(prompt)
    return render_template("index.html", answer=answer, prompt=prompt)


if __name__ == "__main__":
    # Запуск: python app.py
    app.run(host="127.0.0.1", port=5050, debug=True)

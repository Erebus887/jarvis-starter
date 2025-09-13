import os
from flask import Flask, request, render_template, jsonify
import openai

# Load your API key (from environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are Jarvis, a helpful assistant for a university student.
Keep answers short, clear, and friendly.
"""

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"answer": "Please type something for Jarvis."}), 400

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]

    # Call OpenAI
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )
    answer = resp["choices"][0]["message"]["content"].strip()
    return jsonify({"answer": answer})

if __name__ == "__main__":
    # Render requires dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

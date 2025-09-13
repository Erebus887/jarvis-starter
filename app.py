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
    try:
        data = request.json
        question = data.get("question")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        # Always return JSON even on errors
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Render requires dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

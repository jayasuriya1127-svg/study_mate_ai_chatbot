import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai
from google.genai import types
from chatbot_config import SYSTEM_PROMPT

load_dotenv()
app = Flask(__name__)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")
client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.1-flash-lite"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please enter a study-related question."}), 400
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
            ),
        )
        return jsonify({"reply": response.text or "I could not generate a response."})
    except Exception:
        return jsonify({"reply": "Sorry, I am unable to respond right now. Please try again."}), 500

if __name__ == "__main__":
    app.run()

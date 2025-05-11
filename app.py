from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyBPX8Xg-ONG2GvDbnnylXriBFOlbIVhSJI'
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "⚠️ אין תשובה.")
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "❌ שגיאה בתקשורת עם Gemini."})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
app = Flask(__name__)

def detect_bot_activity(text):
    bot_keywords = ["buy now", "free", "click here", "subscribe"]
    score = sum(1 for word in bot_keywords if word in text.lower()) / len(bot_keywords)
    return score

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
    score = detect_bot_activity(text)
    return jsonify({"bot_score": score})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

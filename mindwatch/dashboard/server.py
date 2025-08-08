from flask import Flask, jsonify, render_template
import cv2

app = Flask(__name__)

def check_mood():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "Unknown", "😐"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    mood = "HAPPY"
    emoji = "😊"
    for (x, y, w, h) in faces:
        if y + h / 2 > 240:
            mood = "SAD"
            emoji = "😢"
        else:
            mood = "HAPPY"
            emoji = "😊"

    return mood, emoji

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-check")
def run_check():
    mood, emoji = check_mood()
    return jsonify({"mood": mood, "emoji": emoji})

if __name__ == "__main__":
    app.run(debug=True)

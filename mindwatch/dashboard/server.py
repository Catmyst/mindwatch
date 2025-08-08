from flask import Flask, jsonify, render_template, Response
import cv2
from fer import FER

app = Flask(__name__)

# Open webcam once at startup
camera = cv2.VideoCapture(0)

# Emotion detector
detector = FER()

# Store the latest frame globally
latest_frame = None

def detect_mood(frame):
    """Detect emotion from a single frame."""
    result = detector.detect_emotions(frame)

    if result:
        top_emotion, score = detector.top_emotion(frame)
        emoji_map = {
            "happy": "😊",
            "sad": "😢",
            "angry": "😡",
            "surprise": "😲",
            "neutral": "😐",
            "fear": "😨",
            "disgust": "🤢"
        }
        return top_emotion.upper(), emoji_map.get(top_emotion, "😐")
    else:
        return "Unknown", "😐"

def generate_frames():
    """Generate frames for video streaming."""
    global latest_frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            latest_frame = frame.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-check")
def run_check():
    """Run mood detection on the latest frame."""
    global latest_frame
    if latest_frame is None:
        return jsonify({"mood": "Unknown", "emoji": "😐"})
    mood, emoji = detect_mood(latest_frame)
    return jsonify({"mood": mood, "emoji": emoji})

@app.route("/video_feed")
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

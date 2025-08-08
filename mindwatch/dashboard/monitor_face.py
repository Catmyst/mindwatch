import serial
import time
import cv2

# Ganti sesuai port ESP32 kamu
esp = serial.Serial('COM4', 115200)
time.sleep(2)

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_mood = ""

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    mood = "HAPPY"  # default mood

    for (x, y, w, h) in faces:
        # Simulasi: kalau wajah posisinya rendah → sedih
        if y + h / 2 > 240:
            mood = "SAD"
        else:
            mood = "HAPPY"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Kirim ke ESP jika mood berubah
    if mood != last_mood:
        esp.write((mood + "\n").encode())
        print("Kirim:", mood)
        last_mood = mood

    # Tampilkan mood di layar
    cv2.putText(frame, f"Mood: {mood}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if mood == "HAPPY" else (0, 0, 255), 2)
    cv2.imshow("Mood Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

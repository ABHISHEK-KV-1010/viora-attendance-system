import cv2
import numpy as np
import mysql.connector
from datetime import datetime
from insightface.app import FaceAnalysis

# ----------------------------
# MySQL Connection
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Korg2005##",   # CHANGE THIS
    database="face_attendance"
)
cursor = conn.cursor()

# ----------------------------
# Load Face Model (GPU)
# ----------------------------
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

# ----------------------------
# Load Registered Students
# ----------------------------
cursor.execute("SELECT id, name, embedding FROM students")
students = cursor.fetchall()

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

marked_today = set()

cap = cv2.VideoCapture(0)
 

print("Press Q to exit")

while True:
    ret, frame = cap.read()
    faces = app.get(frame)
    for face in faces:
        embedding = face.embedding.astype(np.float32)
        bbox = face.bbox.astype(int)

        best_match = None
        best_score = 0

        for student in students:
            student_id, name, emb_blob = student
            reg_embedding = np.frombuffer(emb_blob, dtype=np.float32)

            score = cosine_similarity(embedding, reg_embedding)

            if score > best_score:
                best_score = score
                best_match = (student_id, name)

        if best_score > 0.5 and best_match:
            student_id, name = best_match
            label = f"{name} ({best_score:.2f})"

            today = datetime.now().date()
            time_now = datetime.now().time()

            if name not in marked_today:
                cursor.execute("""
                    INSERT INTO attendance (student_id, date, time)
                    VALUES (%s, %s, %s)
                """, (student_id, today, time_now))
                conn.commit()

                marked_today.add(name)
                print(f"{name} marked present")

        else:
            label = "Unknown"

        cv2.rectangle(frame, (bbox[0], bbox[1]),
                      (bbox[2], bbox[3]), (0,255,0), 2)

        cv2.putText(frame, label,
                    (bbox[0], bbox[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

    cv2.imshow("Face Attendance System (MySQL)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
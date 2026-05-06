import customtkinter as ctk
import cv2
import numpy as np
import mysql.connector
from PIL import Image, ImageTk
from insightface.app import FaceAnalysis
from datetime import datetime
import sys
import mediapipe as mp
import mediapipe as mp
import smtplib
from email.mime.text import MIMEText

MYSQL_PASSWORD = "Korg2005##"

# Face recognition model
face_app = FaceAnalysis(name="buffalo_l")
face_app.prepare(ctx_id=0)

# Mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Blink detection variables
blink_counter = 0
blink_verified = False
EYE_THRESHOLD = 0.20

def send_email(to_email, name, subject):

    sender_email = "viorapro2025@gmail.com"
    sender_password = "mlov pfrd beax lins"

    body = f"""
Hello {name},

Your attendance has been marked.

Subject: {subject}
Time: {datetime.now()}

Viora Attendance System
"""

    msg = MIMEText(body)

    msg["Subject"] = "Attendance Marked"
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent")

    except Exception as e:
        print("Email error:", e)



def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="face_attendance"
    )


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Viora - Face Attendance")
app.geometry("1000x650")

container = ctk.CTkFrame(app)
container.pack(fill="both", expand=True)


def show_frame(frame_func):
    for widget in container.winfo_children():
        widget.destroy()
    frame_func()


# =============================
# BLINK DETECTION FUNCTIONS
# =============================

def eye_aspect_ratio(eye):

    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))

    ear = (A + B) / (2.0 * C)

    return ear


def detect_blink(frame):

    global blink_counter, blink_verified

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:

        for face_landmarks in result.multi_face_landmarks:

            landmarks = face_landmarks.landmark

            left_eye = [
                (landmarks[33].x, landmarks[33].y),
                (landmarks[160].x, landmarks[160].y),
                (landmarks[158].x, landmarks[158].y),
                (landmarks[133].x, landmarks[133].y),
                (landmarks[153].x, landmarks[153].y),
                (landmarks[144].x, landmarks[144].y)
            ]

            right_eye = [
                (landmarks[362].x, landmarks[362].y),
                (landmarks[385].x, landmarks[385].y),
                (landmarks[387].x, landmarks[387].y),
                (landmarks[263].x, landmarks[263].y),
                (landmarks[373].x, landmarks[373].y),
                (landmarks[380].x, landmarks[380].y)
            ]

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            ear = (left_ear + right_ear) / 2.0

            if ear < EYE_THRESHOLD:
                blink_counter += 1

            if blink_counter >= 2:
                blink_verified = True


# =============================
# HOME PAGE
# =============================

def home_page():

    frame = ctk.CTkFrame(container)
    frame.pack(fill="both", expand=True)

    title = ctk.CTkLabel(frame, text="Viora Face Attendance System", font=("Arial", 28, "bold"))
    title.pack(pady=60)

    if role_global == "admin":

        ctk.CTkButton(
            frame,
            text="Register Student",
            width=300,
            height=50,
            command=lambda: show_frame(register_page)
        ).pack(pady=20)

    if subject_global:

        ctk.CTkButton(
            frame,
            text="Mark Attendance",
            width=300,
            height=50,
            command=lambda: show_frame(lambda: attendance_page(subject_global))
        ).pack(pady=20)


# =============================
# REGISTER STUDENT
# =============================

def register_page():

    frame = ctk.CTkFrame(container)
    frame.pack(fill="both", expand=True)

    cap = cv2.VideoCapture(0)

    def go_back():
        cap.release()
        show_frame(home_page)

    ctk.CTkButton(frame, text="Back", command=go_back).pack(anchor="nw", padx=20, pady=20)

    ctk.CTkLabel(frame, text="Register Student", font=("Arial", 24)).pack(pady=10)

    # -------- INPUT FIELDS --------

    name_entry = ctk.CTkEntry(frame, placeholder_text="Name", width=300)
    name_entry.pack(pady=5)

    reg_entry = ctk.CTkEntry(frame, placeholder_text="Reg No", width=300)
    reg_entry.pack(pady=5)

    user_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
    user_entry.pack(pady=5)

    pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", width=300, show="*")
    pass_entry.pack(pady=5)

    # ✅ NEW EMAIL FIELD
    email_entry = ctk.CTkEntry(frame, placeholder_text="Email", width=300)
    email_entry.pack(pady=5)

    status_label = ctk.CTkLabel(frame, text="")
    status_label.pack()

    cam_label = ctk.CTkLabel(frame, text="")
    cam_label.pack(pady=10)

    # -------- CAMERA --------

    def update_camera():

        ret, frame_cam = cap.read()

        if ret:

            faces = face_app.get(frame_cam)

            for face in faces:

                bbox = face.bbox.astype(int)

                cv2.rectangle(
                    frame_cam,
                    (bbox[0], bbox[1]),
                    (bbox[2], bbox[3]),
                    (0, 255, 0),
                    2
                )

            frame_rgb = cv2.cvtColor(frame_cam, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame_rgb)
            img = img.resize((600, 400))

            imgtk = ImageTk.PhotoImage(img)

            cam_label.configure(image=imgtk)
            cam_label.image = imgtk

        cam_label.after(20, update_camera)

    # -------- REGISTER --------

    def register_student():

        name = name_entry.get()
        regno = reg_entry.get()
        username = user_entry.get()
        password = pass_entry.get()
        email = email_entry.get()   # ✅ read email

        if name == "" or regno == "" or username == "" or password == "" or email == "":
            status_label.configure(text="Fill all fields!", text_color="red")
            return

        ret, frame_cam = cap.read()

        faces = face_app.get(frame_cam)

        if len(faces) == 0:
            status_label.configure(text="No face detected!", text_color="red")
            return

        embedding = faces[0].embedding.astype(np.float32)
        embedding_bytes = embedding.tobytes()

        conn = get_connection()
        cursor = conn.cursor()

        # ✅ INSERT WITH EMAIL
        cursor.execute(
            """
            INSERT INTO students
            (name, regno, username, password, email, embedding)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (name, regno, username, password, email, embedding_bytes)
        )

        conn.commit()
        conn.close()

        status_label.configure(
            text="Student Registered Successfully!",
            text_color="green"
        )

    ctk.CTkButton(
        frame,
        text="Capture & Register",
        command=register_student
    ).pack(pady=15)

    update_camera()


# =============================
# ATTENDANCE PAGE
# =============================

def attendance_page(subject):

    global blink_verified, blink_counter

    frame = ctk.CTkFrame(container)
    frame.pack(fill="both", expand=True)

    cap = None
    students = []
    marked_students = set()

    attendance_time = None
    attendance_start_time = None

    blink_counter = 0
    blink_verified = False

    def go_back():
        if cap:
            cap.release()
        show_frame(home_page)

    ctk.CTkButton(frame, text="Back", command=go_back).pack(anchor="nw", padx=20, pady=20)

    ctk.CTkLabel(frame, text="Automatic Attendance", font=("Arial", 24)).pack(pady=20)
    ctk.CTkLabel(frame, text=f"Subject : {subject}", font=("Arial", 18)).pack(pady=10)

    status_label = ctk.CTkLabel(frame, text="Blink to verify face")
    status_label.pack()

    cam_label = ctk.CTkLabel(frame, text="")

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


    def start_attendance():

        nonlocal cap, attendance_time, attendance_start_time

        today = datetime.now().date()
        attendance_time = datetime.now().time()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,name,regno,embedding FROM students"
        )

        data = cursor.fetchall()

        for student in data:

            student_id, name, regno, emb_blob = student

            if emb_blob is None:
                continue

            embedding = np.frombuffer(emb_blob, dtype=np.float32)

            students.append(
                (student_id, name, regno, embedding)
            )

            cursor.execute(
                """
                INSERT INTO attendance
                (student_id,regno,subject,date,time,status)
                VALUES(%s,%s,%s,%s,%s,'Absent')
                """,
                (student_id, regno, subject, today, attendance_time)
            )

        conn.commit()
        conn.close()

        attendance_start_time = datetime.now()

        cap = cv2.VideoCapture(0)

        cam_label.pack(pady=20)

        update_camera()


    def update_camera():

        nonlocal cap

        if cap is None:
            return

        if (datetime.now() - attendance_start_time).seconds > 60:
            cap.release()
            status_label.configure(
                text="Attendance Closed",
                text_color="yellow"
            )
            return

        ret, frame_cam = cap.read()

        if ret:

            detect_blink(frame_cam)

            faces = face_app.get(frame_cam)

            for face in faces:

                bbox = face.bbox.astype(int)
                embedding = face.embedding.astype(np.float32)

                cv2.rectangle(
                    frame_cam,
                    (bbox[0], bbox[1]),
                    (bbox[2], bbox[3]),
                    (0, 255, 0),
                    2
                )

                best_match = None
                best_score = 0

                for student_id, name, regno, reg_embedding in students:

                    score = cosine_similarity(
                        embedding,
                        reg_embedding
                    )

                    if score > best_score:
                        best_score = score
                        best_match = (
                            student_id,
                            name,
                            regno
                        )

                if best_score > 0.45 and best_match:

                    if not blink_verified:
                        continue

                    student_id, name, regno = best_match

                    if student_id in marked_students:
                        continue

                    today = datetime.now().date()

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        UPDATE attendance
                        SET status='Present'
                        WHERE student_id=%s
                        AND regno=%s
                        AND subject=%s
                        AND date=%s
                        AND time=%s
                        """,
                        (
                            student_id,
                            regno,
                            subject,
                            today,
                            attendance_time
                        )
                    )

                    cursor.execute(
                        "SELECT email FROM students WHERE id=%s",
                        (student_id,)
                    )

                    row = cursor.fetchone()

                    email = None
                    if row:
                        email = row[0]

                    conn.commit()
                    conn.close()

                    marked_students.add(student_id)

                    status_label.configure(
                        text=f"{name} marked Present",
                        text_color="green"
                    )

                    if email:
                        send_email(email, name, subject)

                    cv2.putText(
                        frame_cam,
                        name,
                        (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2
                    )

            frame_rgb = cv2.cvtColor(
                frame_cam,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(frame_rgb)
            img = img.resize((600, 400))

            imgtk = ImageTk.PhotoImage(img)

            cam_label.configure(image=imgtk)
            cam_label.image = imgtk

        cam_label.after(80, update_camera)


    ctk.CTkButton(
        frame,
        text="Start Attendance",
        command=start_attendance
    ).pack(pady=15)

# =============================
# PROGRAM START
# =============================

mode = "home"
subject_global = ""
role_global = "teacher"

if len(sys.argv) > 1:
    mode = sys.argv[1]

if len(sys.argv) > 2:
    subject_global = sys.argv[2]

if len(sys.argv) > 3:
    role_global = sys.argv[3]

if mode == "register":

    if role_global != "admin":
        print("Access Denied: Only admin can register students")
        show_frame(home_page)
    else:
        show_frame(register_page)

elif mode == "attendance":

    if subject_global == "":
        print("Subject not provided")
        show_frame(home_page)
    else:
        show_frame(lambda: attendance_page(subject_global))

else:

    show_frame(home_page)

app.mainloop()
import customtkinter as ctk
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from database import get_connection


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Initialize face model
app_face = FaceAnalysis(name="buffalo_l")
app_face.prepare(ctx_id=0)


def start_registration(name):

    if name == "":
        print("Enter student name")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        faces = app_face.get(frame)

        for face in faces:

            embedding = face.embedding

            # convert embedding to binary
            emb_bytes = np.array(embedding).tobytes()

            cursor.execute(
                "INSERT INTO students (name, embedding) VALUES (%s,%s)",
                (name, emb_bytes)
            )

            conn.commit()

            print("Student Registered:", name)

            cap.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Register Face - Press Q to Exit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# -------- GUI --------

def open_register_window():

    win = ctk.CTk()
    win.title("Register Student")
    win.geometry("400x300")

    title = ctk.CTkLabel(win,
                         text="Register Student",
                         font=("Arial",24,"bold"))
    title.pack(pady=20)

    name_entry = ctk.CTkEntry(
        win,
        placeholder_text="Enter Student Name",
        width=250
    )
    name_entry.pack(pady=20)

    def register():

        name = name_entry.get()
        start_registration(name)

    register_btn = ctk.CTkButton(
        win,
        text="Start Face Registration",
        command=register
    )

    register_btn.pack(pady=20)

    win.mainloop()


# Run window
if __name__ == "__main__":
    open_register_window()
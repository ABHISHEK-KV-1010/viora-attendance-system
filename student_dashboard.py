import customtkinter as ctk
import mysql.connector
import sys


# ---------- DB ----------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Korg2005##",
        database="face_attendance"
    )


# ---------- GET LOGIN DATA ----------

if len(sys.argv) >= 3:
    student_name = sys.argv[1]
    regno = sys.argv[2]
else:
    student_name = "Unknown"
    regno = "0"


# ---------- GUI ----------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x650")
app.title("Student Dashboard")


# ---------- HEADER ----------

header = ctk.CTkFrame(app, corner_radius=20, fg_color="#1f1f1f")
header.pack(fill="x", padx=20, pady=15)

title = ctk.CTkLabel(
    header,
    text="📊 Student Dashboard",
    font=("Arial", 30, "bold")
)
title.pack(pady=(15, 5))

info = ctk.CTkLabel(
    header,
    text=f"👤 {student_name}   |   🆔 {regno}",
    font=("Arial", 15),
    text_color="#aaaaaa"
)
info.pack(pady=(0, 15))


# ---------- SUMMARY CARDS ----------

summary_frame = ctk.CTkFrame(app, fg_color="transparent")
summary_frame.pack(fill="x", padx=20)

card1 = ctk.CTkFrame(summary_frame, corner_radius=20, fg_color="#2c2c2c")
card1.pack(side="left", expand=True, fill="x", padx=10, pady=10)

card2 = ctk.CTkFrame(summary_frame, corner_radius=20, fg_color="#2c2c2c")
card2.pack(side="left", expand=True, fill="x", padx=10, pady=10)

total_subjects_label = ctk.CTkLabel(card1, text="0", font=("Arial", 28, "bold"))
total_subjects_label.pack(pady=(15, 0))

ctk.CTkLabel(card1, text="Subjects", text_color="#bbbbbb").pack(pady=(0, 15))


avg_label = ctk.CTkLabel(card2, text="0%", font=("Arial", 28, "bold"))
avg_label.pack(pady=(15, 0))

ctk.CTkLabel(card2, text="Average Attendance", text_color="#bbbbbb").pack(pady=(0, 15))


# ---------- REFRESH BUTTON ----------

def refresh():
    for widget in frame.winfo_children():
        widget.destroy()
    load_attendance()

refresh_btn = ctk.CTkButton(
    app,
    text="🔄 Refresh Dashboard",
    corner_radius=25,
    height=40,
    font=("Arial", 14, "bold"),
    command=refresh
)
refresh_btn.pack(pady=10)


# ---------- MAIN FRAME ----------

frame = ctk.CTkScrollableFrame(app, corner_radius=20)
frame.pack(fill="both", expand=True, padx=20, pady=10)


# ---------- GET ATTENDANCE ----------

def load_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT subject FROM attendance")
    subjects = cursor.fetchall()

    total_subjects = len(subjects)
    total_percent = 0

    row = 0

    for s in subjects:

        subject = s[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT date,time)
            FROM attendance
            WHERE subject=%s
        """, (subject,))
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE subject=%s
            AND regno=%s
            AND status='Present'
        """, (subject, regno))
        attended = cursor.fetchone()[0]

        percent = 0
        if total > 0:
            percent = round((attended / total) * 100, 2)

        total_percent += percent

        # ---------- COLOR ----------

        if percent >= 75:
            color = "#2ecc71"
        elif percent >= 50:
            color = "#f1c40f"
        else:
            color = "#e74c3c"


        # ---------- MODERN CARD ----------

        card = ctk.CTkFrame(
            frame,
            corner_radius=20,
            fg_color="#252525"
        )
        card.grid(row=row, column=0, sticky="ew", pady=12, padx=5)

        frame.grid_columnconfigure(0, weight=1)

        # Left Side Info
        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", padx=15, pady=15)

        ctk.CTkLabel(
            left,
            text=subject,
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text=f"Total: {total}   |   Attended: {attended}",
            text_color="#aaaaaa"
        ).pack(anchor="w", pady=3)


        # Right Side Percent Circle Style
        right = ctk.CTkFrame(card, fg_color="transparent")
        right.pack(side="right", padx=20)

        percent_box = ctk.CTkFrame(
            right,
            width=70,
            height=70,
            corner_radius=35,
            fg_color=color
        )
        percent_box.pack()

        ctk.CTkLabel(
            percent_box,
            text=f"{int(percent)}%",
            font=("Arial", 14, "bold"),
            text_color="black"
        ).place(relx=0.5, rely=0.5, anchor="center")

        row += 1

    # ---------- SUMMARY UPDATE ----------

    avg = 0
    if total_subjects > 0:
        avg = round(total_percent / total_subjects, 2)

    total_subjects_label.configure(text=str(total_subjects))
    avg_label.configure(text=f"{avg}%")

    conn.close()


load_attendance()


app.mainloop()
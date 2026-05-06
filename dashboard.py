import customtkinter as ctk
import mysql.connector
import subprocess
import sys
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Dashboard(ctk.CTk):

    def __init__(self, teacher_name="User", subject="", role="teacher"):
        super().__init__()

        self.title("Viora Dashboard")
        self.geometry("1200x700")

        self.teacher_name = teacher_name
        self.subject = subject
        self.role = role

        # ---------- ICONS ----------

        self.icon_user = ctk.CTkImage(Image.open("user (1).png"), size=(80, 80))

        self.icon_register = ctk.CTkImage(
            Image.open("register1.png"), size=(100, 100)
        )
        self.icon_attendance = ctk.CTkImage(
            Image.open("attendence.png"), size=(100, 100)
        )
        self.icon_report = ctk.CTkImage(
            Image.open("combo-chart.png"), size=(100, 100)
        )
        self.icon_logout = ctk.CTkImage(
            Image.open("logout-rounded-left.png"), size=(30, 30)
        )

        self.buttons = []

        # ---------- LEFT PANEL ----------

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color="#1e1e2f")
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="Viora",
            font=("Arial", 28, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.sidebar,
            image=self.icon_user,
            text=""
        ).pack(pady=10)

        ctk.CTkLabel(
            self.sidebar,
            text=f"Name: {self.teacher_name}",
            font=("Arial", 16)
        ).pack(pady=5)

        ctk.CTkLabel(
            self.sidebar,
            text=f"Role: {self.role}",
            font=("Arial", 16)
        ).pack(pady=5)

        ctk.CTkLabel(
            self.sidebar,
            text=f"Subject: {self.subject}",
            font=("Arial", 16)
        ).pack(pady=5)

        # ---------- MAIN ----------

        self.main = ctk.CTkFrame(self, fg_color="#2b2b2b")
        self.main.pack(fill="both", expand=True)

        self.show_home()

        self.bind("<Configure>", self.resize_icons)

    # ---------- RESIZE ----------

    def resize_icons(self, event):

        w = self.winfo_width()

        size = max(80, int(w / 10))

        btn_w = max(150, int(w / 10))
        btn_h = max(120, int(w / 16))

        self.icon_register.configure(size=(size, size))
        self.icon_attendance.configure(size=(size, size))
        self.icon_report.configure(size=(size, size))

        for b in self.buttons:
            b.configure(width=btn_w, height=btn_h)

    # ---------- DB ----------

    def get_connection(self):

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Korg2005##",
            database="face_attendance"
        )

    # ---------- HOME ----------

    def show_home(self):

        for widget in self.main.winfo_children():
            widget.destroy()

        self.buttons.clear()

        # ---------- TOP BAR ----------

        top = ctk.CTkFrame(self.main, height=50, fg_color="#3a3a3a")
        top.pack(fill="x")

        logout_btn = ctk.CTkButton(
            top,
            text="Logout",
            image=self.icon_logout,
            compound="left",
            fg_color="#d32f2f",
            command=self.logout
        )
        logout_btn.pack(side="left", padx=10, pady=5)

        ctk.CTkLabel(
            top,
            text="Dashboard",
            font=("Arial", 20, "bold")
        ).pack()

        # ---------- BUTTON AREA (TOP CENTER) ----------

        center = ctk.CTkFrame(self.main, fg_color="#2b2b2b")
        center.pack(anchor="n", pady=40)

        center.grid_columnconfigure((0, 1, 2), weight=1)

        def make_btn(text, icon, cmd, col):

            btn = ctk.CTkButton(
                center,
                text=text,
                image=icon,
                compound="top",
                font=("Arial", 14, "bold"),
                fg_color="#1976d2",
                hover_color="#0d47a1",
                width=180,
                height=140,
                command=cmd
            )

            btn.grid(row=0, column=col, padx=20, pady=10)

            self.buttons.append(btn)

        col = 0

        if self.role == "admin":
            make_btn("Register", self.icon_register, self.open_register, col)
            col += 1

        make_btn("Attendance", self.icon_attendance, self.open_attendance, col)
        col += 1

        make_btn("Report", self.icon_report, self.open_report, col)

    # ---------- REGISTER ----------

    def open_register(self):

        subprocess.Popen([
            sys.executable,
            "viora_gui.py",
            "register",
            "",
            self.role
        ])

    # ---------- ATTENDANCE ----------

    def open_attendance(self):

        subprocess.Popen([
            sys.executable,
            "viora_gui.py",
            "attendance",
            self.subject,
            self.role
        ])

    # ---------- REPORT ----------

    def open_report(self):

        for widget in self.main.winfo_children():
            widget.destroy()

        ctk.CTkButton(
            self.main,
            text="← Back",
            command=self.show_home
        ).pack(anchor="nw", padx=10, pady=10)

        ctk.CTkLabel(
            self.main,
            text=f"{self.subject} Attendance %",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        table = ctk.CTkFrame(self.main)
        table.pack(fill="both", expand=True, padx=20, pady=20)

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
        students.name,
        SUM(attendance.status='Present'),
        COUNT(*),
        ROUND((SUM(attendance.status='Present')/COUNT(*))*100,2)
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        WHERE attendance.subject=%s
        GROUP BY students.id
        """, (self.subject,))

        records = cursor.fetchall()

        conn.close()

        headers = ["Student", "Present", "Total", "%"]

        for col, h in enumerate(headers):
            ctk.CTkLabel(
                table,
                text=h,
                font=("Arial", 16, "bold")
            ).grid(row=0, column=col, padx=40, pady=10)

        for r, row in enumerate(records, start=1):
            for c, val in enumerate(row):
                ctk.CTkLabel(
                    table,
                    text=str(val)
                ).grid(row=r, column=c, padx=40, pady=5)

    # ---------- LOGOUT ----------

    def logout(self):

        self.destroy()

        subprocess.Popen([
            sys.executable,
            "login.py"
        ])


if __name__ == "__main__":

    teacher_name = "User"
    subject = ""
    role = "teacher"

    if len(sys.argv) >= 4:
        teacher_name = sys.argv[1]
        subject = sys.argv[2]
        role = sys.argv[3]

    app = Dashboard(teacher_name, subject, role)
    app.mainloop()
import sys
import os
import mysql.connector 
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Korg2005##",
        database="face_attendance"
    )


# ✅ THIS IS IMPORTANT
class Page(QWebEnginePage):

    def acceptNavigationRequest(self, url, _type, isMainFrame):

        url_str = url.toString()

        if url_str.startswith("login://"):

            data = url_str.replace("login://", "")

            try:
                username, password, user_type = data.split("//")
            except:
                return False

            print(username, password, user_type)

            conn = get_connection()
            cursor = conn.cursor()

            if user_type == "Teacher":

                cursor.execute(
                    "SELECT id,name,subject,role FROM teachers WHERE username=%s AND password=%s",
                    (username, password)
                )

                user = cursor.fetchone()

                if user:

                    teacher_id, name, subject, role = user

                    subprocess.Popen([
                        sys.executable,
                        "dashboard.py",
                        name,
                        subject,
                        role,
                        str(teacher_id)
                    ])

                    sys.exit()

            else:

                cursor.execute(
                    "SELECT name,regno FROM students WHERE username=%s AND password=%s",
                    (username, password)
                )

                user = cursor.fetchone()

                if user:

                    name, regno = user

                    subprocess.Popen([
                        sys.executable,
                        "student_dashboard.py",
                        name,
                        regno
                    ])

                    sys.exit()

            conn.close()

            return False

        return super().acceptNavigationRequest(url, _type, isMainFrame)


app = QApplication(sys.argv)

view = QWebEngineView()

page = Page()
view.setPage(page)

path = os.path.abspath("login.html")

view.load(QUrl.fromLocalFile(path))

view.resize(1000, 600)
view.show()

sys.exit(app.exec())
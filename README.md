# 🎯 AI-Based Face Recognition Attendance System

A professional real-time attendance management system powered by **InsightFace (ArcFace)**, **RetinaFace**, and **GPU-accelerated deep learning**.

The system automatically detects, recognizes, and verifies student identities through facial biometrics and records attendance with timestamps, eliminating manual attendance processes and reducing proxy attendance.

---

## 🚀 Features

✅ Real-Time Face Detection

✅ High Accuracy Face Recognition using ArcFace

✅ GPU Acceleration (NVIDIA RTX Support)

✅ Automatic Attendance Logging

✅ Duplicate Attendance Prevention

✅ Student Registration Module

✅ Facial Embedding Database

✅ CSV / SQLite Attendance Storage

✅ Modular & Scalable Architecture

---

## 🏗️ System Architecture

```text
Camera Input
      │
      ▼
 Face Detection
   (RetinaFace)
      │
      ▼
 Face Recognition
    (ArcFace)
      │
      ▼
512-D Face Embeddings
      │
      ▼
Cosine Similarity Matching
      │
      ▼
Attendance Database
      │
      ▼
Attendance Report

🧠 Technologies Used
Category	Technology
Language	Python 3.11
Face Detection	RetinaFace
Face Recognition	ArcFace
Framework	InsightFace
Computer Vision	OpenCV
Numerical Processing	NumPy
Data Handling	Pandas
Runtime	ONNX Runtime GPU
Database	CSV / SQLite
Hardware	NVIDIA RTX GPU
📂 Project Structure

FaceRecognitionAttendance/
│
├── dataset/
│   ├── student1/
│   ├── student2/
│   └── ...
│
├── embeddings/
│   └── embeddings.pkl
│
├── attendance/
│   └── attendance.csv
│
├── models/
│
├── register.py
├── recognize.py
├── attendance.py
├── database.py
│
├── requirements.txt
└── README.md

⚙️ Installation
Clone Repository

git clone https://github.com/yourusername/FaceRecognitionAttendance.git

cd FaceRecognitionAttendance

Create Virtual Environment

python -m venv venv

Activate:
Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

🔥 Running the Project
Student Registration

python register.py

Captures and stores facial embeddings.
Start Attendance System

python recognize.py

Detects faces in real time and marks attendance automatically.
📊 Attendance Output

Example:
Student Name	Date	Time
John Doe	26-06-2026	09:05:12
Alice Smith	26-06-2026	09:08:41
🎯 Methodology
Step 1: Face Detection

RetinaFace detects faces from the live camera feed.
Step 2: Face Recognition

ArcFace generates a 512-dimensional facial embedding.
Step 3: Similarity Matching

Cosine similarity compares incoming embeddings against stored embeddings.
Step 4: Attendance Logging

Verified identities are recorded with date and time.
📈 Advantages

    High Recognition Accuracy

    Fast Real-Time Processing

    Contactless Attendance

    Eliminates Proxy Attendance

    Easily Scalable

    GPU Accelerated

🔒 Future Enhancements

    Web Dashboard

    Mobile Application

    Cloud Database Integration

    Multi-Camera Support

    Face Mask Recognition

    Analytics Dashboard

    RFID + Face Recognition Hybrid Authentication

📚 Research Background

This project is based on modern deep-learning face recognition techniques:

    ArcFace (Deng et al., 2019)

    RetinaFace

    InsightFace Framework

    ONNX Runtime GPU


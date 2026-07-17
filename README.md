# 💊 Khurakh – AI-Powered Medicine Scanner & Medical Assistant

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![EasyOCR](https://img.shields.io/badge/EasyOCR-OCR-orange?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama%203.3-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

## 📖 About

**Khurakh** is an AI-powered healthcare web application that helps users instantly identify medicines and understand their purpose using **Computer Vision, OCR, Artificial Intelligence, and Full Stack Development**.

Instead of manually searching for medicine information, users can simply upload a picture of a medicine strip. The application extracts the medicine name using OCR, searches a medicine database, and displays detailed information such as:

- 💊 Medicine Name
- 🧪 Composition
- ✅ Uses
- ⚠️ Side Effects
- 💰 Price
- 🔄 Alternative Medicines

If the medicine is not available in the local database, **Groq LLaMA 3.3** intelligently generates structured medicine information in real time, ensuring users always receive helpful information.

---

# 🚀 Key Features

### 📸 AI Medicine Scanner

- Upload medicine strip images
- OCR-based text extraction using EasyOCR
- Automatic medicine name detection

---

### 🔍 Smart Medicine Search

- Searches a medicine database
- Exact matching
- Fuzzy matching using SequenceMatcher
- Handles OCR spelling mistakes

---

### 🤖 AI Fallback System

If a medicine is unavailable in the database:

- Queries Groq LLaMA 3.3 (70B)
- Generates structured medicine information
- Provides:
  - Uses
  - Side Effects
  - Precautions
  - Composition (when available)

---

### 💬 AI Medical Chatbot

Ask natural language questions such as:

- What is Crocin used for?
- Can I take Paracetamol after food?
- What are the side effects of Augmentin?
- Explain this medicine in simple language.

---

### 📊 Intelligent Medicine Database

- CSV-based medicine dataset
- Fast lookups using Pandas
- Easily expandable database

---

# 🧠 AI Workflow

```text
                 Medicine Image
                       │
                       ▼
                 EasyOCR Engine
                       │
                       ▼
            Medicine Name Extraction
                       │
                       ▼
           Fuzzy Database Matching
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Medicine Found      Medicine Not Found
             │                   │
             ▼                   ▼
      Database Result     Groq LLaMA 3.3
             │                   │
             └─────────┬─────────┘
                       ▼
          Structured Medicine Details
                       ▼
             Frontend Result Display
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- Uvicorn

---

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Cropper.js

---

## AI / Machine Learning

- EasyOCR
- Groq API
- LLaMA 3.3 70B
- OCR Pipeline
- Fuzzy String Matching

---

## Data Processing

- Pandas
- NumPy

---

# 📂 Project Structure

```text
Khurakh
│
├── backend
│   ├── api.py
│   ├── services
│   │      └── ocr_service.py
│   ├── datasets
│   │      └── FINAL_DATASET.csv
│   └── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets
│
└── README.md
```

---

# 📷 Screenshots

## 🏠 Home Page

<img width="1918" height="931" alt="image" src="https://github.com/user-attachments/assets/996e1585-80f7-4f3f-8cea-39f1c3899901" />

---

## 🔍 Medicine Search

<img width="1918" height="932" alt="image" src="https://github.com/user-attachments/assets/468fbd9b-7f62-4ba8-a6e0-1767830d8d97" />

---

## 📸 OCR Scanner

<img width="1918" height="927" alt="image" src="https://github.com/user-attachments/assets/88a4b918-ccaf-449a-ac38-b8637f8b3112" />

---

## 💬 AI Chatbot


<img width="1918" height="927" alt="image" src="https://github.com/user-attachments/assets/ca779ba3-405b-4d6f-8cac-251ae30f0ca2" />
<img width="1912" height="693" alt="image" src="https://github.com/user-attachments/assets/cff6e93d-b038-4859-b301-ab04392f8450" />


# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Akshit172005/Khurakh.git
```

---

## 2️⃣ Navigate to Project

```bash
cd Khurakh
```

---

## 3️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 4️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 5️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Start Backend

```bash
cd backend
python -m uvicorn api:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

---

## 7️⃣ Start Frontend

Open

```
frontend/index.html
```

using **Live Server** in VS Code or any local web server.

---

# 🔌 API Endpoints

## Search Medicine

```
GET /search
```

Example

```
/search?query=paracetamol
```

---

## Scan Medicine

```
POST /upload
```

Upload an image using multipart/form-data.

---

## AI Chatbot

```
POST /chat
```

Example Request

```json
{
  "message": "What is Crocin used for?"
}
```

---

# 🌟 Highlights

✅ OCR-based medicine recognition

✅ AI-powered medicine explanation

✅ Intelligent fuzzy matching

✅ FastAPI backend

✅ Lightweight architecture

✅ Modern responsive UI

✅ Real-time AI chatbot

---

# 🚀 Future Improvements

- 📱 Mobile Application
- 📦 Barcode Scanner
- 🎙 Voice Search
- 📑 Prescription Scanner
- 🏥 Nearby Pharmacy Locator
- ❤️ Save Favorite Medicines
- 🔐 User Authentication
- 🌙 Dark Mode
- ☁ Cloud Database
- 🌍 Multi-language Support

---

# 👨‍💻 Author

## Akshit Gupta

**B.Tech Computer Science (Data Science)**

Bennett University

### GitHub

https://github.com/Akshit172005

### LinkedIn

_Add your LinkedIn profile here_

---

# ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub!

It helps others discover the project and motivates further development.

---

## ⚠️ Disclaimer

Khurakh is developed for **educational and informational purposes only**.

The information provided by the application should **not** be considered professional medical advice. Always consult a qualified healthcare professional before taking or changing any medication.

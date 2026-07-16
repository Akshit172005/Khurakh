# 💊 Khurakh - AI-Powered Medicine Scanner & Assistant

Khurakh is an AI-first, full-stack web application designed to eliminate information asymmetry in the healthcare domain. It allows users to scan physical medicine strips using Computer Vision (OCR) to instantly retrieve critical data such as uses, side effects, and composition. 

If a medicine is not found in the local database, Khurakh utilizes a generative AI fallback (Groq LLaMA 3.3) to dynamically generate the required structured data and feeds it back into the dataset for continuous self-learning.

## 🚀 Features
* **Computer Vision (OCR):** Upload or capture an image of a medicine strip. The app uses `EasyOCR` to extract unstructured text and isolates the medicine name.
* **Fuzzy Database Matching:** Uses string similarity (`SequenceMatcher`) to query a massive Pandas-managed dataset for exact or closest matches.
* **Generative AI Fallback:** Integrates the **Groq API (LLaMA 3.3 70B)** to automatically generate missing medicine data in a strict JSON format.
* **Self-Learning Pipeline:** AI-generated results are automatically cleaned and appended to the core `FINAL_DATASET.csv` file, making the system smarter with every unknown scan.
* **Medical Chatbot:** A built-in AI assistant to answer general medicine and health-related queries.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI & ML:** EasyOCR, Groq API (LLaMA 3.3 70B), Pandas, NumPy
* **Frontend:** HTML, CSS, Vanilla JavaScript, Cropper.js

## 💻 How to Run Locally

### 1. Clone the Repository
git clone https://github.com/Akshit172005/Khurakh.git

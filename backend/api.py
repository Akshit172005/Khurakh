from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import os
import shutil
import tempfile
from difflib import SequenceMatcher
import json
import numpy as np

# -------------------------------
# 🤖 GROQ CLIENT
# -------------------------------
from openai import OpenAI

client = OpenAI(
    api_key="-",  # 🔥 REPLACE WITH YOUR GROQ API KEY BEFORE SUBMISSION
    base_url="https://api.groq.com/openai/v1"
)

# -------------------------------
# INIT APP
# -------------------------------
app = FastAPI(title="Khurakh API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# LOAD DATA
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets")
FILE_PATH = os.path.join(DATASET_PATH, "FINAL_DATASET.csv")

df = pd.read_csv(FILE_PATH)

df["name"] = df["name"].astype(str)
df["name_clean"] = df["name"].str.lower().str.strip()

# ✅ CLEAN DATA (IMPORTANT)
df = df.replace([np.inf, -np.inf], 0)
df = df.fillna("")

# -------------------------------
# SIMILARITY FUNCTION
# -------------------------------
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# -------------------------------
# 🔍 CENTRALIZED SEARCH HELPER
# -------------------------------
def search_medicine(query):
    global df
    query_clean = query.lower().strip()

    # Create a copy to avoid overriding global state during concurrent API calls
    temp_df = df.copy()
    temp_df["score"] = temp_df["name_clean"].apply(
        lambda x: similarity(query_clean, x)
    )

    exact = temp_df[temp_df["name_clean"] == query_clean]

    if not exact.empty:
        results = exact
    else:
        results = temp_df.sort_values(by="score", ascending=False).head(5)
        results = results[
            (results["score"] > 0.55) |
            (results["name_clean"].str.contains(query_clean, na=False))
        ]

    return results

# -------------------------------
# 🔍 SEARCH API
# -------------------------------
@app.get("/search")
def search(query: str):
    query_clean = query.lower().strip()
    
    # 1. Try Database First
    results = search_medicine(query_clean)

    if not results.empty:
        output = []
        for _, row in results.iterrows():
            output.append({
                "name": str(row["name"]) if pd.notna(row["name"]) else "",
                "price": str(row["price"]) if pd.notna(row.get("price")) else "N/A",
                "composition": f"{row.get('composition', '')}, {row.get('composition2', '')}".strip(", "),
                "uses": str(row.get("uses")) if pd.notna(row.get("uses")) else "N/A",
                "side_effects": str(row.get("side_effects")) if pd.notna(row.get("side_effects")) else "N/A",
                "precautions": "Consult your doctor for detailed precautions.",
                "alternatives": str(row.get("substitutes", "")).split(",")[:3] if row.get("substitutes") else [],
                "score": float(row["score"]) if pd.notna(row["score"]) else 0.0,
                "source": "database"
            })
        
        output = json.loads(json.dumps(output, default=str))
        return {"results": output}

    # 2. AI Fallback (If not found in database)
    print("🚀 USING AI FALLBACK FOR SEARCH")
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a medical assistant.
Give response EXACTLY in this format:

USER_OUTPUT:
Uses:
- point 1
- point 2

Side Effects:
- point 1
- point 2

Precautions:
- point 1
- point 2

STRUCTURED_JSON:
{
  "name": "",
  "uses": "",
  "side_effects": "",
  "precautions": ""
}"""
                },
                {
                    "role": "user",
                    "content": f"Medicine: {query}"
                }
            ]
        )

        reply = response.choices[0].message.content

        # Parse output
        if "STRUCTURED_JSON:" in reply:
            parts = reply.split("STRUCTURED_JSON:")
            user_part = parts[0].replace("USER_OUTPUT:", "").strip()
            json_part = parts[1].strip()
        else:
            user_part = reply.strip()
            json_part = "{}"

        try:
            data = json.loads(json_part)
        except:
            data = {
                "name": query,
                "uses": user_part,
                "side_effects": "",
                "precautions": ""
            }

        # Save to database (Self-Learning)
        try:
            global df
            if query_clean not in df["name_clean"].values:
                df_new = pd.DataFrame([{
                    "name": data.get("name", query),
                    "uses": data.get("uses", user_part),
                    "side_effects": data.get("side_effects", ""),
                    "composition": "AI Generated",
                    "composition2": "",
                    "substitutes": ""
                }])
                df = pd.concat([df, df_new], ignore_index=True)
                df["name_clean"] = df["name"].str.lower().str.strip()
                df.to_csv(FILE_PATH, index=False)
        except Exception as save_error:
            print("Save error:", save_error)

        return {
            "results": [{
                "name": data.get("name", query),
                "price": "N/A",
                "composition": "AI Generated",
                "uses": user_part,
                "side_effects": data.get("side_effects", ""),
                "precautions": data.get("precautions", ""),
                "alternatives": [],
                "score": 1,
                "source": "ai"
            }]
        }

    except Exception as e:
        print("AI ERROR:", e)
        return {
            "results": [{
                "name": query,
                "price": "N/A",
                "composition": "AI Error",
                "uses": "Unable to fetch data",
                "side_effects": "",
                "precautions": "",
                "alternatives": [],
                "score": 0,
                "source": "error"
            }]
        }

# -------------------------------
# 📤 OCR UPLOAD API
# -------------------------------
from services.ocr_service import extract_text

# -------------------------------
# 📤 OCR UPLOAD API
# -------------------------------
from services.ocr_service import extract_text

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    
    # 🔥 FIX: Save to the OS Temp directory so VS Code Live Server doesn't refresh the browser!
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"temp_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(file_path)
    
    # Clean up file immediately after extracting text
    if os.path.exists(file_path):
        os.remove(file_path)

    words = str(text).split()
    keywords = []

    # Clean OCR words
    for word in words:
        word = word.strip()
        if len(word) < 4:
            continue
        if word.isdigit():
            continue
        if word.lower() in ["tablet", "tabletas", "mg", "ml", "capsule", "strip"]:
            continue
        keywords.append(word.lower())

    if not keywords:
        return {
            "source": "ocr_error",
            "message": "No medicine detected"
        }

    # Find the best match across all extracted keywords
    best_results = pd.DataFrame()
    best_score = 0
    query_clean = keywords[0]  # Default to first valid word

    for word in keywords:
        res = search_medicine(word)
        if not res.empty:
            top_score = res.iloc[0]["score"]
            if top_score > best_score:
                best_score = top_score
                best_results = res
                query_clean = word

    # 1. Try Database Result
    if not best_results.empty:
        row = best_results.iloc[0]
        return {
            "source": "database",
            "medicine": {
                "name": str(row["name"]) if pd.notna(row["name"]) else "",
                "price": str(row["price"]) if pd.notna(row.get("price")) else "N/A",
                "composition": f"{row.get('composition', '')}, {row.get('composition2', '')}".strip(", ") or "N/A",
                "uses": str(row.get("uses")) if pd.notna(row.get("uses")) else "N/A",
                "side_effects": str(row.get("side_effects")) if pd.notna(row.get("side_effects")) else "N/A",
                "precautions": "Consult your doctor for detailed precautions.",
                "alternatives": str(row.get("substitutes", "")).split(",")[:3] if row.get("substitutes") else []
            }
        }

    # 2. AI Fallback Result (If DB has no match)
    print(f"🚀 USING AI FALLBACK FOR OCR UPLOAD: {query_clean}")
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant.\n\nReturn ONLY valid JSON.\n\n{\n\"name\":\"\",\n\"uses\":\"\",\n\"side_effects\":\"\",\n\"composition\":\"\",\n\"precautions\":\"\"\n}"
                },
                {
                    "role": "user",
                    "content": f"Medicine: {query_clean}"
                }
            ]
        )

        reply = response.choices[0].message.content
        medicine_data = json.loads(reply)
    except Exception:
        medicine_data = {
            "name": query_clean,
            "uses": "Information unavailable.",
            "side_effects": "Information unavailable.",
            "composition": "AI Generated",
            "precautions": "Always consult a doctor."
        }

    # Save to database (Self-Learning for OCR flow)
    try:
        global df
        clean_name = medicine_data.get("name", query_clean).lower().strip()
        if clean_name not in df["name_clean"].values:
            df_new = pd.DataFrame([{
                "name": medicine_data.get("name", query_clean),
                "uses": medicine_data.get("uses", "N/A"),
                "side_effects": medicine_data.get("side_effects", "N/A"),
                "composition": medicine_data.get("composition", "AI Generated"),
                "composition2": "",
                "substitutes": ""
            }])
            df = pd.concat([df, df_new], ignore_index=True)
            df["name_clean"] = df["name"].str.lower().str.strip()
            df.to_csv(FILE_PATH, index=False)
    except Exception as save_error:
        print("OCR Save error:", save_error)

    return {
        "source": "ai",
        "medicine": {
            "name": medicine_data.get("name", query_clean),
            "price": "N/A",
            "composition": medicine_data.get("composition", "AI Generated"),
            "uses": medicine_data.get("uses", "N/A"),
            "side_effects": medicine_data.get("side_effects", "N/A"),
            "precautions": medicine_data.get("precautions", "Always consult a doctor."),
            "alternatives": []
        }
    }

# -------------------------------
# 💬 CHAT API
# -------------------------------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical assistant. Explain medicines in simple language. Always suggest consulting a doctor."
                },
                {
                    "role": "user",
                    "content": req.message
                }
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
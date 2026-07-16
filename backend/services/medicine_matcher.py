import pandas as pd
from difflib import SequenceMatcher

# Load once
df = pd.read_csv("FINAL_DATASET.csv")

df["name"] = df["name"].fillna("").astype(str)

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_best_match(ocr_text):

    best_score = 0
    best_row = None

    words = ocr_text.split()

    for _, row in df.iterrows():

        name = row["name"]

        score = max(similarity(word, name) for word in words)

        if score > best_score:
            best_score = score
            best_row = row

    if best_score > 0.65:

        return {
            "found": True,
            "medicine": {
                "name": best_row["name"],
                "price": best_row.get("price", "N/A"),
                "uses": best_row.get("uses", ""),
                "side_effects": best_row.get("side_effects", ""),
                "source": "database"
            }
        }

    return {
        "found": False,
        "ocr": ocr_text
    }
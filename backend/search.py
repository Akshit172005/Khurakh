import pandas as pd
import os
from difflib import SequenceMatcher

# -------------------------------
# LOAD DATA
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets")

df = pd.read_csv(os.path.join(DATASET_PATH, "FINAL_DATASET.csv"))

df["name"] = df["name"].astype(str)
df["name_clean"] = df["name"].str.lower().str.strip()

# -------------------------------
# SIMILARITY FUNCTION
# -------------------------------
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# -------------------------------
# SEARCH FUNCTION
# -------------------------------
def search_medicine(query):
    query = query.lower().strip()

    # Calculate similarity score
    df["score"] = df["name_clean"].apply(lambda x: similarity(query, x))

    # Get top 5 matches
    results = df.sort_values(by="score", ascending=False).head(5)

    # Filter weak matches
    results = results[results["score"] > 0.4]

    if results.empty:
        print("\n❌ No strong match found.")
        return

    print("\n" + "═" * 60)
    print("💊 DAWAICHECK — SEARCH RESULTS")
    print("═" * 60)

    # Show multiple results
    for i, (_, row) in enumerate(results.iterrows(), start=1):
        print(f"\n🔹 RESULT {i}")
        print("─" * 40)

        print(f"Name: {row['name'].title()}")
        print(f"Match Score: {round(row['score'], 2)}")
        print(f"Price: ₹{row.get('price', 'N/A')}")

        # Composition
        comp = f"{row.get('composition', '')}, {row.get('composition2', '')}".strip(", ")
        print(f"\n🧬 Composition:\n{comp if comp else 'Not Available'}")

        # Uses
        uses = row.get("uses", "Not Available")
        print(f"\n🩺 Uses:\n{uses}")

        # Side effects
        side = row.get("side_effects", "Not Available")
        print(f"\n⚠️ Side Effects:\n{side}")

        # Alternatives
        subs = str(row.get("substitutes", "")).split(",")
        print(f"\n🔁 Alternatives:\n{', '.join(subs[:3])}")

        print("─" * 40)

    print("\n" + "═" * 60 + "\n")


# -------------------------------
# MAIN LOOP
# -------------------------------
if __name__ == "__main__":
    print("\n💊 DawaiCheck Pro Search Engine\n")

    while True:
        query = input("🔍 Search medicine (or 'exit'): ")

        if query.lower() == "exit":
            print("\n👋 Goodbye!\n")
            break

        search_medicine(query)
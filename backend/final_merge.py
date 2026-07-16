import pandas as pd
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets")

# Load both datasets
df1 = pd.read_csv(os.path.join(DATASET_PATH, "clean_dataset1.csv"))
df2 = pd.read_csv(os.path.join(DATASET_PATH, "clean_medicine_dataset.csv"))

# -------------------------------
# CLEAN NAME FOR MATCHING
# -------------------------------
df1["name"] = df1["name"].str.lower().str.strip()
df2["name"] = df2["name"].str.lower().str.strip()

# -------------------------------
# MERGE
# -------------------------------
# AFTER MERGE

merged = pd.merge(df1, df2, on="name", how="left")

# Clean text
merged["uses"] = merged["uses"].str.replace("Treatment of ", "", regex=False)

# Remove duplicates
merged = merged.drop_duplicates(subset=["name"])

# Fill missing
merged.fillna("Not Available", inplace=True)

# Save
merged.to_csv(os.path.join(DATASET_PATH, "FINAL_DATASET.csv"), index=False)
print("✅ FINAL MERGE COMPLETED!")
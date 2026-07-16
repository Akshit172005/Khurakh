import pandas as pd
import os

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets")

# Load dataset
df = pd.read_csv(os.path.join(DATASET_PATH, "medicine_dataset.csv"))

# -------------------------------
# COMBINE USES
# -------------------------------
use_cols = [col for col in df.columns if col.startswith("use")]

df["uses"] = df[use_cols].apply(
    lambda x: ", ".join(x.dropna().astype(str)), axis=1
)

# -------------------------------
# COMBINE SIDE EFFECTS
# -------------------------------
side_cols = [col for col in df.columns if col.startswith("sideEffect")]

df["side_effects"] = df[side_cols].apply(
    lambda x: ", ".join(x.dropna().astype(str)), axis=1
)

# -------------------------------
# COMBINE SUBSTITUTES (🔥 IMPORTANT)
# -------------------------------
sub_cols = [col for col in df.columns if col.startswith("substitute")]

df["substitutes"] = df[sub_cols].apply(
    lambda x: ", ".join(x.dropna().astype(str)), axis=1
)

# -------------------------------
# KEEP IMPORTANT COLUMNS
# -------------------------------
final_df = df[[
    "name",
    "uses",
    "side_effects",
    "substitutes",
    "Therapeutic Class"
]]

# Rename column
final_df.rename(columns={
    "Therapeutic Class": "therapeutic_class"
}, inplace=True)

# Save cleaned dataset
final_df.to_csv(os.path.join(DATASET_PATH, "clean_medicine_dataset.csv"), index=False)

print("✅ New dataset cleaned successfully!")
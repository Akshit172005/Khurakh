import sqlite3
import pandas as pd
import os

# Get base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "..", "datasets")

# Connect to database
conn = sqlite3.connect(os.path.join(DATASET_PATH, "dawai.db"))

# SQL JOIN
query = """
SELECT 
    m.name,
    m.base_name,
    m.strength,
    m.form,
    m.price,
    m.manufacturer,
    m.composition,
    i.category,
    i.dosage_form,
    i.uses,
    i.classification
FROM medicines m
LEFT JOIN medicine_info i
ON m.base_name = i.name
"""

# Execute query
merged_df = pd.read_sql_query(query, conn)

# Save output
merged_df.to_csv(os.path.join(DATASET_PATH, "final_merged_dataset.csv"), index=False)

print("✅ Merge completed successfully!")

conn.close()
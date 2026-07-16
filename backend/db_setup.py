import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("../datasets/dawai.db")

# Load datasets
df1 = pd.read_csv("../datasets/clean_dataset1.csv")
df2 = pd.read_csv("../datasets/clean_dataset2.csv")

# Save to database
df1.to_sql("medicines", conn, if_exists="replace", index=False)
df2.to_sql("medicine_info", conn, if_exists="replace", index=False)

print("✅ Data loaded into SQLite successfully!")

conn.close()
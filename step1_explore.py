# step1_explore.py
print("=== STEP 1: EXPLORING THE DATA ===")
print()

# 1. First, let's see what files we have
import os

print("Files in folder:")
for file in os.listdir('.'):
    print(f"  - {file}")

print("\n" + "="*50)
print()

# 2. Look at crx.names to understand data
print("Reading crx.names file:")
with open('crx.names', 'r') as f:
    names_content = f.read()
    print(names_content[:500])  # First 500 characters

print("\n" + "="*50)
print()

# 3. Load the main data file
import pandas as pd

# The data has no headers, so header=None
df = pd.read_csv('crx.data', header=None)

print(f"Data loaded! Shape: {df.shape}")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\nFirst look at data:")
print(df.head())

print("\n" + "="*50)
print()

# 4. Check each column
print("Column types and sample values:")
for i in range(min(5, df.shape[1])):  # Check first 5 columns
    print(f"\nColumn {i}:")
    print(f"  First 5 values: {df[i].head().tolist()}")
    print(f"  Type: {df[i].dtype}")
    print(f"  Unique values: {df[i].unique()[:10]}")  # First 10 unique

print("\n" + "="*50)
print()

# 5. Look for the target column (approval)
print("Looking for approval column (+/-):")
for i in range(df.shape[1]):
    unique_vals = df[i].dropna().unique()
    if len(unique_vals) < 10:  # If few unique values
        if any('+' in str(val) or '-' in str(val) for val in unique_vals):
            print(f"  Column {i} might be approval: {unique_vals}")

print("\n" + "="*50)
print()

# 6. Basic statistics
print("Basic statistics for numeric columns:")
print(df.describe())
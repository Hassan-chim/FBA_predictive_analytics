# step2_clean.py
print("=== STEP 2: CLEANING THE DATA ===")
print()

import pandas as pd
import numpy as np

# Load data with '?' as missing values
df = pd.read_csv('crx.data', header=None, na_values='?')

print("Original data shape:", df.shape)
print()

# Give columns better names (based on typical credit dataset)
column_names = [
    'Gender', 'Age', 'Debt', 'Married', 'BankCustomer', 'EducationLevel',
    'Ethnicity', 'YearsEmployed', 'PriorDefault', 'Employed', 'CreditScore',
    'DriversLicense', 'Citizen', 'ZipCode', 'Income', 'ApprovalStatus'
]

df.columns = column_names

print("Columns renamed:")
for i, col in enumerate(df.columns):
    print(f"  {i:2d}. {col}")

print("\n" + "="*50)
print()

# Check for missing values
print("Missing values per column:")
missing = df.isnull().sum()
for col in df.columns:
    if missing[col] > 0:
        print(f"  {col:20s}: {missing[col]} missing ({missing[col]/len(df):.1%})")

print("\n" + "="*50)
print()

# Fix missing values
print("Fixing missing values...")

# For numeric columns, fill with median
numeric_cols = ['Age', 'Debt', 'YearsEmployed', 'CreditScore', 'Income']
for col in numeric_cols:
    if col in df.columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"  {col}: filled with median value {median_val}")

# For categorical columns, fill with mode (most frequent)
categorical_cols = ['Gender', 'Married', 'BankCustomer', 'EducationLevel', 
                    'Ethnicity', 'PriorDefault', 'Employed', 'DriversLicense',
                    'Citizen', 'ZipCode']

for col in categorical_cols:
    if col in df.columns:
        mode_val = df[col].mode()[0]  # Most frequent value
        df[col] = df[col].fillna(mode_val)
        print(f"  {col}: filled with most frequent value '{mode_val}'")

print("\n" + "="*50)
print()

# Convert ApprovalStatus from + and - to 1 and 0
df['ApprovalStatus'] = df['ApprovalStatus'].map({'+': 1, '-': 0})

print("ApprovalStatus converted:")
print("  + -> 1 (Approved)")
print("  - -> 0 (Rejected)")
print(f"\nApproval counts:")
print(df['ApprovalStatus'].value_counts())
print(f"\nApproval rate: {df['ApprovalStatus'].mean():.1%}")

print("\n" + "="*50)
print()

# Save cleaned data
df.to_csv('cleaned_credit_data.csv', index=False)
print("Cleaned data saved as 'cleaned_credit_data.csv'")
print("\nFirst 5 rows of cleaned data:")
print(df.head())
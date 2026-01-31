# step4_model.py
print("=== STEP 4: BUILDING PREDICTION MODEL ===")
print()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load cleaned data
df = pd.read_csv('cleaned_credit_data.csv')
print(f"Data loaded: {len(df)} records, {len(df.columns)} columns")

print("\n" + "="*50)
print()

# Prepare features (X) and target (y)
print("Preparing data for machine learning...")

# Separate target variable
y = df['ApprovalStatus']
X = df.drop('ApprovalStatus', axis=1)

print(f"Target (y) shape: {y.shape}")
print(f"Features (X) shape: {X.shape}")

print("\n" + "="*50)
print()

# Handle categorical variables (convert text to numbers)
print("Converting categorical variables...")

label_encoders = {}
categorical_cols = ['Gender', 'Married', 'BankCustomer', 'EducationLevel',
                    'Ethnicity', 'PriorDefault', 'Employed', 'DriversLicense',
                    'Citizen', 'ZipCode']

for col in categorical_cols:
    if col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        print(f"  Encoded {col}")

print("\n" + "="*50)
print()

# Split data into training and testing sets
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} samples")
print(f"Testing set: {len(X_test)} samples")
print(f"Training approval rate: {y_train.mean():.1%}")
print(f"Testing approval rate: {y_test.mean():.1%}")

print("\n" + "="*50)
print()

# Train a Random Forest model
print("Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,  # Number of trees
    max_depth=10,      # Maximum depth of trees
    random_state=42    # For reproducibility
)

model.fit(X_train, y_train)
print("Model trained successfully!")

print("\n" + "="*50)
print()

# Make predictions
print("Making predictions...")
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.2%}")

print("\n" + "="*50)
print()

# Detailed report
print("Detailed Classification Report:")
print(classification_report(y_test, y_pred, 
                           target_names=['Rejected', 'Approved']))

print("\n" + "="*50)
print()

# Confusion Matrix
print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"               Predicted")
print(f"               Rej  App")
print(f"Actual Rej:   {cm[0,0]:4d}  {cm[0,1]:4d}")
print(f"       App:   {cm[1,0]:4d}  {cm[1,1]:4d}")

print("\n" + "="*50)
print()

# Feature importance
print("Top 10 Most Important Features:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance.head(10))

print("\n" + "="*50)
print()

# Test with a new example
print("Testing with a new example...")
example = {
    'Gender': 'b',           # b = male, a = female
    'Age': 35,
    'Debt': 5.5,
    'Married': 'u',          # u = unmarried
    'BankCustomer': 'g',
    'EducationLevel': 'c',
    'Ethnicity': 'v',
    'YearsEmployed': 5,
    'PriorDefault': 'f',     # f = no prior default
    'Employed': 't',         # t = employed
    'CreditScore': 50,
    'DriversLicense': 'f',
    'Citizen': 'g',
    'ZipCode': 560,
    'Income': 50
}

# Convert example to DataFrame
example_df = pd.DataFrame([example])

# Encode categorical variables (using same encoders as before)
for col in categorical_cols:
    if col in example_df.columns:
        # Handle unseen labels
        try:
            example_df[col] = label_encoders[col].transform(example_df[col])
        except:
            # If label not seen before, use most common
            example_df[col] = 0

# Make sure columns are in same order
example_df = example_df[X.columns]

# Predict
prediction = model.predict(example_df)
probability = model.predict_proba(example_df)

print(f"\nExample applicant:")
for key, value in example.items():
    print(f"  {key}: {value}")

print(f"\nPrediction: {'APPROVED' if prediction[0] == 1 else 'REJECTED'}")
print(f"Confidence: {probability[0][prediction[0]]:.1%}")

print("\n" + "="*50)
print()

# Save the model
import joblib
joblib.dump(model, 'credit_approval_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("Model saved as 'credit_approval_model.pkl'")
print("Label encoders saved as 'label_encoders.pkl'")
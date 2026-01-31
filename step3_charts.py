# step3_charts.py
print("=== STEP 3: CREATING CHARTS ===")
print()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('cleaned_credit_data.csv')

print(f"Loaded {len(df)} records")
print()

# Set up the figure
plt.figure(figsize=(15, 10))

# Chart 1: Approval vs Rejection
plt.subplot(2, 3, 1)
approval_counts = df['ApprovalStatus'].value_counts()
colors = ['#ff6b6b', '#51cf66']  # Red for rejected, green for approved
bars = plt.bar(['Rejected (0)', 'Approved (1)'], approval_counts.values, color=colors)
plt.title('Credit Applications: Approved vs Rejected')
plt.ylabel('Number of Applications')

# Add counts on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{int(height)}', ha='center', va='bottom')

# Chart 2: Approval by Gender
plt.subplot(2, 3, 2)
approval_by_gender = df.groupby('Gender')['ApprovalStatus'].mean()
gender_bars = plt.bar(approval_by_gender.index, approval_by_gender.values * 100, 
                      color=['#ffd43b', '#339af0'])
plt.title('Approval Rate by Gender')
plt.ylabel('Approval Rate (%)')
plt.xlabel('Gender')

# Add percentages
for bar in gender_bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{height:.1f}%', ha='center', va='bottom')

# Chart 3: Age distribution
plt.subplot(2, 3, 3)
plt.hist(df['Age'], bins=30, color='#74c0fc', edgecolor='black', alpha=0.7)
plt.title('Age Distribution of Applicants')
plt.xlabel('Age')
plt.ylabel('Count')
plt.axvline(df['Age'].mean(), color='red', linestyle='--', 
            label=f'Mean: {df["Age"].mean():.1f}')
plt.legend()

# Chart 4: Income vs Approval
plt.subplot(2, 3, 4)
approved = df[df['ApprovalStatus'] == 1]
rejected = df[df['ApprovalStatus'] == 0]

plt.scatter(approved['Age'], approved['Income'], alpha=0.5, color='green', 
            label='Approved', s=30)
plt.scatter(rejected['Age'], rejected['Income'], alpha=0.5, color='red', 
            label='Rejected', s=30)
plt.title('Age vs Income (by Approval)')
plt.xlabel('Age')
plt.ylabel('Income')
plt.legend()

# Chart 5: Years Employed
plt.subplot(2, 3, 5)
employed_approved = df[df['ApprovalStatus'] == 1]['YearsEmployed']
employed_rejected = df[df['ApprovalStatus'] == 0]['YearsEmployed']

plt.boxplot([employed_approved, employed_rejected], 
            labels=['Approved', 'Rejected'])
plt.title('Years Employed (by Approval Status)')
plt.ylabel('Years')

# Chart 6: Debt distribution
plt.subplot(2, 3, 6)
debt_approved = df[df['ApprovalStatus'] == 1]['Debt']
debt_rejected = df[df['ApprovalStatus'] == 0]['Debt']

plt.hist(debt_approved, bins=20, alpha=0.5, color='green', label='Approved', density=True)
plt.hist(debt_rejected, bins=20, alpha=0.5, color='red', label='Rejected', density=True)
plt.title('Debt Distribution (by Approval)')
plt.xlabel('Debt')
plt.ylabel('Density')
plt.legend()

plt.tight_layout()
plt.savefig('credit_analysis_charts.png', dpi=100, bbox_inches='tight')
plt.show()

print("Charts saved as 'credit_analysis_charts.png'")
print("\n" + "="*50)
print()

# Show some statistics
print("Key Statistics:")
print(f"1. Total applications: {len(df)}")
print(f"2. Approval rate: {df['ApprovalStatus'].mean():.1%}")
print(f"3. Average age: {df['Age'].mean():.1f} years")
print(f"4. Average income: ${df['Income'].mean():,.0f}")
print(f"5. Average years employed: {df['YearsEmployed'].mean():.1f} years")
print(f"6. Average debt: ${df['Debt'].mean():,.0f}")
print()

# Approval rates by different factors
print("Approval Rates by Category:")
for col in ['Gender', 'Married', 'PriorDefault', 'Employed']:
    if col in df.columns:
        rates = df.groupby(col)['ApprovalStatus'].mean() * 100
        print(f"\n{col}:")
        for val, rate in rates.items():
            print(f"  {val}: {rate:.1f}%")
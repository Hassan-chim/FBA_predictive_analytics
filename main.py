# main.py
"""
Credit Approval Analysis - Complete Pipeline
Run all steps from data loading to model training
"""

def main():
    print("🚀 CREDIT APPROVAL ANALYSIS PIPELINE")
    print("="*50)
    
    # Step 1: Exploration
    import step1_explore
    # Step 2: Cleaning
    import step2_clean
    # Step 3: Visualization
    import step3_charts
    
    # Step 4: Modeling
    import step4_model

if __name__ == "__main__":
    main()
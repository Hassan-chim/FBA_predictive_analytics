# app.py - Simple web interface to test the model
import pandas as pd
import joblib
import streamlit as st

# Load the trained model
@st.cache_resource
def load_model():
    model = joblib.load('credit_approval_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    return model, label_encoders

def main():
    st.title("Credit Approval Predictor")
    st.write("Enter applicant details to predict credit approval")
    
    # Load model
    model, label_encoders = load_model()
    
    # Create input form
    with st.form("applicant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Gender", ['b', 'a'])
            age = st.number_input("Age", min_value=18, max_value=100, value=35)
            debt = st.number_input("Debt", min_value=0.0, value=5.5)
            married = st.selectbox("Marital Status", ['u', 'y'])
            bank_customer = st.selectbox("Bank Customer", ['g', 'p'])
            
        with col2:
            education = st.selectbox("Education Level", ['c', 'd', 'cc', 'i', 'j', 'k',
                                                       'm', 'r', 'q', 'w', 'x', 'e', 
                                                       'aa', 'ff'])
            ethnicity = st.selectbox("Ethnicity", ['v', 'h', 'bb', 'j', 'n', 'z', 
                                                  'dd', 'ff', 'o'])
            years_employed = st.number_input("Years Employed", min_value=0.0, max_value=50.0, value=5.0)
            prior_default = st.selectbox("Prior Default", ['f', 't'])
            employed = st.selectbox("Currently Employed", ['t', 'f'])
        
        income = st.number_input("Income", min_value=0, value=50)
        
        submitted = st.form_submit_button("Predict Approval")
    
    if submitted:
        # Create input data
        input_data = {
            'Gender': gender,
            'Age': age,
            'Debt': debt,
            'Married': married,
            'BankCustomer': bank_customer,
            'EducationLevel': education,
            'Ethnicity': ethnicity,
            'YearsEmployed': years_employed,
            'PriorDefault': prior_default,
            'Employed': employed,
            'CreditScore': 50,  # Default value
            'DriversLicense': 'f',  # Default
            'Citizen': 'g',  # Default
            'ZipCode': 560,  # Default
            'Income': income
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encode categorical variables
        categorical_cols = ['Gender', 'Married', 'BankCustomer', 'EducationLevel',
                          'Ethnicity', 'PriorDefault', 'Employed', 'DriversLicense',
                          'Citizen', 'ZipCode']
        
        for col in categorical_cols:
            if col in input_df.columns:
                try:
                    input_df[col] = label_encoders[col].transform(input_df[col])
                except:
                    input_df[col] = 0
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Display results
        st.subheader("Prediction Result")
        
        if prediction == 1:
            st.success(f"✅ **APPROVED** (Confidence: {probability[1]:.1%})")
        else:
            st.error(f"❌ **REJECTED** (Confidence: {probability[0]:.1%})")
        
        # Show feature importance
        st.subheader("Key Factors in Decision")
        
        # Get feature importance
        feature_importance = pd.DataFrame({
            'Feature': model.feature_names_in_,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        # Show top 5 factors
        top_factors = feature_importance.head(5)
        
        for idx, row in top_factors.iterrows():
            feature_name = row['Feature']
            importance = row['Importance']
            
            # Get actual value for this feature
            if feature_name in input_data:
                value = input_data[feature_name]
                st.write(f"- **{feature_name}**: {value} (Impact: {importance:.1%})")

if __name__ == "__main__":
    # Install streamlit first: pip install streamlit
    # Then run: streamlit run app.py
    main()
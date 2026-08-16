import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title="Tabular ML Predictor", page_icon="🤖", layout="wide")

st.title("🤖 Standard ML Classification (Tabular Features)")
st.markdown("This page uses a classic Machine Learning algorithm (**Random Forest**) trained on the Tabular Features of our dataset to predict a candidate's Job Category.")

# Load the model
@st.cache_resource
def load_ml_model():
    model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "tabular_rf_pipeline.pkl")
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_ml_model()

if model is None:
    st.error("Model not found! Please run `python scripts/train_tabular_ml.py` first.")
else:
    st.sidebar.success("Random Forest Model Loaded Successfully!")
    
    st.subheader("Manual Feature Input")
    st.markdown("Enter the extracted features of a candidate manually to see how the Random Forest classifies them.")
    
    with st.form("ml_prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_area("Extracted Skills (Comma separated)", placeholder="Python, SQL, AWS, React, Machine Learning")
            
        with col2:
            experience = st.text_area("Experience Snippet", placeholder="Worked as a Senior Developer for 5 years building scalable web applications...")
            
        submit = st.form_submit_button("Predict Job Category", type="primary")
        
    if submit:
        if not skills and not experience:
            st.warning("Please enter some skills or experience.")
        else:
            # Prepare the tabular feature (same logic as training)
            text_feature = f"{skills} {experience}"
            
            with st.spinner("Classifying with Random Forest..."):
                prediction = model.predict([text_feature])[0]
                probabilities = model.predict_proba([text_feature])[0]
                classes = model.classes_
                
                # Get top 3 probabilities
                prob_df = pd.DataFrame({"Category": classes, "Probability": probabilities})
                top_3 = prob_df.sort_values(by="Probability", ascending=False).head(3)
                
                st.success(f"🎯 **Predicted Category:** {prediction}")
                
                st.markdown("### Top 3 Probabilities")
                for _, row in top_3.iterrows():
                    st.write(f"- **{row['Category']}**: {round(row['Probability'] * 100, 2)}%")
                    st.progress(row['Probability'])

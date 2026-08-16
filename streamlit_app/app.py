import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import torch
from sentence_transformers import SentenceTransformer, util

# --- CONFIG ---
st.set_page_config(page_title="HR Job Matcher", page_icon="👔", layout="wide")

st.title("👔 HR Resume Matcher (Full 2,400+ Dataset)")
st.markdown("Enter a Job Description below to instantly find the best matching resumes from our **entire training dataset of 2,466 real resumes**.")

# --- LOAD DATA (Pre-computed Embeddings) ---
EMB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cv_embeddings.npy")
META_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cv_metadata.json")

@st.cache_data
def load_data():
    if not os.path.exists(EMB_PATH) or not os.path.exists(META_PATH):
        return None, None
        
    cv_embs = np.load(EMB_PATH)
    with open(META_PATH, 'r') as f:
        cv_meta = json.load(f)
        
    # Convert metadata to DataFrame for easy display
    df = pd.DataFrame(cv_meta)
    return cv_embs, df

cv_embs, df = load_data()

# --- LOAD AI MODEL ---
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

if df is None or df.empty:
    st.error("Dataset not found! Please ensure data/cv_embeddings.npy and data/cv_metadata.json exist.")
else:
    st.sidebar.header("Database Overview")
    st.sidebar.metric("Total Resumes in DB", len(df))
    
    # Show top categories
    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    st.sidebar.dataframe(category_counts, hide_index=True)
    
    jd = st.text_area("Paste the Job Description here:", height=200, placeholder="We are looking for a Senior Frontend Developer with React and TypeScript...")
    
    if st.button("Find Best Candidates", type="primary") and jd.strip():
        with st.spinner("AI is analyzing the Job Description and matching against 2,466 candidates..."):
            model = load_model()
            
            # Embed the Job Description
            jd_emb = model.encode(jd, convert_to_tensor=True)
            
            # Convert loaded numpy embeddings to tensor
            cv_embs_tensor = torch.tensor(cv_embs)
            
            # Compute cosine similarities
            cos_scores = util.cos_sim(jd_emb, cv_embs_tensor)[0].cpu().numpy()
            
            # Add scores to DataFrame
            df["Match Score (%)"] = [round(float(s) * 100, 1) for s in cos_scores]
            
            # Sort by score and take top 50
            results = df.sort_values("Match Score (%)", ascending=False).head(50).reset_index(drop=True)
            
            st.success("Matching complete! Here are the top candidates:")
            st.markdown("### Top Matches")
            
            # Display results
            display_cols = ["id", "category", "Match Score (%)", "skills_preview"]
            st.dataframe(
                results[display_cols].style.background_gradient(subset=['Match Score (%)'], cmap='Greens'),
                use_container_width=True,
                height=400
            )
            
            st.markdown("### Detailed View (Top 3 Candidates)")
            for i in range(3):
                candidate = results.iloc[i]
                with st.expander(f"🏅 #{i+1} | {candidate['id']} - {candidate['category']} (Score: {candidate['Match Score (%)']}%)", expanded=(i==0)):
                    st.write("**Extracted Skills:**")
                    st.info(candidate['skills_preview'])
                    st.write("**Experience Summary:**")
                    st.write(candidate['experience_preview'])

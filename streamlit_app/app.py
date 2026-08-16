import streamlit as st
import pandas as pd
import os
import torch
from sentence_transformers import SentenceTransformer, util

# --- CONFIG ---
st.set_page_config(page_title="HR Job Matcher", page_icon="👔", layout="wide")

st.title("👔 HR Resume Matcher")
st.markdown("Enter a Job Description below to instantly find the best matching resumes from our local database.")

# --- LOAD DATA ---
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "extracted_resumes.csv")

@st.cache_data
def load_data():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)

df = load_data()

# --- LOAD AI MODEL ---
@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

if df.empty:
    st.warning("No resumes found in the database. Please upload and extract resumes in the main app first.")
else:
    st.sidebar.header("Database Overview")
    st.sidebar.metric("Total Resumes", len(df))
    st.sidebar.dataframe(df["Category"].value_counts())
    
    jd = st.text_area("Paste the Job Description here:", height=200, placeholder="We are looking for a Senior Frontend Developer with React and TypeScript...")
    
    if st.button("Find Best Candidates", type="primary") and jd.strip():
        with st.spinner("AI is analyzing the Job Description and matching candidates..."):
            model = load_model()
            
            # Embed the Job Description
            jd_emb = model.encode(jd, convert_to_tensor=True)
            
            # Embed all Resume raw texts
            cv_embs = model.encode(df["RawText"].fillna("").tolist(), convert_to_tensor=True)
            
            # Compute cosine similarities
            cos_scores = util.cos_sim(jd_emb, cv_embs)[0].cpu().numpy()
            
            # Add scores to DataFrame
            df["Match Score (%)"] = [round(float(s) * 100, 1) for s in cos_scores]
            
            # Sort by score
            results = df.sort_values("Match Score (%)", ascending=False).reset_index(drop=True)
            
            st.success("Matching complete!")
            st.markdown("### Top Matches")
            
            # Display results
            display_cols = ["Filename", "Category", "Match Score (%)", "Skills"]
            st.dataframe(
                results[display_cols].style.background_gradient(subset=['Match Score (%)'], cmap='Greens'),
                use_container_width=True,
                height=400
            )
            
            st.markdown("### Detailed View (Top Candidate)")
            top_candidate = results.iloc[0]
            st.info(f"**{top_candidate['Filename']}** - {top_candidate['Category']} (Score: {top_candidate['Match Score (%)']}%)")
            st.write("**Extracted Skills:**", top_candidate['Skills'])
            st.write("**Experience:**", top_candidate['Experience'])

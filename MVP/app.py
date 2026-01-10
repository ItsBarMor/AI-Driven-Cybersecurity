import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

# --- Setup Logging ---
logging.basicConfig(filename='traffic_logs.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# --- Load Model ---
@st.cache_resource
def load_model():
    # Use the folder name where your optimized model is
    model_path = "../phishing_model_optimized" 
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model

try:
    tokenizer, model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

# --- Web Interface ---
st.title("🛡️ AI Phishing Detector (MVP)")
st.write("Enter email text below to scan for phishing attempts.")

email_text = st.text_area("Email Content:", height=150)

if st.button("Scan Email"):
    if email_text and model_loaded:
        # Inference
        inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, predicted_class = torch.max(probabilities, dim=1)
        
        # 1 = Phishing, 0 = Safe
        is_phishing = predicted_class.item() == 1 
        score = confidence.item() * 100

        if is_phishing:
            st.error(f"🚨 PHISHING DETECTED! (Confidence: {score:.2f}%)")
            logging.warning(f"ALERT: Phishing detected. Text: {email_text[:30]}... Score: {score}")
        else:
            st.success(f"✅ Email is Safe. (Confidence: {score:.2f}%)")
            logging.info(f"SAFE: Traffic processed. Text: {email_text[:30]}... Score: {score}")
    elif not model_loaded:
        st.error("Model not loaded. Please check your folder structure.")
    else:
        st.warning("Please enter text to analyze.")
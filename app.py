import streamlit as st
import pickle
import pdfplumber
import docx
import subprocess
import os
import re
import tempfile

# Load trained model
with open("svm_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# DOC → DOCX conversion (local using LibreOffice)
def convert_doc_to_docx(doc_path):
    subprocess.run([
        "soffice",
        "--headless",
        "--convert-to",
        "docx",
        doc_path,
        "--outdir",
        os.path.dirname(doc_path)
    ], check=True)
    return doc_path.replace(".doc", ".docx")

# Text extraction
def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return " ".join(p.text for p in doc.paragraphs)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z ]", " ", text)
    return text


st.title("Resume Classification System")
st.write("Upload Resume (PDF / DOCX / DOC)")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "doc"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    try:
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(temp_path)

        elif uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(temp_path)

        elif uploaded_file.name.endswith(".doc"):
            docx_path = convert_doc_to_docx(temp_path)
            text = extract_text_from_docx(docx_path)

        text = clean_text(text)

        if st.button("Predict Category"):
            prediction = model.predict([text])[0]
            st.success(f"Predicted Category: {prediction}")

    except Exception as e:
        st.error(f"Error: {e}")


import streamlit as st
import pickle
import pdfplumber
import docx

# Load model
with open("svm_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# Text extraction
def extract_text_from_pdf(path):
    try:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except:
        return ""

def extract_text_from_docx(path):
    try:
        doc = docx.Document(path)
        return " ".join(p.text for p in doc.paragraphs)
    except:
        return ""

st.title("Resume Classification System")
st.write("Upload a resume (PDF / DOCX)")

uploaded_file = st.file_uploader("Choose a resume", type=["pdf", "docx"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file.name)
    else:
        text = extract_text_from_docx(uploaded_file.name)

    if text.strip():
        prediction = model.predict([text])[0]
        st.success(f"Predicted Category: {prediction}")
    else:
        st.error("Could not extract text")

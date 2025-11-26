import streamlit as st
from groq import Groq
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

# Load user profile model
with open("cover_letter_model.txt", "r") as f:
    base_profile = f.read()

# Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📄 AI Cover Letter Generator (Free – Groq)")
st.write("Paste the job description and generate a tailored cover letter.")

# Inputs
job_description = st.text_area("Job Description", height=250)
tone = st.selectbox("Select tone:", ["Professional", "Friendly", "Confident", "Enthusiastic"])

if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Generating your cover letter..."):

        prompt = (
            "Write a 1-page professional cover letter.\n\n"
            "PERSONAL MODEL:\n"
            f"{base_profile}\n\n"
            "JOB DESCRIPTION:\n"
            f"{job_description}\n\n"
            f"Tone: {tone.lower()}\n"
            "Format: A business cover letter with clear paragraphs.\n"
        )

        # ✅ FINAL WORKING GROQ CALL
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )

        cover_letter = response.choices[0].message.content

        st.subheader("Generated Letter:")
        st.write(cover_letter)

        pdf_bytes = create_pdf(cover_letter)

        st.download_button(
            "⬇️ Download PDF",
            pdf_bytes,
            "cover_letter.pdf",
            "application/pdf",
        )


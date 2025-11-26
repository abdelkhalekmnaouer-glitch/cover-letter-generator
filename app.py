import streamlit as st
from groq import Groq
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

# Load user profile model
with open("cover_letter_model.txt", "r") as f:
    base_profile = f.read()

# Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📄 AI Cover Letter Generator")
st.write("Paste the job description and generate a tailored cover letter.")

# User Inputs
job_description = st.text_area("Job Description", height=250)
tone = st.selectbox("Select tone:", ["Professional", "Friendly", "Confident", "Enthusiastic"])

# Generate button
if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner("Generating..."):

            # SAFEST PROMPT FORMAT
            prompt = (
                "Write a 1-page professional cover letter.\n\n"
                "PERSONAL MODEL:\n"
                f"{base_profile}\n\n"
                "JOB DESCRIPTION:\n"
                f"{job_description}\n\n"
                f"Tone: {tone.lower()}\n"
                "Format: Business letter with clear paragraphs.\n"
            )

            # GROQ API CALL — USING UNIVERSALLY AVAILABLE FREE MODEL
            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[{"role": "user", "content": prompt}]
            )

            cover_letter = response.choices[0].message["content"]

            # Display result
            st.subheader("Generated Letter:")
            st.write(cover_letter)

            # Create PDF
            pdf_bytes = create_pdf(cover_letter)

            # Download button
            st.download_button(
                "⬇️ Download PDF",
                pdf_bytes,
                "cover_letter.pdf",
                "application/pdf",
            )

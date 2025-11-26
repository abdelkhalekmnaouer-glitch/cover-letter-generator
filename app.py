import streamlit as st
from groq import Groq
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Cover Letter Generator (Free)", layout="centered")

# Load user profile model
with open("cover_letter_model.txt", "r") as f:
    base_profile = f.read()

st.title("📄 Free AI Cover Letter Generator (Groq)")
st.write("Paste a job offer and generate a tailored cover letter using the free Groq API.")

# Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

job_description = st.text_area("Job Description", height=250, placeholder="Paste the job offer here...")

tone = st.selectbox(
    "Select the tone:",
    ["Professional", "Friendly", "Confident", "Enthusiastic"]
)

if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner("Generating your cover letter using LLaMA-3-70B (Free)..."):

            prompt = f"""
            Write a 1-page cover letter based on the user's profile and the job description.

            USER PERSONAL MODEL:
            {base_profile}

            JOB DESCRIPTION:
            {job_description}

            Requirements:
            - Tone: {tone.lower()}
            - Professional formatting
            - Clear structure
            - Tailored to job
            - Keep it concise and business-appropriate
            """

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )

            cover_letter = response.choices[0].message["content"]

            st.subheader("Generated Cover Letter:")
            st.write(cover_letter)

            # Generate PDF
            pdf_bytes = create_pdf(cover_letter)

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )



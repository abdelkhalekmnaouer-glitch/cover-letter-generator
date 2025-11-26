import streamlit as st
from openai import OpenAI
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

# Load your base model
with open("cover_letter_model.txt", "r") as f:
    base_profile = f.read()

st.title("📄 AI Cover Letter Generator")
st.write("Paste a job offer and automatically generate a personalized cover letter.")

# OpenAI client
client = OpenAI(api_key=st.secrets["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"])

# UI input
job_description = st.text_area("Job Description", height=250, placeholder="Paste the job offer here...")

tone = st.selectbox(
    "Choose tone:",
    ["Professional", "Friendly", "Confident", "Enthusiastic"]
)

if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner("AI is generating your personalized cover letter..."):

            prompt = f"""
            You are a professional cover letter writer.

            USER PERSONAL MODEL:
            {base_profile}

            JOB DESCRIPTION:
            {job_description}

            Write a 1-page cover letter in a {tone.lower()} tone.
            Tailor the letter to the job description while maintaining the user's identity and style.
            Format it as a real business letter with paragraphs and good structure.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
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


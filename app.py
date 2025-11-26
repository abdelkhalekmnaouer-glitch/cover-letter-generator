import streamlit as st
from groq import Groq
from utils.pdf_generator import create_pdf

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

# Load user profile model
with open("cover_letter_model.txt", "r") as f:
    base_profile = f.read()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📄 AI Cover Letter Generator")
st.write("Paste the job description and generate a tailored letter.")

job_description = st.text_area("Job Description", height=250)

tone = st.selectbox("Select tone:", ["Professional", "Friendly", "Confident", "Enthusiastic"])

if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner("Generating..."):

            prompt = f"""
            Write a 1-page cover letter based on:

            PERSONAL MODEL:
            {base_profile}

            JOB DESCRIPTION:
            {job_description}

            Tone: {tone.lower()}
            Format: Business letter.
            """

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )

            cover_letter = response.choices[0].message["content"]

            st.subheader("Generated Letter:")
            st.write(cover_letter)

            pdf_bytes = create_pdf(cover_letter)

            st.download_button(
                "⬇️ Download PDF",
                pdf_bytes,
                "cover_letter.pdf",
                "application/pdf",
            )

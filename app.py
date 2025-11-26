if st.button("Generate Cover Letter"):
    if not job_description:
        st.error("Please paste a job description.")
    else:
        with st.spinner("Generating your cover letter using LLaMA 3 (Groq)…"):

            # CREATE THE PROMPT — must come BEFORE the API call
            prompt = f"""
            Write a 1-page cover letter with the following guidelines:

            USER PERSONAL MODEL:
            {base_profile}

            JOB DESCRIPTION:
            {job_description}

            Tone: {tone.lower()}
            Format: Business letter, clear paragraphs, concise.
            """

            # CALL THE GROQ API — prompt must already exist
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            cover_letter = response.choices[0].message["content"]

            st.subheader("Generated Cover Letter:")
            st.write(cover_letter)

            pdf_bytes = create_pdf(cover_letter)

            st.download_button(
                label="⬇️ Download PDF",
                data=pdf_bytes,
                file_name="cover_letter.pdf",
                mime="application/pdf"
            )

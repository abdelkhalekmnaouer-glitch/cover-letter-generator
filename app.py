import streamlit as st
from groq import Groq
from utils.pdf_generator import create_pdf

# ------------------------------
# CONFIG
# ------------------------------

st.set_page_config(page_title="Générateur de Lettre de Motivation", layout="centered")

# Load personal model
with open("cover_letter_model.txt", "r", encoding="utf-8") as f:
    base_profile = f.read()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📄 Générateur de Lettre de Motivation – Format Ultra Fidèle")
st.write("Générez une lettre parfaitement formatée selon votre modèle PDF.")

# ------------------------------
# USER INPUTS
# ------------------------------

job_description = st.text_area("Description du poste :", height=250)
tone = st.selectbox("Ton de la lettre :", ["Professionnel", "Soutenu", "Convaincant"])

generate = st.button("Générer la lettre (PDF ultra fidèle)")

# ------------------------------
# GENERATION
# ------------------------------

if generate:
    if not job_description:
        st.error("Veuillez coller une offre d’emploi.")
        st.stop()

    with st.spinner("Génération de la lettre..."):

        # ------------------------------------------
        # Prompt STRUCTURÉ (obligatoire pour PDF)
        # ------------------------------------------
        prompt = f"""
Tu es un assistant expert en rédaction professionnelle. 
Tu dois générer une lettre de motivation STRICTEMENT dans le format suivant, avec BALISES.

Respecte absolument ce format :

@@coordonnees
[Nom Prénom]
[Adresse]
[Code Postal + Ville]
[Téléphone]
[Email]

@@objet
[Titre de l’objet]

@@p1
[Premier paragraphe]

@@p2
[Deuxième paragraphe]

@@p3
[Troisième paragraphe]

@@p4
[Quatrième paragraphe]

@@signature
[Phrase finale]

RÈGLES IMPORTANTES :
- N’AJOUTE AUCUN texte en dehors des balises.
- Aucune ligne vide inutile.
- AUCUN emoji.
- PAS de mise en forme Markdown.
- Chaque paragraphe doit être cohérent, professionnel, en lien avec l’offre.
- Le contenu doit être en français.

Voici le PROFIL du candidat :
{base_profile}

Voici l’OFFRE D'EMPLOI :
{job_description}

Génère maintenant la lettre en utilisant les balises ci-dessus.
"""

        # ------------------------------------------
        # GROQ CALL
        # ------------------------------------------
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.7
        )

        ai_text = response.choices[0].message.content

        st.subheader("Lettre générée (format balisé) :")
        st.code(ai_text)

        # ------------------------------------------
        # CREATE PDF ULTRA-FIDÈLE
        # ------------------------------------------
        try:
            pdf_bytes = create_pdf(ai_text)

            st.download_button(
                label="📥 Télécharger la lettre PDF",
                data=pdf_bytes,
                file_name="lettre_motivation.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error("Erreur lors de la génération du PDF :")
            st.error(str(e))

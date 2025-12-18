import streamlit as st
import google.generativeai as genai

# 1. Configuratie van de pagina
st.set_page_config(page_title="De Differentiatie Assistent", page_icon="🎓")

st.title("🎓 De Differentiatie Assistent (via Gemini)")
st.write("Speciaal voor basisschooldocenten. Maak in één keer oefenmateriaal op 3 niveaus.")

# 2. API Key ophalen uit Streamlit Secrets
# Zorg dat je in Streamlit Cloud je secret 'GEMINI_API_KEY' noemt
api_key = st.secrets["GEMINI_API_KEY"]

# Google Gemini instellen
genai.configure(api_key=api_key)

# 3. De Interface (hetzelfde als eerst)
col1, col2 = st.columns(2)

with col1:
    groep = st.selectbox("Voor welke groep?", 
                         ["Groep 3", "Groep 4", "Groep 5", "Groep 6", "Groep 7", "Groep 8"])

with col2:
    vakgebied = st.selectbox("Vakgebied", 
                             ["Taal", "Spelling", "Begrijpend Lezen", "Rekenen", "Wereldoriëntatie"])

bronmateriaal = st.text_area("Plak hier de tekst, de som of het lesdoel:", height=150, 
                             placeholder="Bijv: Een tekst over fotosynthese OF De tafels van 7 oefenen.")

output_type = st.radio("Wat wil je genereren?", 
                       ["Uitlegkaart (Instructie)", "Oefenvragen (Open vragen)", "Meerkeuzevragen"])

# 4. De Knop en de AI-Magie
if st.button("🚀 Genereer Differentiatie"):
    if not bronmateriaal:
        st.warning("Vul eerst wat bronmateriaal in!")
    else:
        with st.spinner('Gemini is aan het denken...'):
            try:
                # We gebruiken hier het 'flash' model, dat is snel en goedkoop/gratis
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Je bent een onderwijsexpert voor het Nederlandse basisonderwijs.
                Ik wil differentiatie materiaal voor {groep}, vakgebied: {vakgebied}.
                
                Bronmateriaal/Onderwerp: {bronmateriaal}
                Gewenste outputvorm: {output_type}
                
                Maak drie varianten:
                1. 1-STER (Basis/Ondersteuning): Eenvoudige taal, kortere zinnen, meer tussenstappen, visuele suggesties.
                2. 2-STERREN (Gemiddeld): Past precies bij het niveau van {groep}.
                3. 3-STERREN (Verdieping/Plus): Uitdagend, doet een beroep op inzicht.
                
                Geef het antwoord in mooie Markdown opmaak met duidelijke koppen (###).
                """

                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                st.success("Klaar!")
                
            except Exception as e:
                st.error(f"Er ging iets mis: {e}")

st.markdown("---")
st.caption("Gemaakt met Google Gemini")

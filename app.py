import streamlit as st
from openai import OpenAI

# 1. Configuratie van de pagina
st.set_page_config(page_title="De Differentiatie Assistent", page_icon="🎓")

# Titel en intro
st.title("🎓 De Differentiatie Assistent")
st.write("Speciaal voor basisschooldocenten. Maak in één keer oefenmateriaal op 3 niveaus.")

# 2. API Key ophalen (veilig via secrets)
# Zorg dat je dit in Streamlit Cloud instelt bij 'Secrets'
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# 3. De Invoervelden (De interface)
col1, col2 = st.columns(2)

with col1:
    groep = st.selectbox("Voor welke groep?", 
                         ["Groep 3", "Groep 4", "Groep 5", "Groep 6", "Groep 7", "Groep 8"])

with col2:
    vakgebied = st.selectbox("Vakgebied", 
                             ["Taal", "Spelling", "Begrijpend Lezen", "Rekenen", "Wereldoriëntatie"])

# Tekstveld voor de input
bronmateriaal = st.text_area("Plak hier de tekst, de som of het lesdoel:", height=150, 
                             placeholder="Bijv: Een tekst over fotosynthese OF De tafels van 7 oefenen.")

# Keuze wat voor output ze willen
output_type = st.radio("Wat wil je genereren?", 
                       ["Uitlegkaart (Instructie)", "Oefenvragen (Open vragen)", "Meerkeuzevragen"])

# 4. De Knop en de AI-Magie
if st.button("🚀 Genereer Differentiatie"):
    if not bronmateriaal:
        st.warning("Vul eerst wat bronmateriaal in!")
    else:
        with st.spinner('De AI is hard aan het nadenken... even geduld...'):
            
            # De Prompt (Het brein van de tool)
            prompt = f"""
            Je bent een onderwijsexpert voor het Nederlandse basisonderwijs.
            Ik wil differentiatie materiaal voor {groep}, vakgebied: {vakgebied}.
            
            Bronmateriaal/Onderwerp: {bronmateriaal}
            Gewenste outputvorm: {output_type}
            
            Maak drie varianten:
            1. 1-STER (Basis/Ondersteuning): Eenvoudige taal, kortere zinnen, meer tussenstappen, visuele suggesties. Focus op herhalen/begrijpen.
            2. 2-STERREN (Gemiddeld): Past precies bij het niveau van {groep}. Focus op toepassen.
            3. 3-STERREN (Verdieping/Plus): Uitdagend, doet een beroep op inzicht, analyseren of verbanden leggen. Geen "meer werk", maar "ander werk".
            
            Geef het antwoord in mooie Markdown opmaak. Gebruik duidelijke koppen (###).
            Zorg dat de toon bemoedigend is voor de leerling.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o", # Of gpt-3.5-turbo voor goedkoper/sneller
                    messages=[
                        {"role": "system", "content": "Je bent een behulpzame assistent voor leerkrachten."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                # Resultaat tonen
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                st.success("Klaar! Je kunt dit kopiëren naar Word of PowerPoint.")
                
            except Exception as e:
                st.error(f"Er ging iets mis: {e}")

# Footer
st.markdown("---")
st.caption("Gemaakt voor de training 'Lesvoorbereiden met AI'")
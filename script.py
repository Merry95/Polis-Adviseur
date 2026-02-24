import streamlit as st

# Configure page
st.set_page_config(page_title="Polis-Adviseur", page_icon="🛡️")

# Title
st.title("Welkom bij GlobalSecure Polis-Adviseur")

# Introduction text
st.write("""
Fijn dat je er bent.

Met deze tool helpen we je om inzicht te krijgen in welke verzekeringen 
passen bij jouw persoonlijke situatie.

We stellen een aantal korte vragen over je woonsituatie, gezinssamenstelling 
en bezittingen. Op basis daarvan ontvang je een overzicht van:

- Essentiële verzekeringen
- Aanbevolen verzekeringen
- Optionele verzekeringen

Dit is een transparant en vrijblijvend advies.
""")

st.info("⏱️ Het invullen duurt ongeveer 3 minuten.")

# ----------------------
# Algemene gegevens
# ----------------------

st.subheader("Algemene gegevens")

naam = st.text_input("Wat is uw naam?")
#leeftijd = st.number_input("Wat is uw leeftijd?", min_value=18, max_value=100, step=1)
email = st.text_input("Wat is uw e-mailadres?")
woonSituatie = st.selectbox("Wat is uw woonsituatie ?", ["Huurwoning", "Koopwoning", "inwonend"])
werkSituatie = st.selectbox("Wat is uw werksituatie?", ["In loondienst", "zzp", "Werkloos"])
gezinssituatie = st.selectbox("Wat is uw gezinssituatie ?", ["Alleen", "samenwonend", "kinderen","huisdieren"])
spaarGeld = st.selectbox("Heeft u meer dan 25 000 euro aan spaargeld?", ["nee", "ja"])
if spaarGeld == "ja":
    spaarGeldGebruiken = st.selectbox("bent u bereid om dat uit te geven aan ongevallen?", ["ja", "nee"])



# ----------------------
# Start knop
# ----------------------

if st.button("Start advies"):
    if naam and email and woonSituatie and gezinssituatie and werkSituatie and spaarGeld:
        # Opslaan in session state
        st.session_state.naam = naam
        #st.session_state.leeftijd = leeftijd
        st.session_state.email = email
        st.session_state.woonSituatie = woonSituatie
        st.session_state.gezinssituatie = gezinssituatie
        st.session_state.werkSituatie = werkSituatie
        st.session_state.spaarGeld = spaarGeld
        if spaarGeld == "Ja":
            st.session_state.spaarGeldGebruiken = spaarGeldGebruiken


        st.switch_page("pages/main_flow.py")
    else:

        st.warning("Vul alle velden in.")

import streamlit as st
import time
import random

from script import woonSituatie

st.set_page_config(page_title="Wonen & Bezittingen Chatbot")
st.title("🏠 Wonen & Bezittingen Chatbot")

# ----------------------------
# Session state init
# ----------------------------

if "choices" not in st.session_state:
    st.session_state.choices = {}  # dictionary voor alle antwoorden

if "messages_wb" not in st.session_state:
    st.session_state.messages_wb = []

if "step_wb" not in st.session_state:
    st.session_state.step_wb = 1



# ----------------------------
# Typing functie
# ----------------------------
def bot_message(text, min_delay=0.5, max_delay=1.5):
    typing_placeholder = st.empty()
    with typing_placeholder.container():
        with st.chat_message("assistant"):
            st.markdown("...")
            time.sleep(random.uniform(min_delay, max_delay))
    typing_placeholder.empty()
    st.session_state.messages_wb.append({"role": "assistant", "content": text})

# ----------------------------
# Toon chatgeschiedenis
# ----------------------------
for msg in st.session_state.messages_wb:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# Startbericht
# ----------------------------
if st.session_state.step_wb == 1 and len(st.session_state.messages_wb) == 0:
    bot_message("Hallo! 👋 Laten we beginnen met je inboedel. Hoeveel euro is je inboedel waard?")
    st.session_state.step_wb = 2
    st.rerun()



elif st.session_state.step_wb == 5:
    bot_message("Neemt u deel aan risicovolle activiteiten? (bijvoorbeeld extreme sporten) Antwoord met: ja / nee")
    st.session_state.step_wb = 6
    st.rerun()


elif st.session_state.step_wb == 7:

    woonSituatie = st.session_state.get("woonSituatie")

    if woonSituatie == "Koopwoning":
        bot_message("Woningverzekering: Essentieel bij koopwoning.")
    else:
        bot_message("Woningverzekering: Optioneel bij huurwoning.")

    st.session_state.step_wb = 100  # echte eindstatus
    st.rerun()




# ----------------------------
# User input
# ----------------------------
user_input = st.chat_input("Typ hier je antwoord...")

if user_input:

    # user bericht opslaan
    st.session_state.messages_wb.append(
        {"role": "user", "content": user_input}
    )

    antwoord = user_input.lower().strip()

    # ----------------------------
    # STAP 2 → Inboedel verwerken
    # ----------------------------
    if st.session_state.step_wb == 2:

        try:
            cleaned = (
                user_input.replace("€", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", "")
            )
            waarde = int(cleaned)

            st.session_state.choices["inboedel_waarde"] = waarde

            if waarde <= 500:
                type_inboedel = "geen inboedelverzekering"
            elif waarde <= 5000:
                type_inboedel = "optionele inboedelverzekering"
            elif waarde <= 10000:
                type_inboedel = "aanbevolen inboedelverzekering"
            else:
                type_inboedel = "essentiële inboedelverzekering"

            st.session_state.choices["type_inboedel"] = type_inboedel
            woonSituatie = st.session_state.get("woonSituatie")
            bot_message(
                f"👍 Dank je! Je inboedel wordt geschat op €{waarde:,}. "
                f"Adviescategorie: {type_inboedel}.{woonSituatie}"
            )

            # 👉 NU GLAS-VRAAG
            if woonSituatie == "Koopwoning":
                bot_message(
                    "Heeft u veel of speciaal glas (bijvoorbeeld een serre of glas-in-lood)? Antwoord met: ja / nee"
                )
                st.session_state.step_wb = 3
            else:
                bot_message(
                    "Wat voor type woning heeft u? appartement / eensgezinswoning / overig"
                )
                st.session_state.step_wb = 4


        except ValueError:
            bot_message("⚠️ Voer alstublieft een geldig getal in, bijvoorbeeld 25000.")

        st.rerun()

    # ----------------------------
    # STAP 3 → Glas verwerken
    # ----------------------------

    elif st.session_state.step_wb == 3:

        if antwoord in ["ja", "nee"]:

            st.session_state.choices["speciaal_glas"] = antwoord

            if antwoord == "ja":
                glas_verzekering= "essentiële glasverzekering"
                bot_message("👍 We adviseren een essentiële glasverzekering.")


            st.session_state.step_wb = 5  # einde subflow

        else:
            bot_message("Kies alstublieft: ja / nee")

        st.rerun()



### uitleg hier
    elif st.session_state.step_wb == 4:

        if antwoord in ["appartement", "eensgezinswoning", "overig"]:

            if antwoord == "appartement":
                glas_verzekering = "optionele glasverzekering"
            elif antwoord == "eensgezinswoning":
                glas_verzekering = "aanbevolen glasverzekering"
            else:
                glas_verzekering = "geen glasverzekering nodig"

            st.session_state.choices["glas_verzekering"] = glas_verzekering

            bot_message(f"Advies: {glas_verzekering}")

            st.session_state.step_wb = 5

        else:
            bot_message("Kies: appartement / eensgezinswoning / overig")

        st.rerun()







    elif st.session_state.step_wb == 6:

        if antwoord in ["ja", "nee"]:

            st.session_state.choices["risicovolle_activiteiten"] = antwoord

            if antwoord == "ja":
                advies = "Essentiële aansprakelijkheidsverzekering"
                bot_message("⚠️ Advies: Essentiële aansprakelijkheidsverzekering.")
            else:
                advies = (
                    "Aansprakelijkheidsverzekering:\n\n"
                    "Essentieel: kinderen en/of dieren\n\n"
                    "Aanbevolen: samenwonend\n\n"
                    "Optioneel: alleenstaand"
                )
                bot_message(advies)

            # Opslaan
            st.session_state.choices["aansprakelijkheidverzekering"] = advies

            st.session_state.step_wb = 7  # Ga naar volgende stap

        else:
            bot_message("Antwoord met ja of nee.")

        st.rerun()


    elif st.session_state.step_wb == 7:

        woonSituatie = st.session_state.get("woonSituatie")

        if woonSituatie == "Koopwoning":
            bot_message("Woningverzekering: Essentieel bij koopwoning.")
        else:
            bot_message("Woningverzekering: Optioneel bij huurwoning.")

        st.session_state.step_wb = 100  # echte eindstatus
        st.rerun()

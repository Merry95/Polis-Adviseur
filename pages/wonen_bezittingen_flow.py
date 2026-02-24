import streamlit as st
import time
import random

st.set_page_config(page_title="Wonen & Bezittingen Chatbot")
st.title("🏠 Wonen & Bezittingen Chatbot")

# ----------------------------
# SESSION STATE INIT
# ----------------------------

def init_session():
    if "choices" not in st.session_state:
        st.session_state.choices = {}

    if "messages_wb" not in st.session_state:
        st.session_state.messages_wb = []

    if "step_wb" not in st.session_state:
        st.session_state.step_wb = 1


# ----------------------------
# TYPING FUNCTIE
# ----------------------------

def bot_message(text, min_delay=0.5, max_delay=1.5):
    typing_placeholder = st.empty()
    with typing_placeholder.container():
        with st.chat_message("assistant"):
            st.markdown("...")
            time.sleep(random.uniform(min_delay, max_delay))
    typing_placeholder.empty()

    st.session_state.messages_wb.append(
        {"role": "assistant", "content": text}
    )


def show_chat():
    for msg in st.session_state.messages_wb:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


# ----------------------------
# STAP 1 – START
# ----------------------------

def start_message():
    bot_message("Hallo! 👋 Laten we beginnen met je inboedel. Hoeveel euro is je inboedel waard?")
    st.session_state.step_wb = 2


# ----------------------------
# STAP 2 – INBOEDEL
# ----------------------------

def handle_inboedel(user_input):

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
            f"👍 Dank je! Je inboedel wordt geschat op €{waarde:,}."
        )

        if woonSituatie == "Koopwoning":

            st.session_state.choices["opstalverzekering"] = "essentieel"

            bot_message(
                "Goed, dan gaan we nu kijken naar uw glasverzekering 👇\n\n"
                "U heeft aangegeven dat u een koopwoning heeft. Daarom bekijken we of een glasverzekering voor u nodig is.\n\n"
                "Heeft u veel of speciaal glas (bijvoorbeeld een serre of glas-in-lood)? Antwoord alstublieft met: ja / nee."
            )

            st.session_state.step_wb = 3

        else:

            st.session_state.choices["opstalverzekering"] = "optioneel"

            bot_message(
                "Goed, dan gaan we nu kijken naar uw glasverzekering 👇\n\n"
                "U heeft aangegeven dat u geen koopwoning heeft. Daarom willen we nog even uw type woning controleren in verband met de glasverzekering. \n\n"
                "Wat voor type woning heeft u? appartement / eensgezinswoning / overig"
            )

            st.session_state.step_wb = 4

    except ValueError:
        bot_message("⚠️ Voer alstublieft een geldig getal in, bijvoorbeeld 25000.")


# ----------------------------
# STAP 3 – GLAS KOOP
# ----------------------------

def handle_glas_koop(antwoord):

    if antwoord in ["ja", "nee"]:

        if antwoord == "ja":
            glas_verzekering = "essentiële glasverzekering"
        else:
            glas_verzekering = "geen aanvullende glasverzekering nodig"

        st.session_state.choices["glas_verzekering"] = glas_verzekering
        st.session_state.step_wb = 5

    else:
        bot_message("Kies alstublieft: ja / nee")


# ----------------------------
# STAP 4 – GLAS HUUR
# ----------------------------

def handle_glas_huur(antwoord):

    if antwoord in ["appartement", "eensgezinswoning", "overig"]:

        if antwoord == "appartement":
            glas_verzekering = "optionele glasverzekering"
        elif antwoord == "eensgezinswoning":
            glas_verzekering = "aanbevolen glasverzekering"
        else:
            glas_verzekering = "geen glasverzekering nodig"

        st.session_state.choices["glas_verzekering"] = glas_verzekering
        st.session_state.step_wb = 5

    else:
        bot_message("Kies: appartement / eensgezinswoning / overig")


# ----------------------------
# STAP 5 – AANSPRAKELIJKHEID VRAAG
# ----------------------------

def ask_aansprakelijkheid():
    bot_message(
        "De glasverzekering is afgerond ✅. We gaan nu verder met de aansprakelijkheidsverzekering.\n\n"
        "Heeft u een aansprakelijkheidsverzekering? Antwoord met: ja / nee."
    )
    st.session_state.step_wb = 6


# ----------------------------
# STAP 6 – AANSPRAKELIJKHEID
# ----------------------------

def handle_aansprakelijkheid(antwoord):

    if antwoord in ["ja", "nee"]:

        if antwoord == "ja":
            advies = "U heeft al een aansprakelijkheidsverzekering."
            st.session_state.choices["aansprakelijkheidverzekering"] = advies
            bot_message("Goed om te horen dat u verzekerd bent ✅")
            st.session_state.step_wb = 7
            return

        else:
            bot_message(
                "Kunt u bij een grote schadeclaim (bijvoorbeeld €50.000) "
                "dit bedrag zelf betalen? Antwoord met: ja / nee."
            )
            st.session_state.step_wb = 8
            return

    else:
        bot_message("Antwoord met ja of nee.")


# ----------------------------
# STAP 8 – SCHADEVRAAG
# ----------------------------

def handle_schadevraag(antwoord):

    if antwoord in ["ja", "nee"]:

        if antwoord == "ja":
            advies = "Aansprakelijkheidsverzekering: optioneel."
        else:
            advies = "Aansprakelijkheidsverzekering: essentieel."

        st.session_state.choices["aansprakelijkheidverzekering"] = advies
        st.session_state.step_wb = 7

    else:
        bot_message("Antwoord met ja of nee.")


# ----------------------------
# STAP 7 – ALGEMEEN ADVIES + NIEUWE VRAAG
# ----------------------------

def show_algemeen_advies():

    keuzes = st.session_state.choices
    advies_lijst = []

    if "type_inboedel" in keuzes:
        advies_lijst.append(f"Inboedelverzekering: {keuzes['type_inboedel']}")
    if "glas_verzekering" in keuzes:
        advies_lijst.append(f"Glasverzekering: {keuzes['glas_verzekering']}")
    if "aansprakelijkheidverzekering" in keuzes:
        advies_lijst.append(f"Aansprakelijkheidsverzekering: {keuzes['aansprakelijkheidverzekering']}")
    if "woonSituatie" in st.session_state:
        if st.session_state.woonSituatie == "Koopwoning":
            advies_lijst.append("Woningverzekering: Essentieel")
        else:
            advies_lijst.append("Woningverzekering: Optioneel")

    algemeen_advies = "✅ Algemeen advies gebaseerd op uw antwoorden:\n\n" + "\n".join(advies_lijst)
    bot_message(algemeen_advies)

    # Nieuwe vraag
    bot_message("Heeft u Persoon & Gezin verzekeringen?", 1.2, 2)

    st.session_state.step_wb = 11


# ----------------------------
# STAP 11 – PERSOON & GEZIN
# ----------------------------

def handle_persoon_gezin(antwoord):

    if antwoord in ["ja", "nee"]:

        if antwoord == "ja":
            bot_message("Dank u voor uw antwoord! 😊")
            st.session_state.step_wb = 999

        else:
            st.switch_page("pages/personen_gezin_flow.py")

    else:
        bot_message("Antwoord met ja of nee.")


# ----------------------------
# MAIN FLOW
# ----------------------------

init_session()
show_chat()

if st.session_state.step_wb == 1 and len(st.session_state.messages_wb) == 0:
    start_message()
    st.rerun()

if st.session_state.step_wb == 5:
    ask_aansprakelijkheid()
    st.rerun()

if st.session_state.step_wb == 7:
    show_algemeen_advies()
    st.rerun()

user_input = st.chat_input("Typ hier je antwoord...")

if user_input:

    st.session_state.messages_wb.append(
        {"role": "user", "content": user_input}
    )

    antwoord = user_input.lower().strip()

    if st.session_state.step_wb == 2:
        handle_inboedel(user_input)

    elif st.session_state.step_wb == 3:
        handle_glas_koop(antwoord)

    elif st.session_state.step_wb == 4:
        handle_glas_huur(antwoord)

    elif st.session_state.step_wb == 6:
        handle_aansprakelijkheid(antwoord)

    elif st.session_state.step_wb == 8:
        handle_schadevraag(antwoord)

    elif st.session_state.step_wb == 11:
        handle_persoon_gezin(antwoord)

    st.rerun()
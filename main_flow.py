import streamlit as st
import time
import random

st.set_page_config(page_title="Verzekering Chatbot")
st.title("🤖 Verzekering Advies Chatbot")




# ----------------------------
# SESSION STATE INITIALISATIE
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 1


# ----------------------------
# RESET KNOP (SIDEBAR)
# ----------------------------

with st.sidebar:
    if st.button("🔄 Nieuwe adviesronde"):
        st.session_state.messages = []
        st.session_state.step = 1
        st.rerun()


# ----------------------------
# CHAT HISTORY TONEN
# ----------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ----------------------------
# FUNCTIE VOOR BOT BERICHT MET TYPING INDICATOR
# ----------------------------

def bot_message(text, min_delay=0.001, max_delay=0.005):
    # Typing placeholder
    typing_placeholder = st.empty()

    with typing_placeholder.container():
        with st.chat_message("assistant"):
            st.markdown("...")
            time.sleep(random.uniform(min_delay, max_delay))

    # Typing indicator verwijderen
    typing_placeholder.empty()

    # Echte bericht opslaan
    st.session_state.messages.append(
        {"role": "assistant", "content": text}
    )


# ----------------------------
# STARTBERICHT (ALLEEN 1 KEER)
# ----------------------------

if st.session_state.step == 1 and len(st.session_state.messages) == 0:
    bot_message(
        "Welkom 👋"
        "We gaan beginnen met enkele vragen. U kunt antwoorden met: ja / nee. \n\n "
        "Heeft u wonen & bezittingen verzekeringen?\n"
    )
    st.session_state.step = 2
    st.rerun()


# ----------------------------
# USER INPUT
# ----------------------------

user_input = st.chat_input("Typ hier uw antwoord...")

if user_input:

    # User bericht toevoegen
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    antwoord = user_input.lower().strip()

    # ----------------------------
    # FLOW LOGICA
    # ----------------------------

    if st.session_state.step == 2:

        if antwoord == "nee":
            bot_message("We starten nu de Wonen & Bezittingen flow.", 1.5, 3)
            st.session_state.step = 99
            st.switch_page("pages/wonen_bezittingen_flow.py")

        elif antwoord == "ja":
            bot_message("Heeft u Persoon & Gezin verzekeringen?", 1.2, 2)
            st.session_state.step = 3

        else:
            bot_message("Kies alstublieft: nee / ja", 0.5, 1)

    elif st.session_state.step == 3:

        if antwoord == "nee":
            bot_message("We starten nu de Persoon & Gezin flow.", 1.5, 3)
            st.session_state.step = 99
            st.switch_page("pages/personen_gezin_flow.py")

        elif antwoord == "ja":
            bot_message("Heeft u Mobiliteit & Reizen verzekeringen?", 1.2, 2)
            st.session_state.step = 4

        else:
            bot_message("Kies alstublieft: nee / ja", 0.5, 1)

    elif st.session_state.step == 4:

        if antwoord == "nee":
            bot_message("We starten nu de Mobiliteit & Reizen flow.", 1.5, 3)
            st.switch_page("pages/Mobiliteit_Reizen_flow.py")
            st.session_state.step = 99

        elif antwoord == "ja":
            bot_message("Heeft u Inkomen & Toekomst verzekeringen?", 1.2, 2)
            st.session_state.step = 5

        else:
            bot_message("Kies alstublieft: nee / ja", 0.5, 1)

    elif st.session_state.step == 5:

        if antwoord == "nee":
            bot_message("We starten nu de Inkomen & Toekomst flow.", 1.5, 3)
            st.switch_page("pages/Inkomen_Toekomst_flow.py")

        elif antwoord == "ja":
            bot_message("Alles is verzekerd ✅ U krijgt een totaaladvies.", 1.5, 2.5)

        else:
            bot_message("Kies alstublieft: nee / ja", 0.5, 1)

        st.session_state.step = 99

    st.rerun()

import streamlit as st
import time
import random

st.set_page_config(page_title="Personen & Gezin Chatbot")
st.title("👨‍👩‍👧 Personen & Gezin Chatbot")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "choices" not in st.session_state:
    st.session_state.choices = {}

if "messages_pg" not in st.session_state:
    st.session_state.messages_pg = []

if "step_pg" not in st.session_state:
    st.session_state.step_pg = 1

if "laatste_antwoord" not in st.session_state:
    st.session_state.laatste_antwoord = ""

# ----------------------------
# BOT FUNCTIE
# ----------------------------
def bot_message(text, min_delay=0.3, max_delay=0.8):
    placeholder = st.empty()
    with placeholder.container():
        with st.chat_message("assistant"):
            st.markdown("...")
            time.sleep(random.uniform(min_delay, max_delay))
    placeholder.empty()
    st.session_state.messages_pg.append(
        {"role": "assistant", "content": text}
    )

# ----------------------------
# TOON CHATGESCHIEDENIS
# ----------------------------
for msg in st.session_state.messages_pg:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# AUTOMATISCHE VRAGEN / FLOW
# ----------------------------

# STAP 1: Extra zorg vraag
if st.session_state.step_pg == 1:
    bot_message(
        "Verwacht u het komende jaar extra zorg? "
        "(bijvoorbeeld bril of gezinsuitbreiding) (ja / nee)"
    )
    st.session_state.step_pg = 2
    st.rerun()

# ----------------------------
# USER INPUT
# ----------------------------
user_input = st.chat_input("Typ hier uw antwoord...")

if user_input:
    antwoord = user_input.lower().strip()
    st.session_state.laatste_antwoord = antwoord
    st.session_state.messages_pg.append(
        {"role": "user", "content": user_input}
    )
else:
    antwoord = st.session_state.laatste_antwoord

# ----------------------------
# STAP 2 → ExtraZorg verwerken
# ----------------------------
if st.session_state.step_pg == 2 and antwoord:
    if antwoord in ["ja", "nee"]:
        st.session_state.choices["extraZorg"] = antwoord

        if antwoord == "ja":
            advies = "Essentieel: basis + aanvullende zorgverzekering"
            bot_message("Dan adviseren wij een basis + aanvullende zorgverzekering.")
        else:
            advies = "Essentieel: basis zorgverzekering"
            bot_message("Een basis zorgverzekering is voldoende.")

        st.session_state.choices["zorgverzekering"] = advies
        st.session_state.step_pg = 3
        st.session_state.laatste_antwoord = ""
        st.rerun()
    else:
        bot_message("Antwoord met ja of nee.")
        st.rerun()

# ----------------------------
# STAP 3 → WoonSituatie check
# ----------------------------
if st.session_state.step_pg == 3:
    woonSituatie = st.session_state.get("woonSituatie", "Huurwoning")
    if woonSituatie == "Koopwoning":
        bot_message("Wat is de hoogte van uw resterende hypotheek? (bedrag in euro)")
        st.session_state.step_pg = 4
    else:
        bot_message("Geen koopwoning, dus geen overlijdensrisicoverzekering nodig.")
        st.session_state.step_pg = 5
    st.rerun()

# ----------------------------
# STAP 4 → Hypotheek verwerken
# ----------------------------
if st.session_state.step_pg == 4 and antwoord:
    try:
        cleaned = antwoord.replace("€", "").replace(" ", "").replace(".", "").replace(",", "")
        hypotheek = int(cleaned)
        st.session_state.choices["resterende_hypotheek"] = hypotheek

        if hypotheek >= 25000:
            bot_message(
                f"Bij een resterende hypotheek van €{hypotheek:,} is een overlijdensrisicoverzekering essentieel."
            )
        else:
            bot_message(
                f"Bij een resterende hypotheek van €{hypotheek:,} is een overlijdensrisicoverzekering aanbevolen voor kinderen/partner."
            )

        st.session_state.step_pg = 5
        st.session_state.laatste_antwoord = ""
        st.rerun()
    except ValueError:
        bot_message("Voer een geldig bedrag in, bijvoorbeeld 250000.")
        st.rerun()

# ----------------------------
# STAP 5 → Leeftijd vragen
# ----------------------------
if st.session_state.step_pg == 5:
    bot_message("Hoe oud bent u? (voer een getal in)")
    st.session_state.step_pg = 6
    st.rerun()

# ----------------------------
# STAP 6 → Leeftijd verwerken
# ----------------------------
if st.session_state.step_pg == 6 and antwoord:
    try:
        leeftijd = int(antwoord)
        st.session_state.choices["leeftijd"] = leeftijd
        bot_message(f"Uw leeftijd is geregistreerd als {leeftijd} jaar.")

        if leeftijd >= 40:
            bot_message("Bent u bereid om spaargeld uit te geven aan uitvaart? (ja / nee)")
            st.session_state.step_pg = 7
        else:
            bot_message("Loop bij de dokter langs voor preventieve check-ups.")
            st.session_state.step_pg = 8

        st.session_state.laatste_antwoord = ""
        st.rerun()
    except ValueError:
        bot_message("Voer alstublieft een geldig getal in, bijvoorbeeld 35.")
        st.rerun()

# ----------------------------
# STAP 7 → Uitvaartvraag
# ----------------------------
if st.session_state.step_pg == 7 and antwoord:
    if antwoord in ["ja", "nee"]:
        st.session_state.choices["uitvaart"] = antwoord

        if antwoord == "ja":
            bot_message("Aanbevolen: optionele uitvaartverzekering.")
        else:
            bot_message("Essentieel: basis uitvaartverzekering.")

        st.session_state.step_pg = 8
        st.session_state.laatste_antwoord = ""
        st.rerun()
    else:
        bot_message("Antwoord met ja of nee.")
        st.rerun()


werkSituatie = st.session_state.get("werkSituatie", None)
# ----------------------------
# STAP 8 → Werk situatie / juridisch conflict
# ----------------------------
if st.session_state.step_pg == 8:
    if werkSituatie == "zzp":
        bot_message("Essentieel: rechtsbijstandverzekering voor zzp.")
    else:
        bot_message("Optioneel: rechtsbijstandverzekering. Controleer eerdere juridische conflicten.")
    st.session_state.step_pg = 99
    st.rerun()





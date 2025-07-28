#%% packages
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from rich import console
from rich.markdown import Markdown 

#%% Definition der Variablen



#%% LLM Modell
model = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", temperature=0)
 
 #%% Streamlit App / Chatbot Interface
st.title("Chatbot - Automotive News")
MANUFACTURER = st.chat_input(placeholder="Which automotive manufacturer do you want to know more about?")
DAYS = st.slider("Which time period (last # of days) you want to evaluate? ", 30, 365, 30)
WEEK = f"{(datetime.today() - timedelta(days=30)).strftime('%d.%m.%Y')}-{datetime.today().strftime('%d.%m.%Y')}"
LANGUAGE = st.chat_input(placeholder="In which language do you want the information? (default = EN)", key="language")

#%%
if MANUFACTURER is not None:
    if DAYS is not None:
        if LANGUAGE is None:
            LANGUAGE = "EN"
            messages = [
            ("system", "Du bist eine Experte in der Automobilbranche und kennst Dich mit der Marke der der User sendet sehr gut aus."
            " Ich möchte dass Du Neuigkeiten, Informationen, neue Partnerschaften und aktuellste Finanzkennzahlen wie YoY Sales und Marginentwicklung (sowohl Anstieg alsauch Rückgang) zusammenstellst. "
            " Bitte starte mit einer übergreifende Zusammenfassung von maximal 200 Wörter welcher der aktuelle Geschäftssituation im Vergleich zu der Geschäftssituation im vergangene Jahr beschreibt"
            " Ich brauche pro Region (Asien, Europa, Americas) eine bullet point Liste, maximal 3 Punkte pro Region, jeder Punkt maximal 30 Wörter."
            " Bitte vermelde die Quelle als internetlink hinter jeden Bullet Punkt"
            " Bitte schreib ein Titel mit welche Zeitraum du für die Auswertung betrachtet hast."
            " Bitte schreib die zusammenfassung in der sprache der der user dir meldet."
            " Bitte beachte dass die Informationen die du mir lieferst, nicht älter als 30 Tage sind."
            " Bitte schreibe die Zusammenfassung mit objektiven Informationen, ohne persönliche Meinungen oder Bewertungen."
            " Wenn Du unsicher bist, ob eine Information korrekt ist, lasse sie weg."),
            ("user","Hersteller: {manufacturer}"),
            ("user","TimeFrame: {week}"),
            ("user","Sprache: {language}")
]

    prompt_template = ChatPromptTemplate.from_messages(messages)
    chain = prompt_template | model | StrOutputParser()

    
    chain_inputs = {"manufacturer": MANUFACTURER, "week": WEEK, "language": LANGUAGE}
    res = chain.invoke(chain_inputs)


    st.chat_message("user").write(MANUFACTURER)
    st.chat_message("assistant").write(res)




#%% Ausgabe der Ergebnisse

#%%
# console.print(Markdown(res))
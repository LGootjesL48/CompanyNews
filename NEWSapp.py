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
#model = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct", temperature=0)

model = ChatGroq(model="meta-llama/Meta-Llama-3.1-8B-Instruct")

 #%% Streamlit App / Chatbot Interface
st.title("AI - Automotive News")
MANUFACTURER = st.chat_input(placeholder="Which automotive manufacturer do you want to know more about?")
DAYS = st.slider("Which time period (last # of days) you want to evaluate? ", 30, 365, 30)
WEEK = f"{(datetime.today() - timedelta(days=DAYS)).strftime('%d.%m.%Y')}-{datetime.today().strftime('%d.%m.%Y')}"
LANGUAGE = "EN"

#%%
if MANUFACTURER is not None:
    if DAYS is not None:
        #LANGUAGE = st.selectbox("In which language do you want the summary?", ["EN", "DE"], index=1)
        messages = [
        ("system", "Du bist eine Experte in der Automobilbranche und kennst Dich mit der Marke der der User sendet sehr gut aus."
        " Ich möchte dass Du Neuigkeiten, Informationen, neue Partnerschaften und aktuellste Finanzkennzahlen wie YoY Sales und Marginentwicklung (sowohl Anstieg alsauch Rückgang) zusammenstellst. "
        " Bitte starte mit einer übergreifende Zusammenfassung von maximal 200 Wörter welcher der aktuelle Geschäftssituation im Vergleich zu der Geschäftssituation im vergangene Jahr beschreibt"
        " Ich brauche pro Region (Asien, Europa, Americas) eine bullet point Liste, maximal 3 Punkte pro Region, jeder Punkt maximal 50 Wörter."
        " Bitte vermelde die Quelle als internetlink hinter jeden Bullet Punkt. Der Link soll die Information belegen"
        " Bitte schreib ein Titel mit welche Zeitraum du für die Auswertung betrachtet hast."
        " Bitte schreib die zusammenfassung in der sprache der der user dir meldet."
        " Bitte schreibe die Zusammenfassung mit objektiven Informationen, ohne persönliche Meinungen oder Bewertungen."
        " Wenn Du keine funtionierende Datenquelle hast, lasse die zugehörige Information weg."),
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
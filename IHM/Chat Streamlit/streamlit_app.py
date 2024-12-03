import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Récupérer votre clé API Gemini
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def call_gemini_api(prompt):
    response = model.generate_content(contents=prompt)
    rep = response.candidates[0].content.parts[0].text
    return rep

st.title("Assistance à la Maintenance")

btn_audio = st.button("Audio")

user_quest = st.text_input("Saisir votre question :")

btn = st.button("Demander")

if btn and user_quest:
    result = call_gemini_api(user_quest)
    st.write("Response from Gemini API:")
    st.write(result)


    
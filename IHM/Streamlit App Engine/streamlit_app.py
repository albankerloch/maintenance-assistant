import streamlit as st
import requests

def LLM_Response(question):
    response = requests.get("https://poc-edf-gateway-bxostszx.ew.gateway.dev/prompt?prompt=" + question)
    return response.json()["response_text"]

st.title("Assitance à la Maintenance")

user_quest = st.text_input("Saisir votre question :")

btn = st.button("Demander")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.subheader("Response : ")
    st.text(result)
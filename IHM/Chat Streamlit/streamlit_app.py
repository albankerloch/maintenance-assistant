import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

# Récupérer votre clé API Gemini
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
st.session_state.messages = []
st.session_state.gemini_history = []
st.session_state.model = model
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
st.session_state.chat_title = 'ChatSession-1'
st.session_state.chat_id = 1

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'upload_mode' not in st.session_state:
    st.session_state['upload_mode'] = False

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

def call_gemini_text(prompt):
    response = model.generate_content(prompt)
    rep = response.candidates[0].content.parts[0].text
    return rep

def call_gemini_image(prompt, image):
    response = model.generate_content([prompt, image[0], prompt])
    rep = response.candidates[0].content.parts[0].text
    return rep

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role

def fetch_gemini_response(user_query):
    # Use the session's model to generate a response
    response = st.session_state.chat_session.model.generate_content(user_query)
    print(f"Gemini's Response: {response}")
    return response.parts[0].text

st.title("Assistance à la Maintenance")

btn_audio = st.button("Audio")

btn_photo = st.button("Ajouter une photo")

if btn_photo:
    if st.session_state['uploaded_file'] is not None:
        st.session_state['uploaded_file'] = None
        st.session_state['upload_mode'] = False
    else:
        st.session_state['upload_mode'] = not st.session_state['upload_mode']

if st.session_state['upload_mode'] and st.session_state['uploaded_file'] is None:
    uploaded = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        st.session_state['uploaded_file'] = uploaded
        st.session_state['upload_mode'] = False

if st.session_state['uploaded_file'] is not None:
    if st.button("Retirer l'image"):
        st.session_state['uploaded_file'] = None
        st.session_state['upload_mode'] = False
    if st.session_state['uploaded_file'] is not None:
        img = Image.open(st.session_state['uploaded_file'])
        st.image(img, caption='Image à envoyer', width=100)

for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

user_input = st.chat_input("Demander à Gemini ...")

if user_input:
    st.chat_message("user").markdown(user_input)
    if st.session_state['uploaded_file'] is not None:
        image_data = input_image_setup(st.session_state['uploaded_file'])
        result = call_gemini_image(user_input, image_data)
    else:
        result = call_gemini_text(user_input)
    with st.chat_message("assistant"):
        st.markdown(result)
    st.session_state.chat_session.history.append({"role": "user", "content": user_input})
    st.session_state.chat_session.history.append({"role": "model", "content": result})
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

# Récupérer votre clé API Gemini
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'


# Initialisation de l'état de session pour l'historique
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'gemini_history' not in st.session_state:
    st.session_state.gemini_history = []

# Configuration du modèle et du chat
st.session_state.model = genai.GenerativeModel('gemini-1.5-flash')
st.session_state.chat_session = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'upload_mode' not in st.session_state:
    st.session_state['upload_mode'] = False

def call_gemini_text(prompt):
    response = st.session_state.chat_session.send_message(prompt)
    rep = response.parts[0].text
    return rep

def call_gemini_image(prompt, image):
    response = st.session_state.chat_session.send_message([prompt, image[0], prompt])
    rep = response.parts[0].text
    return rep

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

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

for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

user_input = st.chat_input("Demander à Gemini ...")


user_input = st.chat_input('Your message here...')

if user_input:
    with st.chat_message('user'):
        st.markdown(user_input)
    st.session_state.messages.append(dict(role='user',content=user_input))
    if st.session_state['uploaded_file'] is not None:
        image_data = input_image_setup(st.session_state['uploaded_file'])
        result = call_gemini_image(user_input, image_data)
    else:
        result = call_gemini_text(user_input)
    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        st.markdown(result)
    st.session_state.messages.append(dict(role=MODEL_ROLE, content=result, avatar=AI_AVATAR_ICON))
    st.session_state.gemini_history = st.session_state.chat_session.history

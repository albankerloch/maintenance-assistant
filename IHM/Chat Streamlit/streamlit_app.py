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

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'upload_mode' not in st.session_state:
    st.session_state['upload_mode'] = False

def call_gemini_api(prompt, image):
    response = model.generate_content([prompt, image[0], prompt])
    rep = response.candidates[0].content.parts[0].text
    return rep

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
        st.image(img, caption='Image à envoyer', use_container_width =False, width=100)

user_quest = st.text_input("Saisir votre question :")

btn = st.button("Demander")

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

if btn and user_quest:
    image_data = input_image_setup(st.session_state['uploaded_file'])
    result = call_gemini_api(user_quest, image_data)
    st.write("Response from Gemini API:")
    st.write(result)


    
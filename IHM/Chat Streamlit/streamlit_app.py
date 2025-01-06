import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import base64
import os
import speech_recognition as sr
 
 
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
 
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
 
 
def call_gemini_text(prompt: str) -> str:
    """
    Appel à Gemini pour un prompt texte uniquement.
    """
    response = st.session_state.chat_session.send_message(prompt)
    return response.parts[0].text
 
def call_gemini_image(prompt: str, image):
    """
    Appel à Gemini pour un prompt texte et une image.
    """
    response = st.session_state.chat_session.send_message([prompt, image[0], prompt])
    return response.parts[0].text
 
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
 
 
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez maintenant...")
        try:
            audio = r.listen(source, phrase_time_limit=5)  # time limit ( 5 seconds)
        except sr.WaitTimeoutError:
            print("Votre voix n'a pas été détecté à temps, veuillez réessayer!")
            return None
        except Exception as e:
            print(f"Une erreur a été detecté, Veuillez réessayer : {e}")
            return None
    try:
        text = r.recognize_google(audio, language="fr-FR")
        print("Vous avez dit : " + text)
        return text
    except sr.UnknownValueError:
        print("L'audio n'a pas été pris en compte")
        return None
    except sr.RequestError as e:
        print(f"La requête ne s'est pas effectué; {e}")
        return None
 
# Microphone Button Click
def microphone_button_clicked():
  st.session_state['microphone_active'] = not st.session_state['microphone_active']
  if st.session_state['microphone_active']:
    user_prompt = record_audio()
    if user_prompt:
      st.session_state["messages"].append({"role": "user", "content": user_prompt})
      bot_response = call_gemini_text(user_prompt)
      st.session_state["messages"].append({"role": "bot", "content": bot_response})
      st.session_state.gemini_history = st.session_state.chat_session.history
    else:
      st.error("Could not understand audio, please try again.")
  else:
    st.success("Microphone is OFF")
 
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
 
microphone_image_path = "images/microphone.png"
microphone_off_path = "images/microphone.png"
microphone_on_path = "images/pause.png"
chatbot_image_path = "images/chatbot (2).png"
camera_image_path = "images/camera.png"
 
# Initialisation des états de session
if 'microphone_active' not in st.session_state:
    st.session_state['microphone_active'] = False
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'upload_mode' not in st.session_state:
    st.session_state['upload_mode'] = False
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
 
# Basculer l'état du microphone via query_params
if st.query_params.get("toggle_microphone"):
    st.session_state['microphone_active'] = not st.session_state['microphone_active']
 
def toggle_microphone():
    st.session_state['microphone_active'] = not st.session_state['microphone_active']
 
current_image_base64 = (
    get_image_base64(microphone_on_path)
    if st.session_state['microphone_active']
    else get_image_base64(microphone_off_path)
)
 
# Disposition en colonnes (micro, chatbot, camera)
col1, col2, col3 = st.columns([0.07, 0.9, 0.1], gap="small")
 
# Bouton Microphone
with col1:
    if st.button(
        "",
        on_click=microphone_button_clicked,
        icon=":material/mic:" if st.session_state.get('microphone_active') else ":material/mic_off:"
    ):
        if st.session_state['microphone_active']:
            st.success("Microphone is ON")
        else:
            st.warning("Microphone is OFF")
 
#Logo Chatbot
with col2:
    chatbot_base64 = get_image_base64(chatbot_image_path)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <a href="?action=chatbot">
                <img src="data:image/png;base64,{chatbot_base64}" alt="chatbot" style="width: 100px; border-radius: 10px;">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
# Bouton Caméra
with col3:
    if st.button(label="", icon=":material/add_a_photo:"):
        # Si une image est déjà uploadée, on la retire
        if st.session_state['uploaded_file'] is not None:
            st.session_state['uploaded_file'] = None
            st.session_state['upload_mode'] = False
        else:
            # Sinon, on entre/sort du mode upload
            st.session_state['upload_mode'] = not st.session_state['upload_mode']
 
# Si on est en mode upload et qu'aucune image n'est uploadée, afficher le file_uploader
if st.session_state['upload_mode'] and st.session_state['uploaded_file'] is None:
    uploaded = st.file_uploader("Choisissez une image...", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        st.session_state['uploaded_file'] = uploaded
        # On peut sortir du mode upload après sélection
        st.session_state['upload_mode'] = False
 
# Retirer l'image
if st.session_state['uploaded_file'] is not None:
    if st.button("Retirer l'image"):
        st.session_state['uploaded_file'] = None
        st.session_state['upload_mode'] = False
    if st.session_state['uploaded_file'] is not None:
        img = Image.open(st.session_state['uploaded_file'])
        st.image(img, caption='Image à envoyer', use_container_width=False, width=100)
 
if 'welcome_shown' not in st.session_state:
    st.markdown(
        """
        <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px;">
            Bonjour, n’hésitez pas à me poser des questions avec le micro ou m’envoyer des photos avec les icônes ci-dessus.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.session_state['welcome_shown'] = True
 
st.markdown(
    """
    <hr style="border: 2.5px solid #76C1F2; margin-top: 20px; margin-bottom: 20px;border-radius: 10px;">
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div style="text-align: center;"><h1> CHATBOT</h1></div>
    """,
    unsafe_allow_html=True,
)
 
prompt = st.chat_input("Tapez votre question ici...")
 
if prompt:
    user_msg = {"role": "user", "content": prompt.strip()}
 
    if st.session_state["uploaded_file"] is not None:
        image_data = input_image_setup(st.session_state["uploaded_file"])
        st.session_state["uploaded_file"] = None
        bot_response = call_gemini_image(prompt, image_data)
    else:
        bot_response = call_gemini_text(prompt)
    st.session_state["messages"].append(user_msg)
    st.session_state["messages"].append({"role": "bot", "content": bot_response})
    st.session_state.gemini_history = st.session_state.chat_session.history
 
# Affichage
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(
            f"<div style='text-align: right; color: white; background-color: black; "
            f"padding: 10px; border-radius: 10px; margin-left: 280px; margin-bottom: 20px'>"
            f"{message['content']}</div>",
            unsafe_allow_html=True,
        )
        if 'image' in message and message['image'] is not None:
            user_img = Image.open(message['image'])
            st.markdown(
                "<div style='text-align: right; margin-left: 280px; margin-bottom: 20px;'>",
                unsafe_allow_html=True
            )
            st.image(user_img, caption="Image envoyée", use_container_width=False)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # bot
        bot_col1, bot_col2 = st.columns([0.1, 0.9])
        with bot_col1:
            st.image(chatbot_image_path, width=20)
        with bot_col2:
            st.markdown(
                f"<div style='background-color: #f0f0f5; padding: 10px; border-radius: 10px; "
                f"margin-right: 250px; margin-bottom: 20px'>{message['content']}</div>",
                unsafe_allow_html=True,
            )
 
import streamlit as st
from streamlit_chat import message
from audio_recorder_streamlit import audio_recorder
from Alfred.apis import call_chatgpt_api, text_to_speech, call_whisper_api
from Alfred.constants import get_msg
import os
import base64


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        return md


st.set_page_config(
    page_title="Pademe AI",
    page_icon=":robot:"
)

st.title("Pademe") 

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if "value" not in st.session_state:
    st.session_state.value = ""

if "ai_msg" not in st.session_state:
    st.session_state['ai_msg'] = get_msg()

if "email" not in st.session_state:
    st.session_state.email = ""

def get_text():
    input_text = st.text_area("You: ", value=st.session_state.value, key="input")
    return input_text 

col1, col2 = st.columns([8, 1])

with col2:
    audio_bytes = audio_recorder(text="", icon_name="microphone", icon_size="6x")

if audio_bytes:
    input_text = call_whisper_api(audio_bytes)
    st.session_state.value = input_text

with col1:
    user_input = get_text()
col3, col4 = st.columns([10, 2])

email = st.text_input("Your email address", value=st.session_state.email)
if email:
    st.session_state.email = email

with col3:
    tts = st.checkbox(label="Speach Responses", value=False)
audio = st.empty()
if user_input:
    audio.empty()
    st.session_state['ai_msg'].append({"role": "user", "content": user_input})
    answer = call_chatgpt_api(user_input, st.session_state['ai_msg'], st.session_state.email)
    st.session_state['ai_msg'].append({"role": "assistant", "content": answer})
    st.session_state.past.append(user_input)
    st.session_state.generated.append(answer)
    if tts and text_to_speech():
        spoken_answer = text_to_speech()(answer)
        if os.path.exists("./audio.wav"):
            os.remove("./audio.wav")
        with open("./audio.wav", mode='bx') as f:
            f.write(spoken_answer)
        md = autoplay_audio("./audio.wav")
        audio.markdown(md, unsafe_allow_html=True)

with col4:
    clear = st.button("Reset Chat")

if clear:
    st.session_state['ai_msg'] = get_msg()
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.info("Chat cleared")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
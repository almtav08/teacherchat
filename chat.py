import time
import streamlit as st
from gradio_client import Client

def get_response_llama(client: Client, string):
    job = client.submit(
        string + "Contestame en español.",
        "Eres un profesor virtual, cuya tarea es responder a las preguntas y dudas de tus alumnos. Siempre debes ser cortés con tus mensajes y ofrecer apoyo. Tus respuestas deben ser simples para que los alumnos puedan entenderlas. Siempre debes recomendar la visita de material adicional para mejorar el conocimiento sobre su duda.",
        0,
        1000,
        0.6,
        1.2,
        api_name="/chat"
    )
    result = job.result()
    return result.replace("<s>", "").replace("</s>", "").strip()

st.title("Teacher Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    st.session_state.client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("En que puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner(""):
            assistant_response: str = get_response_llama(st.session_state.client, prompt)
        for chunk in assistant_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
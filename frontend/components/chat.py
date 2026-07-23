import time
import streamlit as st


def stream_text(text):

    placeholder = st.empty()

    current_text = ""

    for word in text.split():

        current_text += word + " "

        placeholder.markdown(current_text)

        time.sleep(0.02)

    return current_text


def render_chat(messages):

    for message in messages:

        role = message["role"]

        

        with st.chat_message(
            role,
            
        ):

            st.markdown(
                message["content"]
            )
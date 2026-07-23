import streamlit as st

from api_client import send_message

from utils.session import (
    add_message,
    get_current_chat
)

from components.chat import stream_text


def process_message(message):

    add_message(

        "user",

        message

    )

    chat = get_current_chat()

    if len(chat["messages"]) == 1:

        title = message[:30]

        chat["title"] = title

    with st.chat_message(

        "user",

        avatar=""

    ):

        st.markdown(message)

    with st.chat_message(

        "assistant",

        avatar=""

    ):

        with st.spinner(

            "Thinking..."

        ):

            result = send_message(

                message,

                "demo_user"

            )

        response = result["response"]

        stream_text(response)

    add_message(

        "assistant",

        response

    )
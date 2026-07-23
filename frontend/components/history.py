import streamlit as st


def render_history():

    chat = st.session_state.chats[

        st.session_state.current_chat

    ]

    return chat["messages"]
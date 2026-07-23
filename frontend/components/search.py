import streamlit as st


def search_messages(keyword):

    results = []

    for chat_id, chat in st.session_state.chats.items():

        for msg in chat["messages"]:

            if keyword.lower() in msg["content"].lower():

                results.append(

                    (

                        chat["title"],

                        msg["content"]

                    )

                )

    return results
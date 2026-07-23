import uuid

import streamlit as st


def init_session():

    if "chats" not in st.session_state:

        st.session_state.chats = {}

    if "current_chat" not in st.session_state:

        create_new_chat()


def create_new_chat():

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {

        "title": "New Chat",

        "messages": []

    }

    st.session_state.current_chat = chat_id

    return chat_id


def get_current_chat():

    return st.session_state.chats[

        st.session_state.current_chat

    ]


def add_message(

    role,

    content

):

    chat = get_current_chat()

    chat["messages"].append({

        "role": role,

        "content": content

    })


def rename_chat(

    chat_id,

    title

):

    title = title.strip()

    if title:

        st.session_state.chats[chat_id]["title"] = title


def delete_chat(

    chat_id

):

    if chat_id in st.session_state.chats:

        del st.session_state.chats[chat_id]


    if not st.session_state.chats:

        create_new_chat()

    else:

        if (

            st.session_state.current_chat

            == chat_id

        ):

            st.session_state.current_chat = next(

                iter(st.session_state.chats)

            )


def search_chats(

    keyword

):

    keyword = keyword.lower().strip()

    results = []


    if not keyword:

        return list(

            st.session_state.chats.items()

        )


    for chat_id, chat in st.session_state.chats.items():

        if keyword in chat["title"].lower():

            results.append(

                (chat_id, chat)

            )

            continue


        for message in chat["messages"]:

            if keyword in message["content"].lower():

                results.append(

                    (chat_id, chat)

                )

                break


    return results
import streamlit as st

from utils.session import (

    create_new_chat,

    delete_chat,

    rename_chat,

    search_chats

)


def render_sidebar():

    with st.sidebar:

        st.markdown(

            """

            <h1>EmpathyAI</h1>

            <p class="sidebar-subtitle">

                Your AI companion

            </p>

            """,

            unsafe_allow_html=True

        )


        if st.button(

            "+ New Chat",

            use_container_width=True

        ):

            create_new_chat()

            st.rerun()


        st.divider()


        search_query = st.text_input(

            "Search chats",

            placeholder="Search your chats..."

        )


        st.divider()


        results = search_chats(

            search_query

        )


        if not results:

            st.caption(

                "No chats found."

            )


        for chat_id, chat in results:

            is_current = (

                chat_id

                == st.session_state.current_chat

            )


            title = chat["title"]


            if is_current:

                title = f"● {title}"


            if st.button(

                title,

                key=f"chat_{chat_id}",

                use_container_width=True

            ):

                st.session_state.current_chat = chat_id

                st.rerun()


            if is_current:

                col1, col2 = st.columns(2)


                with col1:

                    if st.button(

                        "Rename",

                        key=f"rename_{chat_id}"

                    ):

                        st.session_state.rename_chat_id = chat_id

                        st.rerun()


                with col2:

                    if st.button(

                        "Delete",

                        key=f"delete_{chat_id}"

                    ):

                        delete_chat(chat_id)

                        st.rerun()


        if (

            "rename_chat_id"

            in st.session_state

        ):

            chat_id = (

                st.session_state.rename_chat_id

            )


            st.divider()


            st.markdown(

                "### Rename Chat"

            )


            new_title = st.text_input(

                "New title",

                value=st.session_state.chats[

                    chat_id

                ]["title"],

                key="rename_input"

            )


            col1, col2 = st.columns(2)


            with col1:

                if st.button(

                    "Save",

                    use_container_width=True

                ):

                    rename_chat(

                        chat_id,

                        new_title

                    )

                    del st.session_state.rename_chat_id

                    st.rerun()


            with col2:

                if st.button(

                    "Cancel",

                    use_container_width=True

                ):

                    del st.session_state.rename_chat_id

                    st.rerun()
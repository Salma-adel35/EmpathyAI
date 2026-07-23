import streamlit as st


from config import USER_ID


from api_client import send_message


from utils.session import (
    init_session,
    get_current_chat,
    add_message
)


from components.sidebar import (
    render_sidebar
)


from components.chat import (
    render_chat,
    stream_text
)


from components.welcome import (
    render_welcome
)




# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(

    page_title="EmpathyAI",

    page_icon="💙",

    layout="wide",

    initial_sidebar_state="expanded"

)


# =========================
# LOAD CSS
# =========================

with open(

    "assets/style.css",

    encoding="utf-8"

) as file:

    st.markdown(

        f"<style>{file.read()}</style>",

        unsafe_allow_html=True

    )


# =========================
# INITIALIZE SESSION
# =========================

init_session()


# =========================
# SIDEBAR
# =========================

render_sidebar()


# =========================
# HEADER
# =========================




# =========================
# CURRENT CHAT
# =========================

chat = get_current_chat()


# =========================
# DISPLAY CHAT OR WELCOME
# =========================

if not chat["messages"]:

    render_welcome()

else:

    render_chat(

        chat["messages"]

    )


# =========================
# GET USER MESSAGE
# =========================

pending_message = st.session_state.pop(

    "pending_message",

    None

)


prompt = st.chat_input(

    "Message EmpathyAI..."

)


message = (

    prompt

    if prompt

    else pending_message

)


# =========================
# PROCESS MESSAGE
# =========================

if message:

    # Add user message

    add_message(

        "user",

        message

    )


    # Get current chat

    chat = get_current_chat()


    # Create chat title

    if len(chat["messages"]) == 1:

        chat["title"] = message[:30]


    # Display user message

    with st.chat_message(

        "user",

        avatar="🧑"

    ):

        st.markdown(

            message

        )


    # Generate assistant response

    with st.chat_message(

        "assistant",

        avatar="💙"

    ):

        with st.spinner(

            "Thinking..."

        ):

            result = send_message(

                message,

                USER_ID

            )


        response = result.get(

            "response",

            "Something went wrong."

        )


        # Typing animation

        stream_text(

            response

        )


    # Save assistant response

    add_message(

        "assistant",

        response

    )
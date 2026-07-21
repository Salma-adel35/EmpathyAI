import streamlit as st

from api_client import send_message


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EmpathyAI",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */

    .stApp {
        background-color: #0f1117;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #151820;
        border-right: 1px solid #282c36;
    }


    /* Header */

    .app-header {
        padding: 18px 0 10px 0;
        border-bottom: 1px solid #282c36;
        margin-bottom: 25px;
    }

    .app-title {
        font-size: 28px;
        font-weight: 700;
        color: #f5f7fa;
        margin-bottom: 2px;
    }

    .app-subtitle {
        font-size: 14px;
        color: #9ca3af;
    }


    /* Welcome section */

    .welcome-container {
        text-align: center;
        padding: 70px 20px 30px 20px;
    }

    .welcome-icon {
        font-size: 52px;
        margin-bottom: 15px;
    }

    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: #f5f7fa;
    }

    .welcome-text {
        color: #9ca3af;
        font-size: 16px;
        max-width: 650px;
        margin: auto;
        line-height: 1.6;
    }


    /* Emotion card */

    .emotion-card {
        background-color: #1a1e27;
        border: 1px solid #2c3240;
        border-radius: 12px;
        padding: 14px 16px;
        margin: 12px 0;
    }

    .emotion-title {
        font-size: 12px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .emotion-value {
        font-size: 18px;
        color: #f5f7fa;
        font-weight: 600;
        margin-top: 4px;
    }


    /* Context status */

    .context-status {
        background-color: #171b23;
        border: 1px solid #292e39;
        border-radius: 10px;
        padding: 12px;
        margin-top: 15px;
        font-size: 13px;
        color: #b8bec9;
    }


    /* Suggestion buttons */

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #303643;
        background-color: #191d26;
        color: #d9dde5;
        min-height: 45px;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        border-color: #6b7280;
        background-color: #222733;
    }


    /* Chat messages */

    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 10px;
    }


    /* Input */

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }


    /* Hide Streamlit branding */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []


if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding: 10px 0 25px 0;">
            <div style="
                font-size: 24px;
                font-weight: 700;
                color: #f5f7fa;
            ">
                💙 EmpathyAI
            </div>

            <div style="
                font-size: 13px;
                color: #9ca3af;
                margin-top: 5px;
            ">
                Emotionally-aware AI support
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "＋ New Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.emotion_history = []

        st.session_state.last_analysis = None

        st.rerun()


    st.divider()


    st.markdown(
        "### 🧠 Emotional Journey"
    )


    if st.session_state.emotion_history:

        for emotion in reversed(
            st.session_state.emotion_history[-5:]
        ):

            st.markdown(
                f"""
                <div class="emotion-card">
                    <div class="emotion-title">
                        Detected emotion
                    </div>

                    <div class="emotion-value">
                        {emotion}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "Your detected emotions will appear here during the conversation."
        )


    st.divider()


    st.markdown(
        "### 🔗 Context Used"
    )


    if st.session_state.last_analysis:

        analysis = st.session_state.last_analysis

        memory_status = (
            "Used"
            if analysis.get("memory_used")
            else "Not used"
        )

        rag_status = (
            "Used"
            if analysis.get("rag_used")
            else "Not used"
        )

        st.markdown(
            f"""
            <div class="context-status">
                🧠 Conversation Memory: {memory_status}<br><br>
                📚 Relevant Knowledge: {rag_status}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.caption(
            "Context information will appear after your first message."
        )


    st.divider()


    st.caption(
        "EmpathyAI is an AI support assistant and does not replace professional help."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">

        <div class="app-title">
            EmpathyAI
        </div>

        <div class="app-subtitle">
            A context-aware AI assistant that understands emotions,
            intent, and conversation history.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-icon">
                💙
            </div>

            <div class="welcome-title">
                Welcome to EmpathyAI
            </div>

            <div class="welcome-text">
                A safe space to express yourself.
                EmpathyAI understands the emotional context
                behind your messages and responds with
                personalized, supportive conversations.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "### 💭 You can start with..."
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "😣 I'm feeling overwhelmed",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I am feeling overwhelmed."
            )

            st.rerun()


        if st.button(
            "💬 I just want to talk",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I just want someone to listen."
            )

            st.rerun()


    with col2:

        if st.button(
            "🎯 I need some advice",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I need some advice about something I am going through."
            )

            st.rerun()


        if st.button(
            "🌱 I need motivation",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I need some motivation right now."
            )

            st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

pending_message = st.session_state.pop(
    "pending_message",
    None
)


user_input = st.chat_input(
    "Share what's on your mind..."
)


message_to_send = (
    user_input
    if user_input
    else pending_message
)


if message_to_send:

    # Add user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message_to_send
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            message_to_send
        )


    # Generate response

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "EmpathyAI is thinking..."
        ):

            result = send_message(
                message_to_send
            )


        response = result.get(
            "response",
            "I am here to listen."
        )


        st.markdown(
            response
        )


    # Save assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    # Save emotion

    emotion = result.get(
        "emotion",
        "Unknown"
    )

    emotion_emoji = result.get(
        "emotion_emoji",
        "💭"
    )


    st.session_state.emotion_history.append(
        f"{emotion_emoji} {emotion}"
    )


    # Save analysis

    st.session_state.last_analysis = result


    st.rerun()
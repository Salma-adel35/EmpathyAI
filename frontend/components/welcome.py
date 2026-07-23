import streamlit as st


def render_welcome():

    st.markdown(
        """
        <div class="welcome-container">

                     Welcome to EmpathyAI

            
                Your emotionally-aware AI assistant.
            

        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "I'm overwhelmed",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I feel overwhelmed."
            )

            st.rerun()


        if st.button(
            "I'm sad",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I feel sad."
            )

            st.rerun()


    with col2:

        if st.button(
            "I need advice",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I need advice."
            )

            st.rerun()


        if st.button(
            "I feel happy",
            use_container_width=True
        ):

            st.session_state.pending_message = (
                "I feel happy."
            )

            st.rerun()
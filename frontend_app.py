import streamlit as st
from backend_chatbot import ask_question
import base64

# ==================================================
# Page Config
# ==================================================

st.set_page_config(page_title="NineSol Assistant", page_icon="🤖", layout="wide")


# ==================================================
# Background Image
# ==================================================


def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


bin_str = get_base64("ninesol_logo1.png")

background_style = f"""
<style>

/* Background */
.stApp {{
    background-image: url("data:image/png;base64,{bin_str}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Dark overlay for better readability */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.35);
    pointer-events: none;
    z-index: 0;
}}

/* Keep content above overlay */
.main {{
    position: relative;
    z-index: 1;
}}

/* Main Content Width */
.block-container {{
    max-width: 950px;
    padding-top: 2rem;
}}

/* Header Card */
.title-box {{
    background: rgba(0,0,0,0.75);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}}

.title-box h1 {{
    color: #00E5FF;
    margin-bottom: 5px;
}}

.title-box p {{
    color: #F5F5F5;
    margin: 0;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.80);
}}

/* Chat Messages */
[data-testid="stChatMessage"] {{
    background: rgba(0,0,0,0.55);
    padding: 12px;
    border-radius: 15px;
    backdrop-filter: blur(8px);
    margin-bottom: 10px;
}}

/* Chat Input */
.stChatInput {{
    background: rgba(0,0,0,0.60);
}}

/* Footer */
.footer {{
    text-align: center;
    color: #EAEAEA;
    opacity: 0.85;
    margin-top: 30px;
}}

/* Sidebar text */
.sidebar-text {{
    color: white;
}}

/* Hide Streamlit Menu */
#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

</style>
"""

st.markdown(
    """
    <h2 style='color:#00E5FF;'>
        NineSol Technologies
    </h2>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# Sidebar
# ==================================================

with st.sidebar:

    st.image("ninesol_logo1.png", width=300)

    st.markdown("## NineSol Technologies")

    st.markdown("""
Welcome to the NineSol AI Assistant.

You can ask questions about:

- Company Services
- Technologies
- Projects
- Team Information
- Internal Knowledge Base
""")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()




col1, col2 = st.columns([1, 4])

with col1:
    st.image("ninesol_logo1.png", width=400 )

with col2:
    st.markdown(
        """
        <div class="title-box">
            <h1>🤖 NineSol AI Assistant</h1>
            <p>Your intelligent assistant for NineSol Technologies</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit_user"


# ==================================================
# Display Chat History
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ==================================================
# User Input
# ==================================================

user_prompt = st.chat_input("Ask something about NineSol Technologies...")


if user_prompt:

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching NineSol knowledge base..."):

            answer = ask_question(user_prompt, st.session_state.session_id)

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ==================================================
# Footer
# ==================================================

st.markdown(
    """
    <div class="footer">
        Let me know if you need any help regarding to NineSol Technologies
    </div>
    """,
    unsafe_allow_html=True,
)

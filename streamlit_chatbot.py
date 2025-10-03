# Import library yang dibutuhkan
import streamlit as st
import time

# Pastikan library ini sudah terinstall: pip install langchain-google-genai langgraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Konfigurasi Halaman & Tampilan Dasar ---
st.set_page_config(
    page_title="Petualangan Mesin Waktu",
    page_icon="🕰️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. Fungsi CSS untuk Tampilan Kustom ---
def add_custom_styling():
    st.markdown("""
    <style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Background animasi futuristik */
    .stApp {
        background: linear-gradient(-45deg, #0d0d2b, #1a1a40, #001f54, #003566);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: white !important;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Judul futuristik */
    h1, .stTitle {
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0px 0px 15px rgba(0,255,255,0.8);
        letter-spacing: 2px;
    }

    /* Caption */
    .stCaption {
        color: #e0e0e0 !important;
        font-style: italic;
    }

    /* Chat input */
    .stChatInput textarea {
        border-radius: 20px !important;
        padding: 12px !important;
        background-color: rgba(255,255,255,0.9) !important;
        color: black !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }

    /* Chat bubble */
    [data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 0 20px rgba(0,255,255,0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(6px);
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(90, 40, 200, 0.7), rgba(0, 180, 255, 0.6));
        border-left: 4px solid cyan;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(0, 200, 150, 0.7), rgba(0, 150, 200, 0.6));
        border-left: 4px solid lime;
    }

    /* Sidebar futuristik */
    [data-testid="stSidebar"] {
        background: rgba(15, 20, 40, 0.9) !important;
        border-right: 2px solid cyan;
        backdrop-filter: blur(12px);
    }

    /* Tombol utama */
    button[kind="primary"], .stButton > button {
        border-radius: 12px;
        background: linear-gradient(90deg, #009ffd, #2a2a72);
        color: white;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(0,255,255,0.5);
    }
    button[kind="primary"]:hover, .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(0,255,255,0.8);
    }

    /* Tombol pertanyaan cepat */
    .stButton > button {
        margin-top: 8px;
        border-radius: 10px !important;
        background: rgba(0, 255, 200, 0.2);
        border: 1px solid rgba(0, 255, 200, 0.6);
    }
    .stButton > button:hover {
        background: rgba(0, 255, 200, 0.4);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# Terapkan CSS
add_custom_styling()

# --- 3. Judul dan Header ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/6028/6028690.png", width=120)
with col2:
    st.title("Petualangan Mesin Waktu 🕰️")
    st.caption("Jelajahi Sejarah Dunia Bersama Profesor Cerdas! 🚀")

# --- 4. Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1693/1693746.png", width=100)
    st.subheader("⚙️ Pengaturan Mesin Waktu")

    google_api_key = st.text_input(
        "🔑 Kunci Rahasia Google AI",
        type="password",
        help="Masukkan kunci rahasiamu untuk menyalakan mesin waktu!"
    )

    if st.button("🚀 Mulai Petualangan Baru", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### ✨ Ide Pertanyaan Seru:")

    questions = [
        "Siapa itu Gajah Mada?",
        "Ceritakan tentang kemerdekaan Indonesia!",
        "Seperti apa Piramida di Mesir?"
    ]
    for q in questions:
        if st.button(q, use_container_width=True):
            st.session_state.selected_question = q

# --- 5. Inisialisasi Agent & State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_agent(api_key):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.8
        )
        agent_prompt = """
        Kamu adalah Profesor Cerdas, robot penjelajah waktu yang ramah, lucu, dan antusias.
        Jelaskan sejarah kepada anak-anak SD dengan bahasa sederhana, penuh semangat,
        berikan fakta unik, dan gunakan banyak emoji. Selalu panggil pengguna 'Adik Penjelajah Waktu'.
        """
        st.session_state.agent = create_react_agent(model=llm, tools=[], prompt=agent_prompt)
        st.session_state._last_key = api_key
        st.session_state.messages = []
        return True
    except Exception as e:
        if "API key" in str(e):
            st.error("❌ Kunci Rahasiamu salah atau kedaluwarsa. Periksa lagi ya! 🗝️")
        else:
            st.error(f"Oh tidak! Mesin waktu error: {e}")
        return False

if not google_api_key:
    st.info("🔑 Masukkan 'Kunci Rahasia Google AI' di sidebar untuk memulai!", icon="🗝️")
    st.stop()
else:
    if "agent" not in st.session_state or getattr(st.session_state, "_last_key", None) != google_api_key:
        if not initialize_agent(google_api_key):
            st.stop()

# --- 6. Fungsi Chat ---
def stream_message(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

if not st.session_state.messages:
    welcome_message = "Halo, Adik Penjelajah Waktu! Aku Profesor Cerdas 🤖. Siap melintasi masa lalu? 🚀 Mau tahu apa hari ini? 🌍✨"
    with st.chat_message("assistant", avatar="🤖"):
        st.write_stream(stream_message(welcome_message))
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

for msg in st.session_state.messages:
    avatar = "🧑‍🚀" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 7. Input Pengguna ---
prompt = st.chat_input("Ketik pertanyaanmu di sini...")
if "selected_question" in st.session_state:
    prompt = st.session_state.selected_question
    del st.session_state.selected_question

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🚀"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Profesor Cerdas sedang melintasi lorong waktu... ⏳"):
            try:
                messages = [
                    HumanMessage(content=m["content"]) if m["role"] == "user" 
                    else AIMessage(content=m["content"]) 
                    for m in st.session_state.messages
                ]
                response = st.session_state.agent.invoke({"messages": messages})
                if response and "messages" in response and len(response["messages"]) > 0:
                    answer = response["messages"][-1].content
                else:
                    answer = "Hmm, sepertinya lorong waktu sedang terganggu... coba tanya lagi ya! ⚡"
            except Exception as e:
                answer = f"Oh tidak! Ada gangguan teknis di mesin waktu: {e}"

        st.write_stream(stream_message(answer))
    st.session_state.messages.append({"role": "assistant", "content": answer})

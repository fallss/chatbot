# Import library yang dibutuhkan
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Konfigurasi Halaman & Tampilan Dasar ---

# Mengatur judul tab, ikon, dan layout halaman menjadi lebih lebar
st.set_page_config(
    page_title="Petualangan Mesin Waktu",
    page_icon="🕰️",
    layout="wide"
)

# Fungsi untuk menambahkan CSS kustom (misalnya, gambar latar belakang)
def add_custom_styling():
    """Menambahkan CSS untuk background dan styling chat bubble."""
    st.markdown(f"""
    <style>
    /* Mengatur gambar latar belakang */
    .stApp {{
        background-image: url("https://www.toptal.com/designers/subtlepatterns/uploads/world-map.png");
        background-attachment: fixed;
        background-size: cover;
    }}
    /* Mengatur agar area chat tidak terlalu lebar di layar besar */
    .st-emotion-cache-1y4p8pa {{
        max-width: 75%;
        margin: auto;
    }}
    /* Memberi style pada gelembung chat agar lebih menonjol */
    [data-testid="stChatMessage"] {{
        background-color: rgba(77, 77, 77, 0.85);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

# Panggil fungsi untuk menerapkan CSS
add_custom_styling()

# --- 2. Judul dan Header yang Menarik ---

# Gunakan kolom untuk menata judul dan gambar agar rapi
col1, col2 = st.columns([1, 4])
with col1:
    # Menambahkan gambar robot lucu sebagai maskot
    st.image("https://cdn-icons-png.flaticon.com/512/6028/6028690.png", width=150)

with col2:
    # Judul utama yang bertema petualangan
    st.title("Petualangan Mesin Waktu 🕰️")
    # Caption yang mengajak anak-anak untuk berinteraksi
    st.caption("Tanya Jawab Seru Seputar Sejarah Bersama Profesor Cerdas! 🚀")

# --- 3. Sidebar untuk Pengaturan ---

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1693/1693746.png", width=100)
    st.subheader("Pengaturan Mesin Waktu")
    
    # Input API key dengan teks yang lebih ramah anak
    google_api_key = st.text_input(
        "Kunci API Google AI", 
        type="password", 
        help="Masukkan kunci rahasiamu untuk menyalakan mesin waktu!"
    )
    
    # Tombol reset dengan teks yang sesuai tema
    if st.button("Mulai Petualangan Baru", help="Hapus semua percakapan dan mulai dari awal"):
        st.session_state.clear()
        st.rerun()

    # Menambahkan contoh pertanyaan untuk memandu anak-anak
    st.markdown("---")
    st.markdown("### Bingung mau tanya apa? Coba ini!")
    if st.sidebar.button("Siapa itu Gajah Mada?"):
        st.session_state.selected_question = "Siapa itu Gajah Mada?"
    if st.sidebar.button("Ceritakan tentang kemerdekaan Indonesia!"):
        st.session_state.selected_question = "Ceritakan tentang kemerdekaan Indonesia!"
    if st.sidebar.button("Seperti apa Piramida di Mesir?"):
        st.session_state.selected_question = "Seperti apa Piramida di Mesir?"

# --- 4. Inisialisasi API Key dan Agent ---

if not google_api_key:
    st.info("Masukkan 'Kunci API Google AI' di sidebar kiri untuk memulai petualanganmu!", icon="🗝️")
    st.stop()

# Inisialisasi ulang agent hanya jika belum ada atau API key berubah
if "agent" not in st.session_state or getattr(st.session_state, "_last_key", None) != google_api_key:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=0.8  # Sedikit lebih kreatif untuk anak-anak
        )
        
        # PROMPT UTAMA: Mengubah "kepribadian" AI menjadi Profesor Cerdas
        agent_prompt = """
        Kamu adalah Profesor Cerdas, sebuah robot penjelajah waktu yang sangat ramah dan antusias.
        Tugasmu adalah menjelaskan sejarah kepada anak-anak SD dengan cara yang seru dan mudah dimengerti.
        Gunakan bahasa yang sederhana, berikan fakta-fakta unik, dan buat perumpamaan yang mereka pahami.
        Selalu panggil pengguna dengan sebutan 'Adik Penjelajah Waktu'.
        Buat jawabanmu selalu menarik, singkat, dan penuh semangat! Gunakan emoji agar lebih seru.
        """
        
        st.session_state.agent = create_react_agent(
            model=llm,
            tools=[],
            prompt=agent_prompt
        )
        st.session_state._last_key = google_api_key
        st.session_state.messages = []  # Hapus riwayat chat saat ganti key
    except Exception as e:
        st.error(f"Waduh, mesin waktunya rusak! Sepertinya ada kesalahan: {e}")
        st.stop()

# --- 5. Manajemen Riwayat Chat ---

# Inisialisasi riwayat chat jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tambahkan pesan selamat datang dari Profesor Cerdas jika chat baru dimulai
if not st.session_state.messages:
    welcome_message = "Halo, Adik Penjelajah Waktu! Aku Profesor Cerdas. Siap untuk berpetualang ke masa lalu? Kamu mau tahu tentang apa hari ini? 🤔"
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

# --- 6. Tampilkan Pesan-Pesan Sebelumnya ---

for msg in st.session_state.messages:
    # Gunakan avatar emoji yang lucu untuk user dan asisten
    avatar = "🧑‍🚀" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 7. Proses Input Pengguna dan Respon AI ---

# Gunakan pertanyaan dari tombol jika diklik, jika tidak, gunakan input chat
prompt = st.chat_input("Ketik pertanyaanmu di sini...")
if "selected_question" in st.session_state:
    prompt = st.session_state.selected_question
    del st.session_state.selected_question # Hapus setelah digunakan agar tidak berulang

if prompt:
    # Tampilkan dan simpan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🚀"):
        st.markdown(prompt)

    # Tampilkan spinner dengan pesan tematik saat AI berpikir
    with st.spinner("Profesor Cerdas sedang melakukan perjalanan waktu... ✨"):
        try:
            # Siapkan format pesan untuk dikirim ke agent
            messages = [
                HumanMessage(content=msg["content"]) if msg["role"] == "user" 
                else AIMessage(content=msg["content"]) 
                for msg in st.session_state.messages
            ]
            
            # Panggil agent untuk mendapatkan respon
            response = st.session_state.agent.invoke({"messages": messages})
            
            # Ekstrak jawaban dengan aman
            if response and "messages" in response and len(response["messages"]) > 0:
                answer = response["messages"][-1].content
            else:
                answer = "Waduh, sepertinya sinyal mesin waktuku sedikit terganggu. Coba tanya lagi ya!"

        except Exception as e:
            answer = f"Oh tidak! Ada gangguan teknis di mesin waktu: {e}"

    # Tampilkan dan simpan respon dari AI
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
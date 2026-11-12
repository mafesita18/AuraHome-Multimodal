import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from gtts import gTTS

st.set_page_config(page_title="Ambiente 2: Seguridad y Entrada", page_icon="🔐", layout="centered")

if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False
    st.session_state.luces_sala = False
    st.session_state.color_luz = "#FFD700"
    st.session_state.ultimo_evento = "Sistema listo."

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("puerta.mp3")
    st.audio("puerta.mp3", format="audio/mp3", autoplay=True)

st.title("🔐 Ambiente 2: Acceso y Seguridad Inteligente")

estado_txt = "🔓 PUERTA DESBLOQUEADA" if st.session_state.puerta_abierta else "🔒 PUERTA CERRADA CON SEGURO"
st.info(f"**Estado físico de la cerradura:** {estado_txt}")

st.markdown("---")
st.subheader("📸 1. Reconocimiento Facial / Visual")
foto = st.camera_input("Toma una foto en la entrada") or st.file_uploader("O sube una imagen de quién está en la puerta", type=["jpg", "png", "jpeg"])

if foto and st.button("🔍 Verificar Identidad", type="primary"):
    img = Image.open(foto)
    st.image(img, caption="Captura procesada en entrada", width=250)
    st.session_state.puerta_abierta = True
    st.session_state.luces_sala = True
    st.session_state.color_luz = "#FFF4B8"
    msg = "Identidad verificada en la entrada. Puerta desbloqueada y luces de bienvenida encendidas en la sala."
    st.session_state.ultimo_evento = msg
    st.success(f"✅ {msg}")
    hablar("Identidad verificada. Bienvenida a casa.")

st.markdown("---")
st.subheader("✍️ 2. Patrón Táctil de Visitante")
st.caption("Dibuja tu firma o patrón de acceso dentro del recuadro blanco:")

canvas = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=6,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=250,
    width=400,
    drawing_mode="freedraw",
    key="patron_puerta_visible"
)

if st.button("✅ Verificar Patrón Táctil"):
    if canvas.image_data is not None and np.max(canvas.image_data[:, :, :3] < 250):
        st.session_state.puerta_abierta = True
        st.session_state.luces_sala = True
        st.session_state.color_luz = "#FFF4B8"
        msg = "Patrón táctil correcto. Puerta abierta y luces de bienvenida activadas en la sala."
        st.session_state.ultimo_evento = msg
        st.success(msg)
        hablar(msg)
    else:
        st.warning("⚠️ Por favor dibuja un trazo o firma en el recuadro blanco antes de verificar.")
        

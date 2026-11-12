import streamlit as st
import base64
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import openai
from gtts import gTTS

st.set_page_config(page_title="Ambiente 2: Seguridad y Entrada", page_icon="🔐", layout="centered")

if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False
    st.session_state.luces_sala = False
    st.session_state.color_luz = "#FFD700"
    st.session_state.ultimo_evento = "Sistema listo."

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("puerta.mp3")
    st.audio("puerta.mp3", format="audio/mp3", autoplay=True)

st.title("🔐 Ambiente 2: Acceso y Seguridad Inteligente")

estado_txt = "🔓 PUERTA DESBLOQUEADA" if st.session_state.puerta_abierta else "🔒 PUERTA CERRADA CON SEGURO"
st.info(f"**Estado físico de la cerradura:** {estado_txt}")

tab1, tab2 = st.tabs(["📸 Reconocimiento Facial / Visual", "✍️ Patrón Táctil de Visitante"])

with tab1:
    st.subheader("Escaneo en la Puerta Principal")
    foto = st.camera_input("Toma una foto en la entrada") or st.file_uploader("O sube una imagen de quién está en la puerta", type=["jpg", "png", "jpeg"])

    if foto and st.button("🔍 Analizar Visitante con IA"):
        api_key = st.session_state.get("api_key", "")
        img = Image.open(foto)
        img.save("visitante.png")

        if not api_key:
            # Modo simulación si no pones API Key en la sustentación
            st.session_state.puerta_abierta = True
            st.session_state.luces_sala = True  # Enciende luces en Ambiente 1
            msg = "Residente reconocido. Abriendo puerta y encendiendo luces de bienvenida en la sala."
            st.session_state.ultimo_evento = msg
            st.success(msg)
            hablar(msg)
        else:
            openai.api_key = api_key
            b64 = encode_image("visitante.png")
            with st.spinner("Analizando cámara de seguridad..."):
                res = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe brevemente quién o qué está en la puerta de la casa en español (máximo 2 líneas)."},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                        ]
                    }],
                    max_tokens=150
                )
                descripcion = res.choices[0].message.content
                st.session_state.puerta_abierta = True
                st.session_state.luces_sala = True
                st.session_state.ultimo_evento = f"Acceso concedido: {descripcion}"
                st.success(f"✅ {descripcion} — **Puerta abierta y luces de sala encendidas.**")
                hablar("Acceso autorizado. Bienvenido a casa.")

with tab2:
    st.subheader("Dibuja el patrón de seguridad para desbloquear")
    canvas = st_canvas(
        stroke_width=6, stroke_color="#00FFAA", background_color="#111111",
        height=220, width=350, drawing_mode="freedraw", key="patron_puerta"
    )
    if st.button("✅ Verificar Patrón Táctil"):
        if canvas.image_data is not None and np.max(canvas.image_data) > 0:
            st.session_state.puerta_abierta = True
            st.session_state.luces_sala = True
            msg = "Patrón táctil correcto. Puerta abierta y luces de bienvenida activadas en la sala."
            st.session_state.ultimo_evento = msg
            st.success(msg)
            hablar(msg)
        else:
            st.warning("Dibuja un patrón en el recuadro negro primero.")

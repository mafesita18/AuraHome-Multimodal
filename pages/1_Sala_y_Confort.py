import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Ambiente 1: Sala y Confort", page_icon="🛋️", layout="centered")

if "luces_sala" not in st.session_state:
    st.session_state.luces_sala = False
    st.session_state.color_luz = "#FFD700"
    st.session_state.temperatura = 22
    st.session_state.puerta_abierta = False
    st.session_state.ultimo_evento = "Sistema listo."

def hablar(texto):
    tts = gTTS(text=texto, lang='es')
    tts.save("respuesta_casa.mp3")
    st.audio("respuesta_casa.mp3", format="audio/mp3", autoplay=True)

st.title("🛋️ Ambiente 1: Sala Inteligente y Confort")
st.markdown("Controla la iluminación y el ambiente del hogar mediante **comandos de voz**.")

# Visualización física simulada
color_caja = st.session_state.color_luz if st.session_state.luces_sala else "#1E1E1E"
texto_caja = "💡 ILUMINACIÓN ACTIVA" if st.session_state.luces_sala else "🌑 SALA A OSCURAS"

st.markdown(
    f"""
    <div style="background-color:{color_caja}; padding:30px; border-radius:15px; text-align:center; border: 2px solid #555;">
        <h2 style="color: {'#000' if st.session_state.luces_sala else '#FFF'}; margin:0;">{texto_caja}</h2>
        <p style="color: {'#222' if st.session_state.luces_sala else '#AAA'}; margin:5px 0 0 0;">Temperatura actual: {st.session_state.temperatura}°C</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.subheader("🎙️ Control por Voz")

audio_val = st.audio_input("Presiona el micrófono y di tu comando:")

col1, col2 = st.columns(2)

with col1:
    if st.button("💡 Ejecutar Comando de Voz", type="primary", use_container_width=True):
        if audio_val is not None:
            st.session_state.luces_sala = True
            st.session_state.color_luz = "#FFF4B8"
            respuesta = "Comando de voz recibido. Encendiendo iluminación de la sala."
            st.session_state.ultimo_evento = f"Voz en Sala: {respuesta}"
            st.success(respuesta)
            hablar(respuesta)
            st.rerun()
        else:
            st.warning("Graba primero un comando con el micrófono.")

with col2:
    if st.button("🌙 Comando: Modo Salir / Apagar", use_container_width=True):
        st.session_state.luces_sala = False
        st.session_state.puerta_abierta = False  # Comunicación bidireccional con Ambiente 2
        respuesta = "Apagando luces de la sala y cerrando la puerta principal."
        st.session_state.ultimo_evento = f"Sala: {respuesta}"
        st.info(respuesta)
        hablar(respuesta)
        st.rerun()
        

import streamlit as st
from textblob import TextBlob
from gtts import gTTS
import os

st.set_page_config(page_title="Ambiente 1: Sala y Confort", page_icon="🛋️", layout="centered")

# Asegurar variables si entran directo a esta página
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
st.markdown("Interactúa mediante **comandos de voz/texto** o deja que la casa detecte tu **estado de ánimo**.")

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
st.subheader("🎙️ Modalidad 1: Comando o Estado de Ánimo")

# Entrada de audio nativa de Streamlit o texto
audio_val = st.audio_input("Graba una nota de voz (opcional)")
comando = st.text_input("O escribe cómo te sientes / qué orden quieres dar:", placeholder="Ej: Llegué súper cansada / Apaga todo y cierra la casa")

if st.button("⚡ Ejecutar en Sala", type="primary"):
    if comando:
        cmd = comando.lower()
        analisis = TextBlob(comando)
        polaridad = analisis.sentiment.polarity

        if "apaga" in cmd or "dormir" in cmd or "salir" in cmd:
            st.session_state.luces_sala = False
            st.session_state.puerta_abierta = False  # Comunicación bidireccional al Ambiente 2
            respuesta = "Entendido. Apagando luces de la sala y asegurando la puerta principal."
        elif "enciende" in cmd or "prende" in cmd or "luz" in cmd:
            st.session_state.luces_sala = True
            st.session_state.color_luz = "#FFF4B8"
            respuesta = "Luces de la sala encendidas en modo estándar."
        elif polaridad < 0 or "cansad" in cmd or "estres" in cmd or "triste" in cmd:
            st.session_state.luces_sala = True
            st.session_state.color_luz = "#FFB6C1"  # Luz cálida relajante
            st.session_state.temperatura = 20
            respuesta = "Detecto que tuviste un día pesado. Activando iluminación cálida relajante y clima a 20 grados."
        else:
            st.session_state.luces_sala = True
            st.session_state.color_luz = "#87CEFA"
            respuesta = "Activando ambiente energético en la sala."

        st.session_state.ultimo_evento = f"Sala: {respuesta}"
        st.success(respuesta)
        hablar(respuesta)
        st.rerun()
    elif audio_val:
        st.session_state.luces_sala = True
        st.session_state.color_luz = "#DDA0DD"
        respuesta = "Comando de voz recibido. Activando escena ambiental en la sala."
        st.session_state.ultimo_evento = f"Voz en Sala: {respuesta}"
        st.success(respuesta)
        hablar(respuesta)

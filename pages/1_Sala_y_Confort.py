import streamlit as st
import speech_recognition as sr
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

def procesar_orden(orden):
    cmd = orden.lower()
    if "apaga" in cmd or "dormir" in cmd or "salir" in cmd or "cierra" in cmd:
        st.session_state.luces_sala = False
        st.session_state.puerta_abierta = False  # Comunicación bidireccional con Ambiente 2
        return "Entendido. Apagando luces de la sala y asegurando la puerta principal."
    elif "enciende" in cmd or "prende" in cmd or "luz" in cmd or "luces" in cmd:
        st.session_state.luces_sala = True
        st.session_state.color_luz = "#FFF4B8"
        return "Luces de la sala encendidas."
    elif "frío" in cmd or "frio" in cmd or "aire" in cmd or "calor" in cmd:
        st.session_state.temperatura = 19
        return "Ajustando el aire acondicionado de la sala a 19 grados."
    elif "cálida" in cmd or "calida" in cmd or "relaj" in cmd or "noche" in cmd:
        st.session_state.luces_sala = True
        st.session_state.color_luz = "#FFB6C1"
        return "Activando iluminación cálida en la sala."
    else:
        st.session_state.luces_sala = True
        st.session_state.color_luz = "#87CEFA"
        return f"Comando '{orden}' recibido. Ajustando ambiente de la sala."

st.title("🛋️ Ambiente 1: Sala Inteligente y Confort")
st.markdown("Controla la iluminación, el clima y el cierre general del hogar mediante **comandos de voz**.")

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
st.caption("Prueba decir comandos como: *'Enciende las luces'*, *'Pon luz cálida'*, *'Hace calor, prende el aire'* o *'Apaga todo y cierra la puerta'*.")

audio_val = st.audio_input("Presiona el micrófono y di tu comando:")

if audio_val is not None:
    if st.button("⚡ Ejecutar Comando de Voz", type="primary"):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio_val) as source:
                audio_data = recognizer.record(source)
                texto_reconocido = recognizer.recognize_google(audio_data, language="es-ES")
            
            st.info(f"🗣️ **Voz reconocida:** \"{texto_reconocido}\"")
            respuesta = procesar_orden(texto_reconocido)
            st.session_state.ultimo_evento = f"Voz en Sala: {respuesta}"
            st.success(respuesta)
            hablar(respuesta)
            st.rerun()
        except sr.UnknownValueError:
            st.warning("No se entendió bien el audio. Intenta hablar más claro cerca del micrófono.")
        except Exception as e:
            st.error(f"Error al procesar el audio: {e}")

import streamlit as st

st.set_page_config(page_title="AuraHome | Casa Inteligente Multimodal", page_icon="🏠", layout="wide")

# Inicializar estados compartidos de la casa (Simulación Física)
if "luces_sala" not in st.session_state:
    st.session_state.luces_sala = False
if "color_luz" not in st.session_state:
    st.session_state.color_luz = "#FFD700"
if "temperatura" not in st.session_state:
    st.session_state.temperatura = 22
if "puerta_abierta" not in st.session_state:
    st.session_state.puerta_abierta = False
if "ultimo_evento" not in st.session_state:
    st.session_state.ultimo_evento = "Sistema iniciado en espera."
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.title("🏠 AuraHome: Sistema Domótico Multimodal")
st.markdown("Control inteligente del hogar mediante **Comandos de Voz")

with st.sidebar:
    st.header("🏡 Ambientes")
    st.info("Usa el menú superior para navegar entre los **2 ambientes** de la casa.")

st.markdown("---")
st.subheader("📊 Estado en Tiempo Real de la Casa (Digital Twin)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    estado_luz = "ENCENDIDAS 💡" if st.session_state.luces_sala else "APAGADAS 🌑"
    st.metric("Ambiente 1: Luces Sala", estado_luz)

with col2:
    st.metric("Ambiente 1: Clima", f"{st.session_state.temperatura} °C ❄️")

with col3:
    estado_puerta = "DESBLOQUEADA 🔓" if st.session_state.puerta_abierta else "CERRADA 🔒"
    st.metric("Ambiente 2: Puerta Principal", estado_puerta)

with col4:
    st.color_picker("Tono de Ambiente", st.session_state.color_luz, disabled=True)

st.success(f"📡 **Última actualización bidireccional:** {st.session_state.ultimo_evento}")

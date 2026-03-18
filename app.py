import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
from supabase import create_client, Client

# ==========================================
# 1. CONEXIÓN REAL A SUPABASE (BÓVEDA)
# ==========================================
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Error Crítico: Configura SUPABASE_URL y SUPABASE_KEY en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 2. CONFIGURACIÓN E INTERFAZ NEÓN PROFESIONAL
# ==========================================
st.set_page_config(page_title="Dropshippingent | IA Analítica de Élite", page_icon="🤖", layout="wide")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = None
if 'idioma' not in st.session_state: st.session_state['idioma'] = 'Español'

st.markdown("""
<style>
body { background-color: #0e1117; }
.main-title { font-size: 3.5rem; font-weight: bold; color: #00FF9C; text-align: center; text-shadow: 0 0 20px #00FF9C; margin-bottom: 0px; }
.subtitle { text-align: center; color: #888; margin-bottom: 2rem; font-size: 1.2rem; }
.stButton>button { background: linear-gradient(135deg, #00FF9C, #0066FF); color: #000; font-weight: bold; border: none; border-radius: 8px; transition: 0.3s; width: 100%; height: 3em; }
.stButton>button:hover { background: linear-gradient(135deg, #0066FF, #00FF9C); transform: scale(1.02); }
section[data-testid="stSidebar"] { background-color: #1a1a2e; }
.stExpander { border: 1px solid #00FF9C33; border-radius: 8px; background-color: #161b22; }
.paywall-box { background-color: #1a1a2e; padding: 25px; border-radius: 12px; border: 2px solid; text-align: center; margin-top: 15px; }
.metric-card { background-color: #161b22; padding: 15px; border-radius: 10px; border

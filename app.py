import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
from supabase import create_client, Client

# ==========================================
# 1. CONEXIÓN REAL A SUPABASE
# ==========================================
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Configura SUPABASE_URL y SUPABASE_KEY en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 2. CONFIGURACIÓN E INTERFAZ NEÓN PROFESIONAL
# ==========================================
st.set_page_config(page_title="Dropshippingent | IA Analítica", page_icon="🤖", layout="wide")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = None
if 'idioma' not in st.session_state: st.session_state['idioma'] = 'Español'

# Estilos CSS - Corregidos para evitar errores de sintaxis
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE USUARIOS Y BASE DE DATOS
# ==========================================
def registrar_usuario(email, password):
    try:
        supabase.table("usuarios").insert({"email": email, "password": password, "role": "free"}).execute()
        return True
    except: return False

def login_usuario(email, password):
    try:
        res = supabase.table("usuarios").select("*").eq("email", email).eq("password", password).execute()
        return res.data[0] if res.data else None
    except: return None

def actualizar_uso(user_id, columna):
    try:
        nuevo_valor = st.session_state['user_data'][columna] + 1
        supabase.table("usuarios").update({columna: nuevo_valor}).eq("id", user_id).execute()
        st.session_state['user_data'][columna] = nuevo_valor
    except: pass

# ==========================================
# 4. MOTOR DE IA Y DICCIONARIO MULTILINGÜE
# ==========================================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def consultar_agente(sistema, prompt):
    lang = st.session_state['idioma']
    sistema_full = f"{sistema} Eres Dropshippingent, un motor analítico de élite enfocado en eCommerce y Dropshipping. Responde 100% en {lang}. Estilo profesional, directo y basado en datos."
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sistema_full}, {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

traducciones = {
    "Español": {
        "sub": "Análisis de Mercado y Dropshipping Potenciado por IA.",
        "desc": "El ecosistema analítico definitivo para emprendedores. Encuentra productos ganadores, calcula rentabilidad exacta y domina tu nicho sin tocar inventario.",
        "t1": "🎯 ¿Para quién está diseñado Dropshippingent?",
        "d1": "Nuestros algoritmos resuelven los problemas de 3 perfiles clave:",
        "p1_t": "🛒 Dropshippers", "p1_d": "Deja de adivinar qué vender. Analiza tendencias y márgenes antes de gastar en Ads.",
        "p2_t": "📦 Vendedores Amazon", "p2_d": "Automatiza tu Amazon A+ y conoce tu punto de equilibrio exacto.",
        "p3_t": "🧠 Estrategas", "p3_d": "Espía reseñas negativas y detecta brechas de mercado para ofertas irresistibles.",
        "t2": "⚡ Arsenal Analítico",
        "pw_limit": "🔒 Límite alcanzado. ¡Desbloquea el poder PRO!",
        "pw_unlock": "### 🚀 Pásate al siguiente nivel",
        "pw_plan_t": "Plan Emprendedor", "pw_plan_b": "Suscribirse"
    },
    "English": {
        "sub": "Market Analysis and Dropshipping Powered by AI.",
        "desc": "The ultimate analytical ecosystem for entrepreneurs. Find winning products, calculate exact profitability, and dominate your niche.",
        "t1": "🎯 Who is Dropshippingent designed for?",
        "d1": "Our algorithms solve the problems of 3 key profiles:",
        "p1_t": "🛒 Dropshippers", "p1_d": "Stop guessing what to sell. Analyze trends and margins before spending on Ads.",
        "p2_t": "📦 Amazon Sellers", "p2_d": "Automate your Amazon A+ and know your exact break-even point.",
        "p3_t": "🧠 Strategists", "p3_d": "Spy on negative reviews and detect market gaps for irresistible offers.",
        "t2": "⚡ Analytical Arsenal",
        "pw_limit": "🔒 Limit reached. Unlock PRO power!",
        "pw_unlock": "### 🚀 Move to the next level",
        "pw_plan_t": "Entrepreneur Plan", "pw_plan_b": "Subscribe"
    },
    "Português": {
        "sub": "Análise de Mercado e Dropshipping com IA.",
        "desc": "O ecossistema analítico definitivo para empreendedores. Encontre produtos vencedores e domine seu nicho.",
        "t1": "🎯 Para quem foi desenhado?",
        "d1": "Nossos algoritmos resolvem problemas de 3 perfis principais:",
        "p1_t": "🛒 Dropshippers", "p1_d": "Pare de adivinhar o que vender. Analise tendências antes de gastar em Ads.",
        "p2_t": "📦 Vendedores Amazon", "p2_d": "Automatize seu Amazon A+ e conheça seu ponto de equilíbrio.",
        "p3_t": "🧠 Estrategistas", "p3_d": "Espione avaliações negativas e detecte lacunas de mercado.",
        "t2": "⚡ Arsenal Analítico",
        "pw_limit": "🔒 Limite atingido. Desbloqueie o poder PRO!",
        "pw_unlock": "### 🚀 Vá para o próximo nível",
        "pw_plan_t": "Plano Empreendedor", "pw_plan_b": "Assinar"
    }
}

def mostrar_paywall():
    t = traducciones[st.session_state['idioma']]
    st.markdown("---")
    st.error(t['pw_

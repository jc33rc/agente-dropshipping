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
# 2. CONFIGURACIÓN E INTERFAZ NEÓN
# ==========================================
st.set_page_config(page_title="Dropshippingent | IA Analítica", page_icon="🤖", layout="wide")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = None
if 'idioma' not in st.session_state: st.session_state['idioma'] = 'Español'

st.markdown("""
<style>
body { background-color: #0e1117; }
.main-title { font-size: 3.5rem; font-weight: bold; color: #00FF9C; text-align: center; text-shadow: 0 0 20px #00FF9C; margin-bottom: 0px; }
.subtitle { text-align: center; color: #888; margin-bottom: 2rem; font-size: 1.2rem; }
.stButton>button { background: linear-gradient(135deg, #00FF9C, #0066FF); color: #000; font-weight: bold; border: none; border-radius: 8px; transition: 0.3s; }
.stButton>button:hover { background: linear-gradient(135deg, #0066FF, #00FF9C); transform: scale(1.02); }
section[data-testid="stSidebar"] { background-color: #1a1a2e; }
.paywall-box { background-color: #1a1a2e; padding: 25px; border-radius: 12px; border: 2px solid; text-align: center; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE USUARIOS (DATABASE)
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
# 4. MOTOR DE IA Y TRADUCCIONES
# ==========================================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def consultar_agente(sistema, prompt):
    lang = st.session_state['idioma']
    sistema_full = f"{sistema} Eres Dropshippingent. Responde 100% en {lang}."
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": sistema_full}, {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

traducciones = {
    "Español": {
        "sub": "Análisis de Mercado y Dropshipping Potenciado por IA.",
        "desc": "El ecosistema analítico definitivo para emprendedores. Encuentra productos ganadores y domina tu nicho.",
        "t1": "🎯 ¿Para quién está diseñado?",
        "p1_t": "🛒 Dropshippers", "p2_t": "📦 Vendedores Amazon", "p3_t": "🧠 Estrategas",
        "pw_limit": "🔒 Límite Freemium alcanzado.",
        "pw_unlock": "### 🚀 Desbloquea el Ecosistema Completo",
        "pw_plan_t": "Plan Emprendedor", "pw_plan_b": "Suscribirse"
    },
    "English": {
        "sub": "Market Analysis and Dropshipping Powered by AI.",
        "desc": "The ultimate analytical ecosystem for entrepreneurs. Find winning products and dominate your niche.",
        "t1": "🎯 Who is it designed for?",
        "p1_t": "🛒 Dropshippers", "p2_t": "📦 Amazon Sellers", "p3_t": "🧠 Strategists",
        "pw_limit": "🔒 Freemium limit reached.",
        "pw_unlock": "### 🚀 Unlock the Complete Ecosystem",
        "pw_plan_t": "Entrepreneur Plan", "pw_plan_b": "Subscribe"
    },
    "Português": {
        "sub": "Análise de Mercado e Dropshipping com IA.",
        "desc": "O ecossistema analítico definitivo para empreendedores. Encontre produtos vencedores e domine seu nicho.",
        "t1": "🎯 Para quem foi desenhado?",
        "p1_t": "🛒 Dropshippers", "p2_t": "📦 Vendedores Amazon", "p3_t": "🧠 Estrategistas",
        "pw_limit": "🔒 Limite Freemium atingido.",
        "pw_unlock": "### 🚀 Desbloqueie o Ecossistema Completo",
        "pw_plan_t": "Plano Empreendedor", "pw_plan_b": "Assinar"
    }
}

def mostrar_paywall():
    t = traducciones[st.session_state['idioma']]
    st.error(t['pw_limit'])
    st.markdown(t['pw_unlock'])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='paywall-box' style='border-color: #00FF9C;'><h3>{t['pw_plan_t']}</h3><h1>$19</h1><button style='width:100%;'>{t['pw_plan_b']}</button></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='paywall-box' style='border-color: #FFD700;'><h3>Oferta Fundador</h3><h1>$99</h1><button style='width:100%;'>Ser Fundador</button></div>", unsafe_allow_html=True)

# ==========================================
# 5. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00FF9C;'>Dropshippingent</h2>", unsafe_allow_html=True)
    st.session_state['idioma'] = st.selectbox("🌐 Language:", ["Español", "English", "Português"])
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        tab_log, tab_reg = st.tabs(["🔐 Login", "🚀 Registro"])
        with tab_log:
            le = st.text_input("Email", key="l_e")
            lp = st.text_input("Password", type="password", key="l_p")
            if st.button("Entrar", use_container_width=True):
                u = login_usuario(le, lp)
                if u:
                    st.session_state.update({'logged_in': True, 'user_data': u})
                    st.rerun()
                else: st.error("Datos incorrectos")
        with tab_reg:
            re = st.text_input("Email Nuevo", key="r_e")
            rp = st.text_input("Password Nueva", type="password", key="r_p")
            if st.button("Crear Cuenta", use_container_width=True):
                if registrar_usuario(re, rp): st.success("¡Registrado! Ya puedes loguearte.")
                else: st.error("El usuario ya existe.")
    else:
        st.success(f"Sesión: {st.session_state['user_data']['email']}")
        st.caption(f"Plan: {st.session_state['user_data']['role'].upper()}")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.update({'logged_in': False, 'user_data': None})
            st.rerun()
        st.markdown("---")
        modulo = st.radio("Arsenal Analítico:", ["1. Investigar Productos", "2. Monitor de Precios", "3. Amazon A+", "4. Redes Sociales", "5. Proveedores", "6. Rentabilidad"])

# ==========================================
# 6. PANTALLA PRINCIPAL
# ==========================================
t = traducciones[st.session_state['idioma']]

if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-title'>Dropshippingent</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{t['sub']}</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; color:#E0E0E0;'>{t['desc']}</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.header(t['t1'])
    c1, c2, c3 = st.columns(3)
    c1.subheader(t['p1_t']); c1.write("Análisis de tendencias con IA.")
    c2.subheader(t['p2_t']); c2.write("Copywriting A+ optimizado.")
    c3.subheader(t['p3_t']); c3.write("Detección de brechas de mercado.")
else:
    user = st.session_state['user_data']
    is_free = user['role'] == 'free'
    st.header(f"🛠️ {modulo}")

    if "1. Investigar" in modulo:
        nicho = st.text_input("Nicho (ej: belleza)")
        if is_free and user['uso_m1_m2'] >= 4: mostrar_paywall()
        elif st.button("Analizar"):
            actualizar_uso(user['id'], 'uso_m1_m2')
            with st.spinner("IA analizando..."):
                st.write(consultar_agente("Analista de mercado.", nicho))

    elif "6. Rentabilidad" in modulo:
        col1, col2 = st.columns(2)
        with col1: pv = st.number_input("Precio Venta", value=20.0)
        with col2: cp = st.number_input("Costo Producto", value=7.0)
        if is_free and user['uso_m6'] >= 1: mostrar_paywall()
        elif st.button("Ver Gráfico"):
            actualizar_uso(user['id'], 'uso_m6')
            fig = px.pie(values=[cp, pv-cp], names=["Costo", "Margen"], template="plotly_dark")
            st.plotly_chart(fig)

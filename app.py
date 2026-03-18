import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
from supabase import create_client, Client

# ==========================================
# 1. CONEXIÓN A BASE DE DATOS (SUPABASE)
# ==========================================
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("⚠️ Error: Configura SUPABASE_URL y SUPABASE_KEY en los Secrets de Streamlit.")
    st.stop()

# ==========================================
# 2. CONFIGURACIÓN E INTERFAZ PROFESIONAL
# ==========================================
st.set_page_config(page_title="Dropshippingent | IA Analítica", page_icon="🤖", layout="wide")

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_data' not in st.session_state: st.session_state['user_data'] = None
if 'idioma' not in st.session_state: st.session_state['idioma'] = 'Español'

# Estilos CSS Neón (Sin recortes)
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
# 3. FUNCIONES DE BASE DE DATOS
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
        "desc": "El ecosistema analítico definitivo para emprendedores. Encuentra productos ganadores, calcula rentabilidad exacta y domina tu nicho sin tocar inventario.",
        "t1": "🎯 ¿Para quién está diseñado Dropshippingent?",
        "d1": "Nuestros algoritmos están entrenados específicamente para resolver los problemas de 3 perfiles clave:",
        "p1_t": "🛒 Dropshippers y Emprendedores",
        "p1_d": "Deja de adivinar qué vender. Usa nuestra IA para analizar tendencias, encontrar productos validados y conocer tu margen de ganancia antes de gastar un solo dólar en Ads.",
        "p2_t": "📦 Vendedores Amazon / Shopify",
        "p2_d": "Automatiza tu copywriting de élite (estructuras Amazon A+) y calcula el impacto de las comisiones para conocer tu punto de equilibrio exacto.",
        "p3_t": "🧠 Estrategas de Marcas Propias",
        "p3_d": "Espía las reseñas negativas de tu competencia. Deja que la IA detecte brechas de mercado y te entregue la estrategia exacta para crear ofertas irresistibles.",
        "t2": "⚡ El Arsenal Analítico a tu Disposición",
        "a1_t": "⏱️ Análisis en Segundos", "a1_d": "Pasa de horas de investigación manual a un escaneo profundo en 10 segundos.",
        "a2_t": "📊 Gráficos de Rentabilidad", "a2_d": "Visualiza tu Break-Even Point. El sistema cruza costos y comisiones proyectando ganancias.",
        "a3_t": "🛡️ Score de Validación IA", "a3_d": "Obtén un puntaje de riesgo de 0 a 100 evaluando saturación y márgenes.",
        "pw_limit": "🔒 Límite Freemium alcanzado.",
        "pw_unlock": "### 🚀 Desbloquea el Ecosistema Analítico Completo",
        "pw_plan_t": "Plan Emprendedor", "pw_plan_p": "$19 / mes", "pw_plan_d": "Acceso ilimitado a todos los módulos IA.",
        "pw_plan_b": "Suscribirse", "pw_found_t": "Oferta Fundador", "pw_found_p": "$99 Único",
        "pw_found_d": "Acceso Vitalicio. 🔥 Solo 12 cupos disponibles.", "pw_found_b": "Ser Fundador"
    },
    "English": {
        "sub": "Market Analysis and Dropshipping Powered by AI.",
        "desc": "The ultimate analytical ecosystem for entrepreneurs. Find winning products and dominate your niche.",
        "t1": "🎯 Who is Dropshippingent designed for?",
        "d1": "Our algorithms solve the problems of 3 key profiles:",
        "p1_t": "🛒 Dropshippers", "p1_d": "Stop guessing what to sell. Analyze trends and margins before spending on Ads.",
        "p2_t": "📦 Amazon Sellers", "p2_d": "Automate your elite copywriting and calculate your exact break-even point.",
        "p3_t": "🧠 Strategists", "p3_d": "Spy on negative reviews and detect market gaps for irresistible offers.",
        "t2": "⚡ Analytical Arsenal",
        "a1_t": "⏱️ Quick Analysis", "a1_d": "Go from hours of research to a deep scan in 10 seconds.",
        "a2_t": "📊 Profit Charts", "a2_d": "Visualize your Break-Even Point and project real profits.",
        "a3_t": "🛡️ AI Risk Score", "a3_d": "Get a risk score from 0 to 100 evaluating saturation and margins.",
        "pw_limit": "🔒 Freemium limit reached.",
        "pw_unlock": "### 🚀 Unlock the Complete Analytical Ecosystem",
        "pw_plan_t": "Entrepreneur Plan", "pw_plan_p": "$19 / month", "pw_plan_d": "Unlimited access to all AI modules.",
        "pw_plan_b": "Subscribe", "pw_found_t": "Founder Offer", "pw_found_p": "$99 One-time",
        "pw_found_d": "Lifetime Access. 🔥 Only 12 spots left.", "pw_found_b": "Become a Founder"
    },
    "Português": {
        "sub": "Análise de Mercado e Dropshipping com IA.",
        "desc": "O ecossistema analítico definitivo para empreendedores. Encontre produtos vencedores e domine seu nicho.",
        "t1": "🎯 Para quem é o Dropshippingent?",
        "d1": "Nossos algoritmos resolvem os problemas de 3 perfis principais:",
        "p1_t": "🛒 Dropshippers", "p1_d": "Pare de adivinhar o que vender. Analise tendências antes de gastar em Ads.",
        "p2_t": "📦 Vendedores Amazon", "p2_d": "Automatize seu copywriting e conheça seu ponto de equilíbrio exato.",
        "p3_t": "🧠 Estrategistas", "p3_d": "Espione avaliações negativas e detecte lacunas de mercado.",
        "t2": "⚡ Arsenal Analítico",
        "a1_t": "⏱️ Análise Rápida", "a1_d": "De horas de pesquisa para uma varredura profunda em 10 segundos.",
        "a2_t": "📊 Gráficos de Lucro", "a2_d": "Visualize seu ponto de equilíbrio e projete lucros reais.",
        "a3_t": "🛡️ Score de Risco", "a3_d": "Obtenha uma pontuação de risco de 0 a 100.",
        "pw_limit": "🔒 Limite atingido.",
        "pw_unlock": "### 🚀 Desbloqueie o Ecossistema Completo",
        "pw_plan_t": "Plano Empreendedor", "pw_plan_p": "$19 / mês", "pw_plan_d": "Acesso ilimitado.",
        "pw_plan_b": "Assinar", "pw_found_t": "Oferta Fundador", "pw_found_p": "$99 Único",
        "pw_found_d": "Acesso Vitalício. 🔥 Apenas 12 vagas.", "pw_found_b": "Ser Fundador"
    }
}

def mostrar_paywall():
    t = traducciones[st.session_state['idioma']]
    st.markdown("---")
    st.error(t['pw_limit'])
    st.markdown(t['pw_unlock'])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='paywall-box' style='border-color: #00FF9C;'><h3>{t['pw_plan_t']}</h3><h1>{t['pw_plan_p']}</h1><p>{t['pw_plan_d']}</p></div>", unsafe_allow_html=True)
        if st.button("Suscribirse Plan Mensual"): st.write("Redirigiendo...")
    with col2:
        st.markdown(f"<div class='paywall-box' style='border-color: #FFD700;'><h3>{t['pw_found_t']}</h3><h1>{t['pw_found_p']}</h1><p>{t['pw_found_d']}</p></div>", unsafe_allow_html=True)
        if st.button("Obtener Acceso Vitalicio"): st.write("Redirigiendo...")

# ==========================================
# 5. BARRA LATERAL (GESTIÓN DE ACCESO)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=60)
    st.markdown("<h2 style='text-align: center; color: #00FF9C;'>Dropshippingent</h2>", unsafe_allow_html=True)
    st.session_state['idioma'] = st.selectbox("🌐 Idioma / Language:", ["Español", "English", "Português"])
    st.markdown("---")
    
    if not st.session_state['logged_in']:
        t_log, t_reg = st.tabs(["🔐 Iniciar Sesión", "🚀 Crear Cuenta"])
        with t_log:
            le = st.text_input("Email", key="l_e")
            lp = st.text_input("Password", type="password", key="l_p")
            if st.button("Entrar", use_container_width=True):
                u = login_usuario(le, lp)
                if u:
                    st.session_state.update({'logged_in': True, 'user_data': u})
                    st.rerun()
                else: st.error("Credenciales incorrectas")
        with t_reg:
            re = st.text_input("Tu mejor Email", key="r_e")
            rp = st.text_input("Crea Password (mín 6)", type="password", key="r_p")
            if st.button("Registrarme Gratis", use_container_width=True):
                if "@" not in re: st.error("Email inválido")
                elif len(rp) < 6: st.warning("Mínimo 6 caracteres")
                elif registrar_usuario(re, rp): st.success("¡Registrado! Inicia sesión.")
                else: st.error("El usuario ya existe.")
    else:
        st.success(f"Sesión: {st.session_state['user_data']['email']}")
        st.caption(f"Plan: {st.session_state['user_data']['role'].upper()}")
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.update({'logged_in': False, 'user_data': None})
            st.rerun()
        st.markdown("---")
        modulo = st.radio("Arsenal Analítico:", [
            "1. Investigar Productos (Free)", "2. Monitor de Precios (Free)", "3. Amazon A+ (Pro)", 
            "4. Redes Sociales (Pro)", "5. Contacto Proveedor (Pro)", "6. Análisis Rentabilidad (Pro)", 
            "7. Monitor Competencia (Pro)", "8. Score Validación (Pro)"
        ])

# ==========================================
# 6. PANTALLA PRINCIPAL: LANDING Y MÓDULOS
# ==========================================
t = traducciones[st.session_state['idioma']]

if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-title'>Dropshippingent</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{t['sub']}</p>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center; color:#E0E0E0; font-weight:normal;'>{t['desc']}</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.header(t['t1'])
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"<h4 style='color:#00FF9C;'>{t['p1_t']}</h4>", unsafe_allow_html=True); st.write(t['p1_d'])
    with col_b:
        st.markdown(f"<h4 style='color:#00FF9C;'>{t['p2_t']}</h4>", unsafe_allow_html=True); st.write(t['p2_d'])
    with col_c:
        st.markdown(f"<h4 style='color:#00FF9C;'>{t['p3_t']}</h4>", unsafe_allow_html=True); st.write(t['p3_d'])
    st.markdown("---")
    st.header(t['t2'])
    c1, c2, c3 = st.columns(3)
    with c1: st.subheader(t['a1_t']); st.write(t['a1_d'])
    with c2: st.subheader(t['a2_t']); st.write(t['a2_d'])
    with c3: st.subheader(t['a3_t']); st.write(t['a3_d'])
    st.markdown("---")
    st.info("👈 **Regístrate en la barra lateral** para iniciar sesión y acceder a los módulos.")

else:
    user = st.session_state['user_data']
    is_free = user['role'] == 'free'
    st.header(f"🛠️ {modulo}")

    if "1. Investigar" in modulo:
        nicho = st.text_input("Nicho (ej: belleza)")
        if is_free and user['uso_m1_m2'] >= 4: mostrar_paywall()
        elif st.button("Investigar ahora"):
            actualizar_uso(user['id'], 'uso_m1_m2')
            with st.spinner("Analizando mercado..."):
                st.write(consultar_agente("Analista de nichos ganadores.", nicho))

    elif "2. Monitor" in modulo:
        prod = st.text_input("Producto")
        if is_free and user['uso_m1_m2'] >= 4: mostrar_paywall()
        elif st.button("Analizar Precios"):
            actualizar_uso(user['id'], 'uso_m1_m2')
            with st.spinner("Calculando..."):
                st.write(consultar_agente("Experto en pricing.", prod))

    elif "3. Amazon A+" in modulo:
        det = st.text_area("Detalles del producto")
        if is_free and user['uso_m3'] >= 1: mostrar_paywall()
        elif st.button("Generar Copywriting"):
            actualizar_uso(user['id'], 'uso_m3')
            st.write(consultar_agente("Copywriter Amazon A+.", det))

    elif "4. Redes Sociales" in modulo:
        item = st.text_input("Producto")
        if is_free and user['uso_m4'] >= 1: mostrar_paywall()
        elif st.button("Crear Estrategia 5 Días"):
            actualizar_uso(user['id'], 'uso_m4')
            st.write(consultar_agente("Estratega viral.", item))

    elif "5. Proveedores" in modulo:
        obj = st.text_input("¿Qué quieres negociar?")
        if is_free and user['uso_m5'] >= 1: mostrar_paywall()
        elif st.button("Generar Mensaje"):
            actualizar_uso(user['id'], 'uso_m5')
            st.write(consultar_agente("Negociador B2B.", obj))

    elif "6. Rentabilidad" in modulo:
        pv = st.number_input("Precio Venta ($)", value=25.0)
        cp = st.number_input("Costo Producto ($)", value=10.0)
        if is_free and user['uso_m6'] >= 1: mostrar_paywall()
        elif st.button("Generar Gráfico"):
            actualizar_uso(user['id'], 'uso_m6')
            st.plotly_chart(px.pie(values=[cp, pv-cp], names=["Costo", "Margen"], template="plotly_dark"))

    elif "7. Competencia" in modulo:
        rev = st.text_area("Pega reseñas negativas de tu competencia")
        if is_free and user['uso_m7'] >= 1: mostrar_paywall()
        elif st.button("Detectar Brechas"):
            actualizar_uso(user['id'], 'uso_m7')
            st.write(consultar_agente("Estratega competitivo.", rev))

    elif "8. Score Validación" in modulo:
        m = st.slider("Margen %", 0, 100, 30)
        if is_free and user['uso_m8'] >= 1: mostrar_paywall()
        elif st.button("Calcular Score"):
            actualizar_uso(user['id'], 'uso_m8')
            s = (m * 0.8) + 20
            st.metric("Product Score", f"{s}/100")
            st.write(consultar_agente("Analista de riesgo.", f"Score {s}"))

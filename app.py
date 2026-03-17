import streamlit as st
from groq import Groq

st.set_page_config(page_title="Agente Dropshipping IA", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main-title { font-size: 2.5rem; font-weight: bold; color: #1F4E79; text-align: center; }
.subtitle { text-align: center; color: #666; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Agente Dropshipping IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu asistente inteligente para dropshipping sin inventario</p>", unsafe_allow_html=True)

api_key = st.sidebar.text_input("API Key de Groq", type="password", placeholder="Pega tu API Key aqui")

if not api_key:
    st.warning("Pega tu API Key de Groq en el panel izquierdo para comenzar")
    st.stop()

client = Groq(api_key=api_key)

def consultar_agente(sistema, prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

modulo = st.sidebar.selectbox("Selecciona un modulo", [
    "Investigar Productos",
    "Generar Descripcion Amazon",
    "Contenido para Redes Sociales",
    "Monitor de Precios",
    "Contactar Proveedor"
])

if modulo == "Investigar Productos":
    st.header("Investigar Productos Ganadores")
    col1, col2, col3 = st.columns(3)
    with col1:
        nicho = st.text_input("Nicho", placeholder="belleza facial")
    with col2:
        presupuesto = st.selectbox("Presupuesto", ["bajo", "medio", "alto"])
    with col3:
        plataforma = st.selectbox("Plataforma", ["Amazon", "AliExpress", "Ambas"])
    if st.button("Investigar ahora", type="primary"):
        with st.spinner("Analizando mercado..."):
            prompt = f"""
            Analiza este nicho para dropshipping sin inventario:
            NICHO: {nicho}, PRESUPUESTO: {presupuesto}, PLATAFORMA: {plataforma}
            Dame: TOP 5 productos ganadores con precio venta, precio compra AliExpress,
            margen % y competencia. Analisis del nicho y estrategia recomendada.
            """
            resultado = consultar_agente("Eres experto en dropshipping para el mercado latinoamericano.", prompt)
            st.success("Analisis completado!")
            st.markdown(resultado)

elif modulo == "Generar Descripcion Amazon":
    st.header("Generar Descripcion para Amazon")
    producto = st.text_input("Nombre del producto", placeholder="Mascarilla carbon activado")
    precio = st.text_input("Precio de venta", placeholder="$12.99")
    caracteristicas = st.text_area("Caracteristicas", placeholder="elimina impurezas, apta para todo tipo de piel...")
    if st.button("Generar descripcion", type="primary"):
        with st.spinner("Generando descripcion optimizada..."):
            prompt = f"""
            Crea descripcion completa optimizada para Amazon:
            PRODUCTO: {producto}, PRECIO: {precio}, CARACTERISTICAS: {caracteristicas}
            Dame: titulo optimizado max 200 caracteres, 5 bullet points persuasivos,
            descripcion larga 150-200 palabras con SEO, keywords backend y categoria.
            """
            resultado = consultar_agente("Eres experto en copywriting y SEO para Amazon en español.", prompt)
            st.success("Descripcion generada!")
            st.markdown(resultado)

elif modulo == "Contenido para Redes Sociales":
    st.header("Crear Contenido para Redes Sociales")
    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Producto", placeholder="Mascarilla carbon activado")
        nicho = st.text_input("Nicho", placeholder="belleza facial")
    with col2:
        plataforma = st.multiselect("Plataformas", ["Instagram", "TikTok", "Facebook"], default=["Instagram", "TikTok"])
    if st.button("Crear contenido", type="primary"):
        with st.spinner("Creando estrategia de contenido..."):
            prompt = f"""
            Crea estrategia completa de contenido organico:
            PRODUCTO: {producto}, NICHO: {nicho}, PLATAFORMAS: {plataforma}
            Dame: post Instagram con caption y 30 hashtags organizados,
            script TikTok 30-60 segundos, calendario 7 dias y estrategia crecimiento.
            """
            resultado = consultar_agente("Eres experto en marketing digital para ecommerce latinoamericano.", prompt)
            st.success("Contenido creado!")
            st.markdown(resultado)

elif modulo == "Monitor de Precios":
    st.header("Monitor de Precios y Rentabilidad")
    col1, col2, col3 = st.columns(3)
    with col1:
        producto = st.text_input("Producto", placeholder="Mascarilla carbon activado")
    with col2:
        precio_actual = st.text_input("Mi precio de venta", placeholder="$12.99")
    with col3:
        categoria = st.text_input("Categoria", placeholder="belleza facial")
    if st.button("Analizar rentabilidad", type="primary"):
        with st.spinner("Calculando rentabilidad..."):
            prompt = f"""
            Analiza precios y rentabilidad para dropshipping sin inventario:
            PRODUCTO: {producto}, MI PRECIO: {precio_actual}, CATEGORIA: {categoria}
            Dame: rango precios tipico, precio optimo, calculo rentabilidad con
            ganancia neta y ventas para $500/mes, estrategia y alertas.
            """
            resultado = consultar_agente("Eres experto en pricing para dropshipping en Amazon.", prompt)
            st.success("Analisis completado!")
            st.markdown(resultado)

elif modulo == "Contactar Proveedor":
    st.header("Contactar Proveedor en AliExpress")
    st.info("En dropshipping sin inventario solo contactas al proveedor para verificar calidad. Los pedidos reales los gestiona DSers automaticamente.")
    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Producto", placeholder="Mascarilla carbon activado")
        proveedor = st.selectbox("Proveedor", ["AliExpress", "CJdropshipping", "Zendrop"])
    with col2:
        objetivo = st.selectbox("Objetivo", [
            "Pedir muestra para verificar calidad",
            "Consultar tiempo de envio",
            "Negociar precio por volumen futuro",
            "Verificar politica de devoluciones"
        ])
    if st.button("Generar mensaje", type="primary"):
        with st.spinner("Redactando mensaje profesional..."):
            prompt = f"""
            Redacta mensaje profesional en INGLES para proveedor de {proveedor}.
            PRODUCTO: {producto}, OBJETIVO: {objetivo}
            MODELO: dropshipping sin inventario, compro solo cuando tengo cliente.
            El mensaje debe ser en INGLES, profesional, maximo 150 palabras.
            Luego dame en español: traduccion, 3 consejos para negociar
            y 3 senales de alerta de proveedor no confiable.
            """
            resultado = consultar_agente("Eres experto en comunicacion con proveedores. SIEMPRE escribe el mensaje en INGLES primero.", prompt)
            st.success("Mensaje generado!")
            st.markdown(resultado)

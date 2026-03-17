import streamlit as st
from groq import Groq
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Agente Dropshipping IA", page_icon="🤖", layout="wide")

st.markdown("""
<style>
body { background-color: #0e1117; }
.main-title { font-size: 2.5rem; font-weight: bold; color: #00FF9C; text-align: center; text-shadow: 0 0 20px #00FF9C; }
.subtitle { text-align: center; color: #888; margin-bottom: 2rem; }
.stButton>button { background: linear-gradient(135deg, #00FF9C, #0066FF); color: #000; font-weight: bold; border: none; border-radius: 8px; }
.stButton>button:hover { background: linear-gradient(135deg, #0066FF, #00FF9C); transform: scale(1.02); }
section[data-testid="stSidebar"] { background-color: #1a1a2e; }
.stExpander { border: 1px solid #00FF9C33; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Agente Dropshipping IA</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu asistente inteligente para dropshipping sin inventario</p>", unsafe_allow_html=True)

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = st.sidebar.text_input("API Key de Groq", type="password")
    if not api_key:
        st.warning("Pega tu API Key de Groq en el panel izquierdo")
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
    "Contactar Proveedor",
    "Analisis de Rentabilidad",
    "Monitor de Competencia",
    "Score de Validacion"
])

# MODULO 1
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

# MODULO 2 — COPYWRITING DE ELITE
elif modulo == "Generar Descripcion Amazon":
    st.header("Copywriting de Elite para Amazon")
    producto = st.text_input("Nombre del producto", placeholder="Mascarilla carbon activado")
    precio = st.text_input("Precio de venta", placeholder="$12.99")
    caracteristicas = st.text_area("Caracteristicas", placeholder="elimina impurezas, apta para todo tipo de piel...")
    tono = st.selectbox("Tono de escritura", ["Persuasivo", "Profesional", "Storytelling"])

    if st.button("Generar descripcion de elite", type="primary"):
        with st.spinner("Generando contenido A+ ..."):
            prompt = f"""
            Crea una descripcion LARGA y COMPLETA para Amazon A+ Content.
            PRODUCTO: {producto}
            PRECIO: {precio}
            CARACTERISTICAS: {caracteristicas}
            TONO: {tono}

            Estructura OBLIGATORIA (minimo 1500 caracteres en total):

            1. TITULO OPTIMIZADO SEO (maximo 200 caracteres con keywords principales)

            2. GANCHO PODEROSO (2-3 oraciones que capturen atencion inmediata)

            3. PROBLEMA Y SOLUCION (describe el problema del cliente y como este producto lo resuelve)

            4. BENEFICIOS DETALLADOS (5 bullet points extensos, minimo 3 lineas cada uno)

            5. DESCRIPCION LARGA A+ (minimo 500 palabras, narrativa persuasiva con SEO natural)

            6. CALL TO ACTION (CTA poderoso que genere urgencia)

            7. KEYWORDS BACKEND (50 palabras clave separadas por espacios)

            8. CATEGORIA RECOMENDADA en Amazon
            """
            resultado = consultar_agente(
                f"Eres el mejor copywriter de Amazon con tono {tono}. Escribes en español. Superas siempre los 1500 caracteres.",
                prompt
            )
            st.success("Descripcion A+ generada!")
            with st.expander("Ver descripcion completa", expanded=True):
                st.markdown(resultado)
            st.download_button("Descargar descripcion", resultado, file_name=f"descripcion_{producto}.txt")

# MODULO 3
elif modulo == "Contenido para Redes Sociales":
    st.header("Crear Contenido para Redes Sociales")
    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Producto", placeholder="Mascarilla carbon activado")
        nicho = st.text_input("Nicho", placeholder="belleza facial")
    with col2:
        plataforma = st.multiselect("Plataformas", ["Instagram", "TikTok", "Facebook"], default=["Instagram", "TikTok"])
    if st.button("Crear contenido", type="primary"):
        with st.spinner("Creando estrategia..."):
            prompt = f"""
            Crea estrategia completa de contenido organico:
            PRODUCTO: {producto}, NICHO: {nicho}, PLATAFORMAS: {plataforma}
            Dame: post Instagram con caption y 30 hashtags organizados,
            script TikTok 30-60 segundos, calendario 7 dias y estrategia crecimiento.
            """
            resultado = consultar_agente("Eres experto en marketing digital para ecommerce latinoamericano.", prompt)
            st.success("Contenido creado!")
            st.markdown(resultado)

# MODULO 4
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
        with st.spinner("Calculando..."):
            prompt = f"""
            Analiza precios y rentabilidad para dropshipping sin inventario:
            PRODUCTO: {producto}, MI PRECIO: {precio_actual}, CATEGORIA: {categoria}
            Dame: rango precios tipico, precio optimo, calculo rentabilidad,
            ganancia neta y ventas para $500/mes, estrategia y alertas.
            """
            resultado = consultar_agente("Eres experto en pricing para dropshipping en Amazon.", prompt)
            st.success("Analisis completado!")
            st.markdown(resultado)

# MODULO 5
elif modulo == "Contactar Proveedor":
    st.header("Contactar Proveedor")
    st.info("Solo contactas al proveedor para verificar calidad. DSers gestiona los pedidos automaticamente.")
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
        with st.spinner("Redactando..."):
            prompt = f"""
            Redacta mensaje profesional en INGLES para proveedor de {proveedor}.
            PRODUCTO: {producto}, OBJETIVO: {objetivo}
            MODELO: dropshipping sin inventario.
            Mensaje en INGLES maximo 150 palabras.
            Luego en español: traduccion, 3 consejos negociacion y 3 senales de alerta.
            """
            resultado = consultar_agente("Eres experto en comunicacion con proveedores. SIEMPRE escribe en INGLES primero.", prompt)
            st.success("Mensaje generado!")
            st.markdown(resultado)

# MODULO 6 — ANALISIS DE RENTABILIDAD CON GRAFICOS
elif modulo == "Analisis de Rentabilidad":
    st.header("Analisis Grafico de Rentabilidad")

    col1, col2 = st.columns(2)
    with col1:
        precio_venta = st.number_input("Precio de venta (USD)", value=15.99, step=0.01)
        costo_producto = st.number_input("Costo del producto AliExpress (USD)", value=5.50, step=0.01)
    with col2:
        costo_envio = st.number_input("Costo de envio (USD)", value=2.00, step=0.01)
        comision = st.number_input("Comision plataforma %", value=15.0, step=0.5)

    if st.button("Generar analisis grafico", type="primary"):

        comision_usd = precio_venta * (comision / 100)
        margen_neto = precio_venta - costo_producto - costo_envio - comision_usd
        margen_pct = (margen_neto / precio_venta) * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Precio Venta", f"${precio_venta:.2f}")
        col2.metric("Ganancia Neta", f"${margen_neto:.2f}")
        col3.metric("Margen %", f"{margen_pct:.1f}%")
        col4.metric("Ventas para $500", f"{int(500/margen_neto) if margen_neto > 0 else 'N/A'}")

        with st.expander("Grafico de Distribucion de Costos", expanded=True):
            fig_pie = px.pie(
                values=[costo_producto, costo_envio, comision_usd, margen_neto],
                names=["Costo Producto", "Envio", "Comision Plataforma", "Margen Neto"],
                color_discrete_sequence=["#FF4B4B", "#FFA500", "#FFD700", "#00FF9C"],
                title="Distribucion del Precio de Venta"
            )
            fig_pie.update_layout(
                paper_bgcolor="#0e1117",
                font_color="white",
                title_font_color="#00FF9C"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with st.expander("Punto de Equilibrio", expanded=True):
            unidades = list(range(1, 101))
            ingresos = [u * precio_venta for u in unidades]
            costos_totales = [u * (costo_producto + costo_envio + comision_usd) for u in unidades]
            ganancias = [u * margen_neto for u in unidades]

            fig_be = go.Figure()
            fig_be.add_trace(go.Scatter(x=unidades, y=ingresos, name="Ingresos", line=dict(color="#00FF9C", width=2)))
            fig_be.add_trace(go.Scatter(x=unidades, y=costos_totales, name="Costos", line=dict(color="#FF4B4B", width=2)))
            fig_be.add_trace(go.Scatter(x=unidades, y=ganancias, name="Ganancia Neta", line=dict(color="#0066FF", width=2)))
            fig_be.update_layout(
                title="Punto de Equilibrio por Unidades Vendidas",
                xaxis_title="Unidades Vendidas",
                yaxis_title="USD",
                paper_bgcolor="#0e1117",
                plot_bgcolor="#1a1a2e",
                font_color="white",
                title_font_color="#00FF9C"
            )
            st.plotly_chart(fig_be, use_container_width=True)

# MODULO 7 — MONITOR DE BRECHA DE MERCADO
elif modulo == "Monitor de Competencia":
    st.header("Monitor de Brecha de Mercado")
    st.markdown("Analiza las debilidades de tu competencia y encuentra tu ventaja ganadora.")

    producto = st.text_input("Producto a analizar", placeholder="Mascarilla carbon activado")
    resenas_negativas = st.text_area(
        "Pega aqui resenas negativas de competidores en Amazon",
        placeholder="Ejemplo: El producto llego sin instrucciones... La calidad es mala... El empaque estaba danado...",
        height=150
    )

    if st.button("Analizar brechas de mercado", type="primary"):
        with st.spinner("Identificando oportunidades..."):
            prompt = f"""
            Analiza estas resenas negativas de competidores para el producto: {producto}

            RESENAS NEGATIVAS:
            {resenas_negativas}

            Dame un analisis detallado con:

            1. PROBLEMAS PRINCIPALES IDENTIFICADOS
               Lista cada queja recurrente con frecuencia estimada

            2. BRECHAS DE MERCADO DETECTADAS
               Oportunidades especificas basadas en las quejas

            3. ESTRATEGIAS DE DIFERENCIACION GANADORAS
               Para cada problema detectado, sugiere una solucion concreta
               Ejemplo: Si se quejan del manual -> incluir video tutorial QR
               Ejemplo: Si se quejan del empaque -> usar caja premium con branding

            4. PROPUESTA DE VALOR UNICA
               Redacta una propuesta de valor que explote estas brechas

            5. MENSAJE DE MARKETING
               Un mensaje corto que comunique tu diferenciacion
            """
            resultado = consultar_agente(
                "Eres un estratega de mercado experto en encontrar ventajas competitivas en ecommerce.",
                prompt
            )
            st.success("Brechas identificadas!")
            with st.expander("Ver analisis completo", expanded=True):
                st.markdown(resultado)

# MODULO 8 — SCORE DE VALIDACION
elif modulo == "Score de Validacion":
    st.header("Score de Validacion de Producto")
    st.markdown("Calcula la probabilidad de exito de tu producto antes de invertir.")

    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Producto", placeholder="Mascarilla carbon activado")
        margen = st.slider("Margen neto estimado %", 0, 100, 50)
        velocidad_envio = st.slider("Velocidad de envio (1=lento, 10=rapido)", 1, 10, 5)
    with col2:
        saturacion = st.slider("Saturacion del mercado (1=saturado, 10=virgen)", 1, 10, 5)
        competencia = st.slider("Competencia directa (1=mucha, 10=poca)", 1, 10, 5)

    if st.button("Calcular Score de Exito", type="primary"):

        score_margen = (margen / 100) * 40
        score_envio = (velocidad_envio / 10) * 20
        score_saturacion = (saturacion / 10) * 20
        score_competencia = (competencia / 10) * 20
        score_total = score_margen + score_envio + score_saturacion + score_competencia

        if score_total < 40:
            nivel = "Bajo Riesgo"
            color = "#FF4B4B"
        elif score_total < 70:
            nivel = "Potencial Medio"
            color = "#FFA500"
        else:
            nivel = "Ganador Probable"
            color = "#00FF9C"

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_total,
            title={"text": f"Score de Exito: {nivel}", "font": {"color": color, "size": 20}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white"},
                "bar": {"color": color},
                "bgcolor": "#1a1a2e",
                "steps": [
                    {"range": [0, 40], "color": "#FF4B4B33"},
                    {"range": [40, 70], "color": "#FFA50033"},
                    {"range": [70, 100], "color": "#00FF9C33"}
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": score_total
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="#0e1117",
            font_color="white",
            height=400
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Margen (40%)", f"{score_margen:.1f}/40")
        col2.metric("Envio (20%)", f"{score_envio:.1f}/20")
        col3.metric("Saturacion (20%)", f"{score_saturacion:.1f}/20")
        col4.metric("Competencia (20%)", f"{score_competencia:.1f}/20")

        with st.spinner("Generando analisis detallado..."):
            prompt = f"""
            Analiza este producto para dropshipping:
            PRODUCTO: {producto}
            SCORE TOTAL: {score_total:.1f}/100
            NIVEL: {nivel}
            MARGEN: {margen}%
            VELOCIDAD ENVIO: {velocidad_envio}/10
            SATURACION: {saturacion}/10
            COMPETENCIA: {competencia}/10

            Dame:
            1. Interpretacion del score
            2. Los 2 factores mas criticos a mejorar
            3. Recomendacion final: proceder, optimizar o descartar
            4. Proximos pasos especificos
            """
            analisis = consultar_agente("Eres experto en validacion de productos para dropshipping.", prompt)
            with st.expander("Ver analisis detallado del score", expanded=True):
                st.markdown(analisis)

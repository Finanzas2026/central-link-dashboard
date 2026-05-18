import streamlit as st
import re

# ── BASE DE CONOCIMIENTO DEL CHATBOT ───────────────────────────────────────────
KNOWLEDGE = [
    # Dashboards
    {
        "keys": ["cash flow","flujo","efectivo","cashflow"],
        "resp": "📊 **Cash Flow Dashboard** monitorea el flujo de efectivo mensual de CD&P.\n\n"
                "Incluye: Ingresos, Gastos Operativos (Admin, Capital Humano, Marketing, Operativos), "
                "Taxes, Financial Outflows y Efectivo Cierre de Mes para los períodos **2025–2028**.\n\n"
                "👉 [Abrir Cash Flow](https://cashflow-rnqmupyaqzpdva42uw6ywt.streamlit.app/)"
    },
    {
        "keys": ["central link","closing","investment","capex","opex","irr","npv","roi","equity multiple","equity"],
        "resp": "🏗️ **Closing Project Assumptions — Central Link** es el Investment Summary Q4 del proyecto.\n\n"
                "Muestra: Total Equity ($8.1M PC), Total CAPEX ($16.5M PC), Total Revenue ($30.6M PC), "
                "Net Profit ($13.4M PC), IRR (14.4%), NPV ($9.6M), Equity Multiple (3.76x) y ROI (64.97%).\n\n"
                "Compara **Project Closing vs Business Plan**.\n\n"
                "👉 [Abrir Central Link](https://closing-ydh6wy5habve4kbgqchkep.streamlit.app/)"
    },
    {
        "keys": ["estado de resultado","p&l","pl","presupuesto","ebitda","utilidad","ingresos","gastos operativos"],
        "resp": "📈 **Estado de Resultado Dashboard** muestra el P&L de CD&P.\n\n"
                "Compara **Ejecutado 2025 vs Presupuesto 2026, 2027 y 2028**.\n\n"
                "Incluye: Ingresos, Utilidad Bruta, Gastos Operativos desglosados (Admin, Capital Humano, "
                "Marketing, Operativos), EBITDA, Utilidad Operativa, Otros Ingresos/Egresos y Utilidad Neta.\n\n"
                "👉 [Abrir Estado de Resultado](https://estado-de-resultado-j2xcmkofq7q7zwnqs9ycmu.streamlit.app/)"
    },
    # Conceptos financieros
    {
        "keys": ["irr","tir","tasa interna","internal rate"],
        "resp": "📐 **IRR (Internal Rate of Return / Tasa Interna de Retorno)**\n\n"
                "Es la tasa de descuento que hace que el VPN (NPV) de un proyecto sea igual a cero. "
                "Indica la rentabilidad anualizada de la inversión.\n\n"
                "✅ Si el IRR > costo de capital → el proyecto es rentable.\n\n"
                "En Central Link el IRR con financiamiento es **14.41% (Project Closing)** vs 11.03% del Business Plan."
    },
    {
        "keys": ["npv","van","valor presente","net present value","valor actual"],
        "resp": "📐 **NPV (Net Present Value / Valor Presente Neto)**\n\n"
                "Es el valor actual de todos los flujos futuros del proyecto descontados a la tasa requerida. "
                "Si el NPV > 0, el proyecto genera valor por encima del costo de capital.\n\n"
                "En Central Link el NPV es **$9,640,215 (Project Closing)**."
    },
    {
        "keys": ["roi","retorno sobre inversión","return on investment"],
        "resp": "📐 **ROI (Return on Investment)**\n\n"
                "Mide la ganancia o pérdida generada en relación a la inversión realizada.\n\n"
                "Fórmula: (Ganancia - Inversión) / Inversión × 100\n\n"
                "En Central Link el ROI es **64.97% (Project Closing)** vs 43.88% del Business Plan."
    },
    {
        "keys": ["equity multiple","multiplicador","moic"],
        "resp": "📐 **Equity Multiple**\n\n"
                "Indica cuántas veces se multiplicó el capital invertido al final del proyecto.\n\n"
                "Ejemplo: 3.76x significa que por cada $1 invertido se recuperaron $3.76.\n\n"
                "En Central Link el Equity Multiple es **3.76x (Project Closing)** vs 2.68x del Business Plan."
    },
    {
        "keys": ["capex","capital expenditure","gastos de capital","inversión"],
        "resp": "📐 **CAPEX (Capital Expenditures)**\n\n"
                "Son las inversiones en activos físicos del proyecto.\n\n"
                "En Central Link el CAPEX total es **$16,549,458 (Project Closing)**, desglosado en:\n"
                "- Acquisition: $3,350,000\n"
                "- Hard Costs: $11,533,678\n"
                "- Soft Costs: $1,087,695\n"
                "- Dev. Fee (4%): $578,086"
    },
    {
        "keys": ["opex","gastos operativos","operating costs","costos operación"],
        "resp": "📐 **OPEX (Operating Expenditures)**\n\n"
                "Son los costos recurrentes para operar el negocio o proyecto.\n\n"
                "En Central Link el OPEX es **$671,256 (Project Closing)** vs $540,000 del Business Plan.\n\n"
                "En el Estado de Resultado, los Gastos Operativos incluyen: Administración, Capital Humano, Marketing y Operativos."
    },
    {
        "keys": ["ebitda","utilidad operativa","earnings before"],
        "resp": "📐 **EBITDA**\n\n"
                "Earnings Before Interest, Taxes, Depreciation and Amortization.\n"
                "Mide la rentabilidad operativa antes de factores financieros y contables.\n\n"
                "En el Estado de Resultado de CD&P se muestra la **Utilidad Operativa (EBITDA)** comparando "
                "Ejecutado 2025 vs Presupuesto 2026–2028."
    },
    {
        "keys": ["cap rate","capitalization rate","tasa capitalización"],
        "resp": "📐 **Cap Rate (Capitalization Rate)**\n\n"
                "Ratio que mide el rendimiento de un activo inmobiliario basado en su ingreso operativo neto.\n\n"
                "Fórmula: NOI / Valor del activo\n\n"
                "En Central Link el Cap Rate es **5.24% (Project Closing)** vs 9.97% del Business Plan."
    },
    {
        "keys": ["cash on cash","coc","retorno efectivo"],
        "resp": "📐 **Cash-on-Cash Return**\n\n"
                "Mide el rendimiento anual del flujo de caja en relación al capital invertido en efectivo.\n\n"
                "En Central Link el Cash-on-Cash es **1.18x (Project Closing)** vs 0.77x del Business Plan."
    },
    {
        "keys": ["revenue","ingresos totales","total revenue"],
        "resp": "💰 **Total Revenue — Central Link**\n\n"
                "- **Project Closing:** $30,615,475\n"
                "- **Business Plan:** $26,064,945\n\n"
                "Compuesto por:\n"
                "- Rent (Jul 2026–Jul 2029): $3,615,475 PC\n"
                "- Sales (Exit Value): $27,000,000 PC"
    },
    {
        "keys": ["net profit","utilidad neta","ganancia neta"],
        "resp": "💰 **Net Profit — Central Link**\n\n"
                "- **Project Closing:** $13,394,761\n"
                "- **Business Plan:** $9,267,602"
    },
    {
        "keys": ["performance fee","performance"],
        "resp": "💰 **Performance Fee — Central Link**\n\n"
                "- **Project Closing:** $2,678,952 (20% del Net Profit)\n"
                "- **Business Plan:** $1,853,520"
    },
    {
        "keys": ["yappy","nequi","fintech","billetera","banco","banking"],
        "resp": "🏦 **Ecosistema Fintech en Panamá**\n\n"
                "Las principales plataformas de pago móvil en Panamá incluyen:\n"
                "- **Yappy** (Banco General) — líder en pagos P2P\n"
                "- **Nequi Panamá** — cuenta digital sin costo\n\n"
                "Panamá cuenta con más de 60 bancos con licencia general supervisados por la SBP."
    },
    {
        "keys": ["hola","hello","hi","buenos","buenas","que tal","como estas"],
        "resp": "👋 ¡Hola! Soy el asistente del **Cuadro de Mando Financiero de CD&P**.\n\n"
                "Puedo ayudarte con:\n"
                "- 📊 Información sobre los 3 dashboards\n"
                "- 📐 Conceptos financieros (IRR, NPV, ROI, CAPEX, EBITDA...)\n"
                "- 💰 Datos clave de los proyectos\n\n"
                "¿Qué deseas consultar?"
    },
    {
        "keys": ["ayuda","help","que puedes","qué puedes","que sabes","opciones"],
        "resp": "🤖 **Puedo ayudarte con:**\n\n"
                "**Dashboards:**\n"
                "- Cash Flow Dashboard\n"
                "- Closing Project Assumptions (Central Link)\n"
                "- Estado de Resultado\n\n"
                "**Conceptos financieros:**\n"
                "- IRR, NPV, ROI, Equity Multiple\n"
                "- CAPEX, OPEX, EBITDA\n"
                "- Cap Rate, Cash-on-Cash\n\n"
                "**Datos del proyecto:**\n"
                "- Revenue, Net Profit, Total Equity\n"
                "- Performance Fee\n\n"
                "Solo escribe tu pregunta."
    },
]

def responder(pregunta):
    q = pregunta.lower().strip()
    q = re.sub(r'[¿?¡!]', '', q)
    for item in KNOWLEDGE:
        if any(k in q for k in item["keys"]):
            return item["resp"]
    return ("🤔 No tengo información específica sobre eso aún.\n\n"
            "Puedo ayudarte con los **3 dashboards**, conceptos como **IRR, NPV, ROI, CAPEX, EBITDA** "
            "o datos de **Central Link y Estado de Resultado**.\n\n"
            "Escribe **'ayuda'** para ver todo lo que sé.")

st.set_page_config(page_title="Cuadro de Mando Financiero", layout="wide")

st.markdown("""
<meta name="viewport" content="width=1200">
<style>
html, body { min-width: 1200px; }
.main .block-container {
    min-width: 1100px;
    max-width: 1400px;
    padding-top: 2rem;
    box-sizing: border-box;
    overflow-x: auto;
}
section[data-testid="stSidebar"] { display: none; }
@media (max-width: 1200px) {
    html, body { min-width: 1200px; overflow-x: auto; }
    .main .block-container { min-width: 1100px; }
}
.app-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 36px 28px 28px 28px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    text-align: center;
    transition: transform 0.2s;
    height: 340px;
    position: relative;
    box-sizing: border-box;
}
.app-card > div { width: 100%; }
.app-btn { position: absolute; bottom: 28px; left: 50%; transform: translateX(-50%); white-space: nowrap; }
.app-card:hover { transform: translateY(-4px); }
.app-icon   { font-size: 48px; margin-bottom: 8px; }
.app-title  { font-size: 20px; font-weight: 900; color: #0052FF; text-transform: uppercase; letter-spacing: 1px; margin: 8px 0; }
.app-desc   { font-size: 14px; color: #666; line-height: 1.5; }
.app-btn {
    display: inline-block;
    background: #0052FF;
    color: white !important;
    font-weight: 700;
    font-size: 15px;
    padding: 12px 32px;
    border-radius: 8px;
    text-decoration: none;
    margin-top: 16px;
    letter-spacing: 0.5px;
}
.app-btn:hover { background: #0041cc; }
</style>
""", unsafe_allow_html=True)

# ── ENCABEZADO ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0052FF;padding:36px 40px;border-radius:12px;margin-bottom:36px;text-align:center;">
  <div style="color:white;font-size:40px;font-weight:900;letter-spacing:3px;">CUADRO DE MANDO FINANCIERO</div>
  <div style="color:#D0E8FF;font-size:17px;font-weight:600;margin-top:8px;">Selecciona el dashboard que deseas consultar</div>
</div>
""", unsafe_allow_html=True)

# ── CARDS ──────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="app-card">
        <div>
            <div class="app-icon">📊</div>
            <div class="app-title">Cash Flow Dashboard</div>
            <div class="app-desc">Monitoreo del flujo de efectivo mensual por período.<br>Ingresos, Gastos Operativos, Taxes y Cierre de Mes 2025–2028.</div>
        </div>
        <a class="app-btn" href="https://cashflow-rnqmupyaqzpdva42uw6ywt.streamlit.app/" target="_blank">Abrir →</a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="app-card">
        <div>
            <div class="app-icon">🏗️</div>
            <div class="app-title">Closing Project Assumptions</div>
            <div class="app-desc">Investment Summary Q4.<br>CAPEX, OPEX, Revenue y métricas de retorno: IRR, NPV, ROI, Equity Multiple.</div>
        </div>
        <a class="app-btn" href="https://closing-ydh6wy5habve4kbgqchkep.streamlit.app/" target="_blank">Abrir →</a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="app-card">
        <div>
            <div class="app-icon">📈</div>
            <div class="app-title">Estado de Resultado</div>
            <div class="app-desc">P&L Presupuesto 2026–2028 vs Ejecutado 2025.<br>Ingresos, Gastos Operativos, EBITDA y Utilidad Neta.</div>
        </div>
        <a class="app-btn" href="https://estado-de-resultado-j2xcmkofq7q7zwnqs9ycmu.streamlit.app/" target="_blank">Abrir →</a>
    </div>
    """, unsafe_allow_html=True)

# ── CHATBOT ────────────────────────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:40px 0 24px;">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;margin-bottom:20px;">
  <span style="font-size:28px;font-weight:900;color:#0052FF;letter-spacing:1px;">🙂 Arturo Aguilar — Tu Analista Financiero</span><br>
  <span style="font-size:14px;color:#888;">Pregúntame sobre los dashboards, métricas o conceptos financieros</span>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🙂 ¡Hola! Soy **Arturo Aguilar**, tu Analista Financiero.\n\nPuedo responderte sobre los 3 dashboards, conceptos como IRR, NPV, CAPEX, EBITDA y datos reales del proyecto.\n\nEscribe **'ayuda'** para ver todo lo que sé."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    respuesta = responder(prompt)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:48px;color:#aaa;font-size:13px;">
    CD&P Real Estate Management · Cuadro de Mando Financiero
</div>
""", unsafe_allow_html=True)

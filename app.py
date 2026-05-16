import streamlit as st

st.set_page_config(page_title="Cuadro de Mando Financiero", layout="wide")

st.markdown("""
<style>
.main .block-container {
    min-width: 1100px;
    max-width: 1400px;
    padding-top: 2rem;
    box-sizing: border-box;
}
section[data-testid="stSidebar"] { display: none; }
@media (max-width: 768px) {
    .main .block-container { min-width: 1100px; overflow-x: auto; }
}
.app-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 36px 28px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    text-align: center;
    transition: transform 0.2s;
    height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
}
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

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:48px;color:#aaa;font-size:13px;">
    CD&P Real Estate Management · Cuadro de Mando Financiero
</div>
""", unsafe_allow_html=True)

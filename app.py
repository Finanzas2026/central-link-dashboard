import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

FILE_ID = "18i4_XRz2zB_W4ERmJL8Wi6-ZXFiWGsb7"
HOJA    = "Invest Summary-CONSOLIDATED"

st.set_page_config(page_title="Central Link – Investment Summary", layout="wide")

# ── ESTILOS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Forzar modo escritorio */
.main .block-container {
    min-width: 1100px;
    max-width: 1400px;
    padding-top: 2rem;
}
section[data-testid="stSidebar"] { display: none; }
@media (max-width: 768px) {
    .main .block-container { min-width: 1100px; overflow-x: auto; }
}
.kpi-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 28px 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    text-align: center;
    margin-bottom: 12px;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-label  { font-size: 12px; font-weight: 700; color: #666; text-transform: uppercase; letter-spacing: 1px; }
.kpi-pc     { font-size: 22px; font-weight: 900; color: #0052FF; margin: 4px 0 2px; }
.kpi-bp     { font-size: 13px; color: #888; }
.section-title {
    font-size: 20px; font-weight: 900; color: #0052FF;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin: 24px 0 12px;
}
</style>
""", unsafe_allow_html=True)

# ── CARGAR DATOS ───────────────────────────────────────────────────────────────
def cargar():
    url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
    r = requests.get(url)
    df = pd.read_excel(io.BytesIO(r.content), sheet_name=HOJA, header=None)
    return df

df = cargar()

def val(fila, col):
    """Extrae valor numérico de fila (1-indexed) y columna (0-indexed)."""
    try:
        return float(df.iloc[fila - 1, col])
    except:
        return None

def fmt(v, tipo="num"):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    if tipo == "pct":
        return f"{v*100:.2f}%"
    if tipo == "mult":
        return f"{v:.2f}x"
    return f"${v:,.0f}"

# ── EXTRACCIÓN DE DATOS ────────────────────────────────────────────────────────
# Columnas: D=3(Label) E=4(Executed) F=5(Pending) H=7(Project Closing) K=10(Business Plan)
PC, BP = 7, 10
EX, PE = 4, 5

data = {
    "total_equity_pc":    val(12, PC),
    "total_equity_bp":    val(12, BP),
    "total_capex_pc":     val(28, PC),
    "total_capex_bp":     val(28, BP),
    "total_opex_pc":      val(34, PC),
    "total_opex_bp":      val(34, BP),
    "total_revenue_pc":   val(40, PC),
    "total_revenue_bp":   val(40, BP),
    "net_profit_pc":      val(60, PC),
    "net_profit_bp":      val(60, BP),
    "irr_pc":             val(68, PC),
    "irr_bp":             val(68, BP),
    "coc_pc":             val(69, PC),
    "coc_bp":             val(69, BP),
    "npv_pc":             val(70, PC),
    "npv_bp":             val(70, BP),
    "eq_mult_pc":         val(71, PC),
    "eq_mult_bp":         val(71, BP),
    "roi_pc":             val(74, PC),
    "roi_bp":             val(74, BP),
    "roe_pc":             val(75, PC),
    "roe_bp":             val(75, BP),
    "cap_rate_pc":        val(76, PC),
    "cap_rate_bp":        val(76, BP),
    "capex_acq_pc":       val(24, PC),
    "capex_hard_pc":      val(25, PC),
    "capex_soft_pc":      val(26, PC),
    "capex_dev_pc":       val(27, PC),
    "rent_pc":            val(38, PC),
    "sales_pc":           val(39, PC),
    "performance_pc":     val(80, PC),
    "performance_bp":     val(80, BP),
}

# ── TÍTULO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#0052FF;padding:18px 28px;border-radius:10px;margin-bottom:24px;">
  <div style="color:white;font-size:26px;font-weight:900;letter-spacing:2px;">CENTRAL LINK</div>
  <div style="color:#D0E8FF;font-size:13px;font-weight:600;">Investment Summary — Q4 · Project Closing vs Business Plan</div>
</div>
""", unsafe_allow_html=True)

# ── SECCIÓN 1: KPI CARDS ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)

def kpi_card(label, pc, bp, tipo="num"):
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-pc">{fmt(pc, tipo)}</div>
        <div class="kpi-bp">BP: {fmt(bp, tipo)}</div>
    </div>"""

kpis = [
    ("Total Equity",    data["total_equity_pc"],  data["total_equity_bp"],  "num"),
    ("Total CAPEX",     data["total_capex_pc"],   data["total_capex_bp"],   "num"),
    ("Total Revenue",   data["total_revenue_pc"], data["total_revenue_bp"], "num"),
    ("Net Profit",      data["net_profit_pc"],    data["net_profit_bp"],    "num"),
    ("IRR",             data["irr_pc"],            data["irr_bp"],           "pct"),
    ("Equity Multiple", data["eq_mult_pc"],        data["eq_mult_bp"],       "mult"),
    ("NPV",             data["npv_pc"],             data["npv_bp"],           "num"),
    ("ROI",             data["roi_pc"],             data["roi_bp"],           "pct"),
]

cols = st.columns(8)
for i, (label, pc, bp, tipo) in enumerate(kpis):
    with cols[i % 8]:
        st.markdown(kpi_card(label, pc, bp, tipo), unsafe_allow_html=True)

# ── SECCIÓN 2: CAPEX ───────────────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">CAPEX — Capital Expenditures</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    capex_items = [
        ("Acquisition",   data["capex_acq_pc"]),
        ("Hard Costs",    data["capex_hard_pc"]),
        ("Soft Costs",    data["capex_soft_pc"]),
        ("Dev. Fee (4%)", data["capex_dev_pc"]),
    ]
    rows_html = ""
    for name, v in capex_items:
        rows_html += f'<div style="display:flex;justify-content:space-between;padding:10px 20px;border-bottom:1px solid #eee;"><span style="font-weight:600;color:#444;">{name}</span><span style="font-weight:bold;">{fmt(v)}</span></div>'
    total_row = f'<div style="display:flex;justify-content:space-between;padding:12px 20px;background:#0052FF;border-radius:0 0 10px 10px;"><span style="font-weight:900;color:white;">TOTAL CAPEX</span><span style="font-weight:900;color:white;">{fmt(data["total_capex_pc"])}</span></div>'
    st.markdown(f'<div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;margin-bottom:16px;"><div style="background:#d0e8ff;padding:12px 20px;font-weight:700;font-size:14px;">Project Closing</div>{rows_html}{total_row}</div>', unsafe_allow_html=True)

with col_right:
    capex_pie = {k: v for k, v in [
        ("Acquisition", data["capex_acq_pc"]),
        ("Hard Costs",  data["capex_hard_pc"]),
        ("Soft Costs",  data["capex_soft_pc"]),
        ("Dev. Fee",    data["capex_dev_pc"]),
    ] if v and v > 0}
    df_pie = pd.DataFrame({"Categoría": list(capex_pie.keys()), "Valor": list(capex_pie.values())})
    fig = px.pie(df_pie, names="Categoría", values="Valor",
                 color_discrete_sequence=["#0052FF","#4C9BE8","#2ECC71","#E8C34C"])
    fig.update_traces(textinfo="label+percent", textposition="outside", textfont=dict(size=13))
    fig.update_layout(height=340, showlegend=False, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig, use_container_width=True)

# ── SECCIÓN 3: OPEX & REVENUE ──────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">OPEX & Revenue</div>', unsafe_allow_html=True)

col_opex, col_rev = st.columns([1, 1])

with col_opex:
    st.markdown(f"""
    <div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">
        <div style="background:#d0e8ff;padding:12px 20px;font-weight:700;font-size:14px;">OPEX — Operating Costs</div>
        <div style="display:flex;justify-content:space-between;padding:14px 20px;border-bottom:1px solid #eee;">
            <span style="font-weight:600;color:#444;">Project Closing</span>
            <span style="font-weight:bold;">{fmt(data["total_opex_pc"])}</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 20px;background:#f9f9f9;">
            <span style="font-weight:600;color:#444;">Business Plan</span>
            <span style="font-weight:bold;">{fmt(data["total_opex_bp"])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_rev:
    rent = data["rent_pc"] or 0
    sales = data["sales_pc"] or 0
    total_rev = data["total_revenue_pc"] or 0
    st.markdown(f"""
    <div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">
        <div style="background:#d0e8ff;padding:12px 20px;font-weight:700;font-size:14px;">Revenue — Project Closing</div>
        <div style="display:flex;justify-content:space-between;padding:14px 20px;border-bottom:1px solid #eee;">
            <span style="font-weight:600;color:#444;">Rent (Jul 2026–Jul 2029)</span>
            <span style="font-weight:bold;">{fmt(rent)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 20px;border-bottom:1px solid #eee;">
            <span style="font-weight:600;color:#444;">Sales (Exit Value)</span>
            <span style="font-weight:bold;">{fmt(sales)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:12px 20px;background:#0052FF;border-radius:0 0 10px 10px;">
            <span style="font-weight:900;color:white;">TOTAL REVENUE</span>
            <span style="font-weight:900;color:white;">{fmt(total_rev)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── SECCIÓN 4: PERFORMANCE ─────────────────────────────────────────────────────
st.markdown('<hr style="border:none;border-top:2px solid #e0e0e0;margin:24px 0;">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Performance Metrics</div>', unsafe_allow_html=True)

perf_items = [
    ("IRR with Financing", data["irr_pc"],       data["irr_bp"],       "pct"),
    ("Cash-on-Cash",       data["coc_pc"],        data["coc_bp"],       "mult"),
    ("NPV",                data["npv_pc"],         data["npv_bp"],        "num"),
    ("Equity Multiple",    data["eq_mult_pc"],    data["eq_mult_bp"],   "mult"),
    ("ROI",                data["roi_pc"],         data["roi_bp"],        "pct"),
    ("ROE",                data["roe_pc"],         data["roe_bp"],        "mult"),
    ("Cap Rate",           data["cap_rate_pc"],   data["cap_rate_bp"],  "pct"),
    ("Performance Fee",    data["performance_pc"],data["performance_bp"],"num"),
]

header = '<div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:10px 20px;background:#0052FF;border-radius:10px 10px 0 0;"><span style="color:white;font-weight:700;">Metric</span><span style="color:white;font-weight:700;text-align:right;">Project Closing</span><span style="color:white;font-weight:700;text-align:right;">Business Plan</span></div>'
rows = ""
for i, (name, pc, bp, tipo) in enumerate(perf_items):
    bg = "#f9f9f9" if i % 2 == 0 else "#ffffff"
    rows += f'<div style="display:grid;grid-template-columns:2fr 1fr 1fr;padding:10px 20px;background:{bg};border-bottom:1px solid #eee;"><span style="font-weight:600;color:#444;">{name}</span><span style="font-weight:bold;text-align:right;color:#0052FF;">{fmt(pc, tipo)}</span><span style="color:#888;text-align:right;">{fmt(bp, tipo)}</span></div>'

st.markdown(f'<div style="background:#fff;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">{header}{rows}</div>', unsafe_allow_html=True)

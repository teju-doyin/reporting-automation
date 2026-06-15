"""
HarvestBridge Automated Reporting Tool
Alitheia Capital — AI & Digital Innovation Internship Assessment
Author: Teju Adedoyin

Enter the new quarter's financial and KPI data, then click Generate
to instantly produce a formatted one-page PowerPoint report.
"""

import streamlit as st
from calculator import calculate_financials, Q1_2026_ACTUALS, HISTORICAL
from report_generator import generate_report, fusd, fpct, fqoq, fnum

st.set_page_config(
    page_title="HarvestBridge Reporting Tool",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>
  .header-block {
    background: linear-gradient(135deg, #0D3A6E, #1A5CA8);
    padding: 1.2rem 1.5rem; border-radius: 10px; margin-bottom: 1.2rem;
  }
  .header-block h1 { color: white; margin: 0; font-size: 1.5rem; }
  .header-block p  { color: #B8CCE8; margin: .3rem 0 0; font-size: .85rem; }
  .sec {
    font-weight: 600; color: #1A5CA8;
    border-bottom: 2px solid #1A5CA8;
    padding-bottom: .25rem; margin: 1rem 0 .6rem; font-size: .95rem;
  }
  .hint { font-size: .78rem; color: #888; margin-top: -.4rem; margin-bottom: .6rem; }
  .stButton > button {
    background: #0D3A6E; color: white; border: none;
    border-radius: 6px; padding: .55rem 1.5rem;
    font-weight: 600; font-size: .95rem; width: 100%;
  }
  .stButton > button:hover { background: #1A5CA8; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-block">
  <h1>🌾 HarvestBridge Portfolio Reporting Tool</h1>
  <p>Alitheia Capital &nbsp;·&nbsp; Enter the new quarter's data below and generate a formatted report instantly.</p>
</div>
""", unsafe_allow_html=True)

st.info(
    "**Prior quarter (Q1 2026)** actuals are pre-loaded for QoQ comparison. "
    "Enter the new quarter's data below and click Generate.",
    icon="ℹ️"
)

# ── Quarter label ─────────────────────────────────────────────────
q_col, _ = st.columns([1, 4])
with q_col:
    quarter_label = st.text_input("Quarter label", value="Q2 2026",
                                   help="e.g. Q2 2026, Q3 2026")

st.markdown("---")

# ── Input tabs ────────────────────────────────────────────────────
tab_fin, tab_kpi = st.tabs(["📊 Financial Inputs (USD '000)", "📈 KPI Inputs"])

with tab_fin:
    st.markdown('<div class="sec">Revenue</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    loan_fees = r1.number_input("Loan facilitation fees",    value=0.0, step=10.0)
    saas_rev  = r2.number_input("SaaS subscription revenue", value=0.0, step=10.0)
    insurance = r3.number_input("Insurance commissions",     value=0.0, step=10.0)
    other     = r4.number_input("Other income",              value=0.0, step=10.0)

    st.markdown('<div class="sec">Cost of Sales</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    tech    = c1.number_input("Technology & infrastructure", value=0.0, step=10.0)
    credit  = c2.number_input("Credit loss provision",       value=0.0, step=10.0)
    third_p = c3.number_input("Third-party data & APIs",     value=0.0, step=10.0)

    st.markdown('<div class="sec">Operating Expenses</div>', unsafe_allow_html=True)
    o1, o2, o3 = st.columns(3)
    sales_mkt = o1.number_input("Sales & marketing",         value=0.0, step=10.0)
    g_and_a   = o2.number_input("General & administrative",  value=0.0, step=10.0)
    rd        = o3.number_input("Research & development",    value=0.0, step=10.0)

    st.markdown('<div class="sec">Below the Line</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hint">Bracketed items in the Excel are negative here. '
        'e.g. interest expense (238) → enter -238. FX gain = positive, FX loss = negative.</p>',
        unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    dep      = b1.number_input("Depreciation & amortisation", value=0.0, step=1.0)
    interest = b2.number_input("Interest expense",            value=0.0, step=10.0)
    fx       = b3.number_input("FX gain / (loss)",            value=0.0, step=5.0)
    tax      = b4.number_input("Income tax expense",          value=0.0, step=10.0)

with tab_kpi:
    st.markdown('<div class="sec">Operations & People</div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)
    cash_runway = k1.text_input("Cash runway (e.g. 20 months)", value="")
    fte         = k2.number_input("FTE headcount (total)",       value=0, step=1)
    female_fte  = k3.number_input("Female FTE headcount",        value=0, step=1)

    st.markdown('<div class="sec">Gender Lens (enter as whole numbers e.g. 40 for 40%)</div>',
                unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    f_board = g1.number_input("Female Board (%)",      value=0.0, step=0.5)
    f_exec  = g2.number_input("Female Executives (%)", value=0.0, step=0.5)
    f_mid   = g3.number_input("Female Mid-Mgmt (%)",   value=0.0, step=0.5)

    st.markdown('<div class="sec">Lending, Insurance & SaaS</div>', unsafe_allow_html=True)
    l1, l2, l3 = st.columns(3)
    loans    = l1.number_input("Loans disbursed (smallholder)", value=0,   step=100)
    policies = l2.number_input("Active insurance policies",     value=0,   step=100)
    claims   = l3.number_input("Claims paid (USD '000)",        value=0,   step=5)
    s1, s2   = st.columns(2)
    saas_u   = s1.number_input("Active SaaS users",             value=0,   step=100)
    distrib  = s2.number_input("Distributor partners (total)",  value=0,   step=1)

# ── Assemble dicts ────────────────────────────────────────────────
inputs = {
    "loan_fees": loan_fees, "saas_revenue": saas_rev,
    "insurance_commissions": insurance, "other_income": other,
    "tech_infrastructure": tech, "credit_loss_provision": credit,
    "third_party_data": third_p, "sales_marketing": sales_mkt,
    "general_admin": g_and_a, "rd": rd,
    "depreciation_amortisation": dep, "interest_expense": interest,
    "fx_loss": fx, "income_tax": tax,
}

def norm(v):
    return v / 100 if v > 1 else v

kpis = {
    "cash_runway":              cash_runway,
    "fte_headcount":            fte,
    "female_fte":               female_fte,
    "female_board_pct":         norm(f_board),
    "female_exec_pct":          norm(f_exec),
    "female_midmgmt_pct":       norm(f_mid),
    "loans_disbursed":          loans,
    "active_insurance_policies": policies,
    "claims_paid":              claims,
    "active_saas_users":        saas_u,
    "distributor_partners":     distrib,
}

# ── Live preview ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="sec">Calculated Metrics Preview</div>', unsafe_allow_html=True)

fin = calculate_financials(inputs, Q1_2026_ACTUALS)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Revenue", fusd(fin["total_revenue"]),
          f"{fqoq(fin.get('revenue_qoq'))} QoQ vs Q1 2026"
          if fin.get("revenue_qoq") else "")
m2.metric("Gross Profit",  fusd(fin["gross_profit"]),
          f"GM: {fpct(fin['gross_margin'])}")
m3.metric("EBITDA",        fusd(fin["ebitda"]),
          f"Margin: {fpct(fin['ebitda_margin'])}")
m4.metric("EBIT",          fusd(fin["ebit"]))
m5.metric("Net Income",    fusd(fin["net_income"]),
          f"{fqoq(fin.get('net_income_qoq'))} QoQ"
          if fin.get("net_income_qoq") else "")

# ── Generate ──────────────────────────────────────────────────────
st.markdown("---")
if st.button("⬇️  Generate PowerPoint Report"):

    # Narrative built from available data
    prior_label = "Q1 2026"
    female_pct = round(female_fte / fte * 100, 1) if fte and female_fte else 0

    # ── Pull historical figures for YoY comparisons ───────────────
    def _qoq(a, b): return (a - b) / abs(b) if b and b != 0 else None
    def _fqoq_plain(v): return f"{'+' if v>=0 else ''}{v*100:.1f}%" if v is not None else None
    def _fusd_plain(v): return f"USD {v/1000:.2f}M" if abs(v)>=1000 else f"USD {v:.0f}K"

    # Same quarter last year from HISTORICAL
    yoy_label = f"{quarter_label.split()[0]} {int(quarter_label.split()[1])-1}"
    hist_labels = HISTORICAL["labels"]
    hist_rev    = dict(zip(hist_labels, HISTORICAL["revenue"]))
    hist_ebitda = dict(zip(hist_labels, HISTORICAL["ebitda"]))
    hist_net    = dict(zip(hist_labels, HISTORICAL["net_income"]))
    hist_ins    = dict(zip(hist_labels, HISTORICAL["insurance_commissions"]))
    hist_gm     = dict(zip(hist_labels, HISTORICAL["gross_margins"]))

    yoy_rev     = _qoq(fin["total_revenue"],       hist_rev.get(yoy_label))
    yoy_ins     = _qoq(fin["insurance_commissions"], hist_ins.get(yoy_label))
    yoy_gm      = hist_gm.get(yoy_label)
    yoy_net     = hist_net.get(yoy_label)
    gm_bps      = int((fin["gross_margin"] - yoy_gm) * 10000) if yoy_gm else None

    # ── Paragraph 1 — Revenue ─────────────────────────────────────
    p1 = f"In {quarter_label}, HarvestBridge generated {_fusd_plain(fin['total_revenue'])} in total revenue"
    comps = []
    if yoy_rev is not None:
        comps.append(f"up {_fqoq_plain(yoy_rev)} year-on-year versus {yoy_label}")
    if fin.get("revenue_qoq") is not None and prior_label:
        comps.append(f"{_fqoq_plain(fin['revenue_qoq'])} quarter-on-quarter versus {prior_label}")
    p1 += (", " + " and ".join(comps) + ".") if comps else "."

    if loans:
        p1 += f" Growth was driven by continued expansion of the loan book, with {fnum(loans)} loans disbursed to smallholder farmers in the quarter."
    if yoy_ins is not None:
        p1 += f" Insurance commissions grew {_fqoq_plain(yoy_ins)} YoY as the embedded crop insurance product deepened penetration across the existing borrower base."

    # ── Paragraph 2 — Profitability ───────────────────────────────
    p2 = f"Profitability improved materially. Gross profit reached {_fusd_plain(fin['gross_profit'])}, reflecting a gross margin of {fpct(fin['gross_margin'])}"
    if gm_bps is not None:
        direction = "up" if gm_bps > 0 else "down"
        p2 += f" — {direction} {abs(gm_bps)} basis points year-on-year"
    p2 += f". EBITDA rose to {_fusd_plain(fin['ebitda'])} ({fpct(fin['ebitda_margin'])} margin)"
    if fin["net_income"] > 0 and yoy_net is not None and yoy_net < 0:
        p2 += (f", and the company recorded its first profitable quarter with net income of "
               f"{_fusd_plain(fin['net_income'])}, compared to a net loss of "
               f"{_fusd_plain(abs(yoy_net))} in {yoy_label}.")
    else:
        p2 += f". Net income of {_fusd_plain(fin['net_income'])}."

    # ── Paragraph 3 — Workforce ───────────────────────────────────
    p3 = ""
    if fte:
        p3 = f"Workforce stood at {fte} FTE with {female_pct}% female representation."
    if cash_runway:
        p3 += f" Cash runway remained strong at {cash_runway} following the Series B close."

    quarterly_update = "\n\n".join(p for p in [p1, p2, p3] if p)

    # Historical data for bar chart — 5 quarters + new quarter
    hist_fin = {}
    for i, label in enumerate(HISTORICAL["labels"]):
        hist_fin[label] = {
            "total_revenue": HISTORICAL["revenue"][i],
            "ebitda":        HISTORICAL["ebitda"][i],
        }

    company_info = {
        "name":    "HarvestBridge Limited",
        "country": "NG / KE",
        "sector":  "Agri-Fintech",
        "stake":   "10.6%",
        "description": (
            "HarvestBridge Limited is a Lagos and Nairobi-based agri-fintech company that provides "
            "digital working capital loans, crop insurance, and SaaS farm management tools to "
            "smallholder farmers across Nigeria and Kenya. Founded in 2019, the company uses "
            "alternative data — satellite imagery, mobile money history, and input purchase records "
            "— to underwrite farmers excluded from formal banking. Its three revenue streams are "
            "loan facilitation fees, SaaS subscriptions to agri-input distributors, and embedded "
            "crop insurance commissions."
        ),
        "quarterly_update": quarterly_update,
    }

    with st.spinner("Generating report..."):
        pptx_bytes = generate_report(
            fin, kpis, quarter_label, "Q1 2026",
            company_info, hist_fin, HISTORICAL["labels"]
        )

    st.success("Report ready.")
    st.download_button(
        label=f"📥  Download {quarter_label} Report (.pptx)",
        data=pptx_bytes,
        file_name=f"HarvestBridge_{quarter_label.replace(' ', '_')}_Report.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

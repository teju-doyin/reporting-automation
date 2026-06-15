"""
calculator.py - derived metric calculations and QoQ variances
"""

def calculate_financials(inputs: dict, prior_quarter: dict) -> dict:
    total_revenue = (
        inputs["loan_fees"] +
        inputs["saas_revenue"] +
        inputs["insurance_commissions"] +
        inputs["other_income"]
    )
    total_cos = (
        inputs["tech_infrastructure"] +
        inputs["credit_loss_provision"] +
        inputs["third_party_data"]
    )
    gross_profit  = total_revenue - total_cos
    gross_margin  = gross_profit / total_revenue if total_revenue else 0
    total_opex    = inputs["sales_marketing"] + inputs["general_admin"] + inputs["rd"]
    ebitda        = gross_profit - total_opex
    ebitda_margin = ebitda / total_revenue if total_revenue else 0
    ebit          = ebitda - inputs["depreciation_amortisation"]
    # Below-the-line items are signed — brackets in Excel = negative number = add directly
    net_income    = ebit + inputs["interest_expense"] + inputs["fx_loss"] + inputs["income_tax"]

    def qoq(current, key):
        prior = prior_quarter.get(key)
        if prior and prior != 0:
            return (current - prior) / abs(prior)
        return None

    return {
        "loan_fees": inputs["loan_fees"],
        "saas_revenue": inputs["saas_revenue"],
        "insurance_commissions": inputs["insurance_commissions"],
        "other_income": inputs["other_income"],
        "total_revenue": total_revenue,
        "tech_infrastructure": inputs["tech_infrastructure"],
        "credit_loss_provision": inputs["credit_loss_provision"],
        "third_party_data": inputs["third_party_data"],
        "total_cos": total_cos,
        "gross_profit": gross_profit,
        "gross_margin": gross_margin,
        "sales_marketing": inputs["sales_marketing"],
        "general_admin": inputs["general_admin"],
        "rd": inputs["rd"],
        "total_opex": total_opex,
        "ebitda": ebitda,
        "ebitda_margin": ebitda_margin,
        "depreciation_amortisation": inputs["depreciation_amortisation"],
        "ebit": ebit,
        "interest_expense": inputs["interest_expense"],
        "fx_loss": inputs["fx_loss"],
        "income_tax": inputs["income_tax"],
        "net_income": net_income,
        "revenue_qoq":    qoq(total_revenue, "total_revenue"),
        "ebit_qoq":       qoq(ebit,          "ebit"),
        "net_income_qoq": qoq(net_income,     "net_income"),
    }


# ── Q1 2026 actuals — prior quarter for Q2 2026 comparison ───────
Q1_2026_ACTUALS = {
    "total_revenue": 3820.0,
    "gross_profit":  2190.0,
    "ebitda":         935.0,
    "ebit":           899.0,
    "net_income":     417.0,
    "gross_margin":   0.5733,
    "ebitda_margin":  0.2448,
}

# ── Historical revenue + EBITDA for bar chart ─────────────────────
HISTORICAL = {
    "labels":  ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"],
    "revenue": [2800.0,    3060.0,    3305.0,    3675.0,    3820.0],
    "ebitda":  [225.0,    425.0,      615.0,     899.0,     935.0],
    "net_income": [-198.0,   -18.0,     120.0,     354.0,    417.0],
    "insurance_commissions": [310.0,   360.0,     400.0,     470.0,    430.0],
    "gross_margins": [0.5093,  0.5293,    0.5494,    0.573,   0.5733],
}
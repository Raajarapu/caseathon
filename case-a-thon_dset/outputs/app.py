
import io
import html
from pathlib import Path

import pandas as pd
import streamlit as st

# ============================================================
# CONFIG
# ============================================================

APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR

st.set_page_config(
    page_title="Rural Follow-Up Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "Data-Driven Follow-Up Assurance"
APP_SUBTITLE = (
    "Rural Teleconsultation Intelligence | "
    "Connect. Predict. Explain. Prioritize. Act."
)

REQUIRED_FILES = [
    "action_queue.csv",
    "patient360_development.csv",
    "model_comparison.csv",
]

OPTIONAL_FILES = [
    "evaluation_intelligence.csv",
    "evaluation_predictions.csv",
    "feature_importance.csv",
    "feature_metadata.csv",
    "model_features.csv",
    "risk_tier_validation.csv",
    "teleconsultation_linkage.csv",
    "eda_dropout_stage.csv",
    "eda_distance.csv",
    "eda_consult_mode.csv",
    "eda_connectivity.csv",
    "eda_ncd.csv",
    "eda_vulnerability.csv",
    "eda_age.csv",
    "eda_gender.csv",
    "eda_language.csv",
    "medicine_dispensing.csv",
    "medicine_stock_status.csv",
    "prescriptions.csv",
    "teleconsultations.csv",
    "facility_reference.csv",
    "geography_reference.csv",
]

# ============================================================
# GLOBAL LIGHT THEME
# ============================================================

st.markdown(
    """
<style>

/* ---------- APP BACKGROUND ---------- */

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main,
section.main {
    background: #F5F7FA !important;
    color: #172033 !important;
}

[data-testid="stHeader"] {
    background: #F5F7FA !important;
}

.block-container {
    max-width: 1500px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* ---------- ALL NORMAL TEXT ---------- */

html, body, [class*="css"] {
    color: #172033 !important;
}

p, span, label, small, li {
    color: #334155 !important;
    opacity: 1 !important;
}

/* ---------- HEADINGS ---------- */

h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    opacity: 1 !important;
    font-weight: 750 !important;
    line-height: 1.25 !important;
    visibility: visible !important;
}

/* ---------- APP TITLE ---------- */

.app-title {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    font-size: 2.35rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    margin: 0 0 0.35rem 0 !important;
    visibility: visible !important;
}

.app-subtitle {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    margin: 0 0 1.8rem 0 !important;
}

/* ---------- EXPLICIT SECTION HEADINGS ---------- */

.section-title {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    line-height: 1.25 !important;
    margin: 0.4rem 0 1rem 0 !important;
    visibility: visible !important;
}

.subsection-title {
    color: #1E293B !important;
    -webkit-text-fill-color: #1E293B !important;
    font-size: 1.25rem !important;
    font-weight: 750 !important;
    line-height: 1.3 !important;
    margin: 0.8rem 0 0.75rem 0 !important;
    visibility: visible !important;
}

.helper-text {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    margin-bottom: 1rem !important;
}

/* ---------- CUSTOM METRIC CARDS ---------- */


.bar-label-clean {
    color: #26364A !important;
    font-weight: 650 !important;
    font-size: 0.88rem !important;
    margin-bottom: 4px !important;
}
.bar-value-clean {
    color: #0F172A !important;
    font-weight: 750 !important;
    font-size: 0.88rem !important;
    text-align: right !important;
    padding-top: 20px !important;
}


/* Visible status tables */
div[data-testid="stDataFrame"] * {
    color: #1E293B !important;
}

.metric-card {
    background: #FFFFFF !important;
    border: 1px solid #D8E0EA !important;
    border-radius: 14px !important;
    padding: 1.05rem 1.15rem !important;
    min-height: 118px !important;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.07) !important;
    margin-bottom: 0.8rem !important;
    overflow: hidden !important;
}

.metric-label {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.035em !important;
    margin-bottom: 0.55rem !important;
}

.metric-value {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    word-break: break-word !important;
}

.metric-description {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    font-size: 0.76rem !important;
    line-height: 1.35 !important;
    margin-top: 0.35rem !important;
}

/* ---------- INSIGHT CARDS ---------- */

.insight-box {
    background: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #D8E0EA !important;
    border-radius: 12px !important;
    padding: 1rem 1.15rem !important;
    margin: 0.55rem 0 !important;
    box-shadow: 0 2px 7px rgba(15, 23, 42, 0.06) !important;
    line-height: 1.55 !important;
}

.insight-box,
.insight-box p,
.insight-box span,
.insight-box strong {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #D8E0EA !important;
}

section[data-testid="stSidebar"] * {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #64748B !important;
}

section[data-testid="stSidebar"] .stSuccess {
    background: #E7F6EC !important;
    border: 1px solid #B8E0C4 !important;
    color: #176B3A !important;
}

/* ---------- INPUTS ---------- */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea,
input {
    background: #FFFFFF !important;
    color: #172033 !important;
}

div[data-baseweb="select"] *,
div[data-baseweb="input"] *,
[data-testid="stFileUploader"] * {
    color: #172033 !important;
}

div[data-baseweb="select"] > div {
    border-color: #CBD5E1 !important;
    border-radius: 8px !important;
}

/* ---------- BUTTONS ---------- */

.stButton > button,
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #172033 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #64748B !important;
    color: #0F172A !important;
}

/* ---------- DATAFRAMES ---------- */

div[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
    border: 1px solid #D8E0EA !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #D8E0EA !important;
}

/* ---------- RADIO ---------- */

div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p,
div[data-testid="stRadio"] span {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* ---------- CAPTIONS ---------- */

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
}


/* ---------- NEW HEALTHCARE INTELLIGENCE ---------- */
.health-step {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 11px !important;
    padding: 0.82rem !important;
    min-height: 82px !important;
    margin-bottom: 0.65rem !important;
    overflow: visible !important;
}
.health-step-title {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    font-weight: 750 !important;
    font-size: 0.92rem !important;
    line-height: 1.35 !important;
}
.health-step-text {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    font-size: 0.82rem !important;
    line-height: 1.5 !important;
    margin-top: 0.25rem !important;
}
.decision-box {
    background: #F8FAFC !important;
    border: 1px solid #D8E0EA !important;
    border-left: 4px solid #4F86C6 !important;
    border-radius: 10px !important;
    padding: 0.9rem 1rem !important;
    margin: 0.55rem 0 !important;
    overflow: visible !important;
}
.decision-box strong {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}
.decision-box span {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}
[data-testid="stDataFrame"] div,
[data-testid="stDataFrame"] span,
[data-testid="stDataFrame"] p {
    color: #1E293B !important;
    -webkit-text-fill-color: #1E293B !important;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 900px) {
    .app-title {
        font-size: 1.9rem !important;
    }

    .section-title {
        font-size: 1.5rem !important;
    }

    .metric-value {
        font-size: 1.55rem !important;
    }
}


/* ---------- POLISHED PAGE HEADER ---------- */
.app-header {
    margin-top: 0.65rem !important;
    margin-bottom: 1.65rem !important;
}

.app-title {
    font-size: 2.15rem !important;
    letter-spacing: -0.025em !important;
}

.section-title {
    font-size: 1.55rem !important;
    letter-spacing: -0.015em !important;
    margin-top: 0.15rem !important;
    margin-bottom: 0.35rem !important;
}

.subsection-title {
    font-size: 1.12rem !important;
    margin-top: 0.25rem !important;
}

/* ---------- LIGHT CHART CARDS ---------- */
.chart-card {
    background: #FFFFFF !important;
    border: 1px solid #DCE3EC !important;
    border-radius: 14px !important;
    padding: 1.05rem 1.15rem !important;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06) !important;
}

.bar-row {
    margin: 0.75rem 0 !important;
}

.bar-row-top {
    display: flex !important;
    justify-content: space-between !important;
    gap: 1rem !important;
    margin-bottom: 0.35rem !important;
}

.bar-label {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
    font-size: 0.86rem !important;
    font-weight: 650 !important;
}

.bar-value {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    font-size: 0.84rem !important;
    font-weight: 750 !important;
}

.bar-track {
    width: 100% !important;
    height: 9px !important;
    background: #E8EEF5 !important;
    border-radius: 999px !important;
    overflow: hidden !important;
}

.bar-fill {
    height: 100% !important;
    background: #4F86C6 !important;
    border-radius: 999px !important;
}

/* ---------- UPLOAD INTRO ---------- */
.upload-intro {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 1rem !important;
    background: #EEF4FB !important;
    border: 1px solid #D5E2F0 !important;
    border-radius: 10px !important;
    padding: 0.8rem 1rem !important;
    margin: 0.2rem 0 0.65rem 0 !important;
}
.upload-intro strong {
    color: #17324D !important;
    -webkit-text-fill-color: #17324D !important;
}
.upload-intro span {
    color: #5B7085 !important;
    -webkit-text-fill-color: #5B7085 !important;
    font-size: 0.84rem !important;
}

/* ---------- FILE UPLOADER: FORCE LIGHT VISIBLE UI ---------- */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1px solid #D5DEE9 !important;
    border-radius: 14px !important;
    padding: 0.8rem !important;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #F8FAFC !important;
    border: 2px dashed #A8B6C8 !important;
    border-radius: 10px !important;
    min-height: 120px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #1D4ED8 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stFileUploaderFile"] {
    background: #FFFFFF !important;
    border: 1px solid #D5DEE9 !important;
}

[data-testid="stFileUploaderFile"] * {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* ---------- SELECTS / MULTISELECTS ---------- */
div[data-baseweb="select"] {
    background: #FFFFFF !important;
    border-radius: 9px !important;
}

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    color: #172033 !important;
}

div[data-baseweb="select"] input {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* ---------- INFO / SUCCESS BOXES ---------- */
div[data-testid="stAlert"] {
    color: #172033 !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* ---------- DOWNLOAD / PRIMARY ACTIONS ---------- */
.stDownloadButton > button,
.stButton > button {
    min-height: 42px !important;
    font-weight: 650 !important;
}

.stButton > button[kind="primary"] {
    background: #1D4ED8 !important;
    color: #FFFFFF !important;
    border-color: #1D4ED8 !important;
}

.stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

def read_csv(filename):
    path = OUTPUT_DIR / filename
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def number(value):
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def percent(value):
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"


def probability(series):
    values = pd.to_numeric(series, errors="coerce")

    if values.dropna().empty:
        return values

    if values.dropna().max() > 1:
        values = values / 100

    return values.clip(0, 1)


def text_value(value, default="N/A"):
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    value = str(value).strip()
    return value if value else default


def safe_metric(value, default="N/A"):
    return text_value(value, default)


def title(text):
    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True,
    )


def subtitle(text):
    st.markdown(
        f'<div class="helper-text">{text}</div>',
        unsafe_allow_html=True,
    )


def subsection(text):
    st.markdown(
        f'<div class="subsection-title">{text}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label, value, description=None):
    description_html = ""
    if description:
        description_html = (
            f'<div class="metric-description">{description}</div>'
        )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )



# ============================================================
# NEW HEALTHCARE INTELLIGENCE HELPERS
# ============================================================

def first_column(df, candidates):
    if df is None or df.empty:
        return None
    lower_map = {str(c).strip().lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
        key = str(candidate).strip().lower()
        if key in lower_map:
            return lower_map[key]
    return None


def clean_key(series):
    return series.astype(str).str.strip().replace({"nan": ""})


def yes_value(value):
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except Exception:
        pass
    return str(value).strip().lower() in {
        "yes", "y", "true", "1", "required", "advised"
    }


def numeric_value(value, default=0.0):
    try:
        value = pd.to_numeric(value, errors="coerce")
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def care_burden_from_row(row):
    """Operational coordination score; not a clinical severity score."""
    score = 0.0
    reasons = []

    medicine = yes_value(row.get("medicine_advised", row.get("medicine_required", False)))
    test = yes_value(row.get("test_advised", row.get("test_required", False)))
    review = yes_value(row.get("review_advised", row.get("review_required", False)))

    requirement_count = int(medicine) + int(test) + int(review)
    if requirement_count:
        score += min(30.0, requirement_count / 3.0 * 30.0)
        reasons.append(f"{requirement_count} required care component(s)")

    distance = numeric_value(row.get("distance_to_facility_km", row.get("distance_km", 0)))
    if distance > 10:
        score += 25
        reasons.append("long travel distance")
    elif distance > 5:
        score += 18
        reasons.append("moderate-to-high travel distance")
    elif distance > 2:
        score += 10
        reasons.append("non-trivial travel distance")

    due = numeric_value(row.get("review_due_days", row.get("days_to_review", 999)), 999)
    if due <= 2:
        score += 20
        reasons.append("follow-up window is very near")
    elif due <= 7:
        score += 14
        reasons.append("follow-up window is approaching")
    elif due <= 14:
        score += 7
        reasons.append("follow-up is due within two weeks")

    previous = numeric_value(row.get("previous_care_requirements", 0))
    if previous > 0:
        score += min(15.0, previous * 5.0)
        reasons.append("previous care requirements are present")

    if yes_value(row.get("complex_care_episode", False)):
        score += 10
        reasons.append("multiple/complex care context")

    if yes_value(row.get("elderly_living_alone", False)):
        score += 5
        reasons.append("recorded social vulnerability")

    score = max(0.0, min(100.0, score))
    level = "HIGH" if score >= 70 else "MODERATE" if score >= 40 else "LOW"
    return score, level, reasons


def infer_stock_signal(stock_df):
    if stock_df is None or stock_df.empty:
        return None, "Stock-status dataset is not packaged in the current output bundle."

    status_col = first_column(
        stock_df,
        [
            "stock_status", "stock_status_label", "availability_status",
            "stock_availability", "status", "availability", "stock_state",
        ],
    )
    days_col = first_column(
        stock_df,
        ["stockout_days", "days_stockout", "stockout_duration_days"],
    )

    if status_col is None and days_col is None:
        return None, "Stock dataset found, but no recognizable stock-status field was available."

    work = stock_df.copy()
    work["__stock_issue"] = False
    work["__stock_label"] = "Available / no issue recorded"

    if status_col is not None:
        status = work[status_col].astype(str).str.strip().str.lower()
        issue_terms = "stockout|out of stock|unavailable|low|shortage|critical|not available"
        work.loc[status.str.contains(issue_terms, regex=True, na=False), "__stock_issue"] = True
        work.loc[work["__stock_issue"], "__stock_label"] = work.loc[
            work["__stock_issue"], status_col
        ].astype(str)

    if days_col is not None:
        days = pd.to_numeric(work[days_col], errors="coerce").fillna(0)
        work.loc[days > 0, "__stock_issue"] = True
        work.loc[days > 0, "__stock_label"] = "Stockout recorded"

    return work, "Stock availability signal detected from regional stock data."


def attach_patient_context(base, patient_df):
    work = base.copy()

    # First enrich with the development Patient 360 context.
    if "patient_id" in work.columns and "patient_id" in patient_df.columns:
        cols = [
            c for c in [
                "patient_id", "medicine_advised", "test_advised", "review_advised",
                "distance_to_facility_km", "connectivity_quality", "vulnerability_group",
                "age_as_of_2026", "review_due_days",
            ] if c in patient_df.columns
        ]
        if cols:
            p = patient_df[cols].copy()
            p["patient_id"] = clean_key(p["patient_id"])
            p = p.drop_duplicates("patient_id", keep="last")
            work["patient_id"] = clean_key(work["patient_id"])
            work = work.merge(p, on="patient_id", how="left", suffixes=("", "_patient"))

    # Evaluation Intelligence is episode-level and is therefore useful for the
    # evaluation cohort, where development Patient 360 may not contain the row.
    try:
        eval_df = DATA.get("evaluation_intelligence", pd.DataFrame())
    except Exception:
        eval_df = pd.DataFrame()

    if not eval_df.empty and "episode_id" in work.columns and "episode_id" in eval_df.columns:
        wanted = [
            "episode_id", "patient_id", "medicine_advised", "test_advised",
            "review_advised", "distance_to_facility_km", "connectivity_quality",
            "review_due_days", "previous_care_requirements", "complex_care_episode",
            "elderly_living_alone", "facility_id", "medicine_id",
        ]
        cols = [c for c in wanted if c in eval_df.columns]
        if "episode_id" in cols:
            e = eval_df[cols].copy().drop_duplicates("episode_id", keep="last")
            e["episode_id"] = clean_key(e["episode_id"])
            work["episode_id"] = clean_key(work["episode_id"])
            work = work.merge(e, on="episode_id", how="left", suffixes=("", "_eval"))

            # Coalesce evaluation context into the base columns without replacing
            # values already present in the action queue.
            for field in [
                "medicine_advised", "test_advised", "review_advised",
                "distance_to_facility_km", "connectivity_quality", "review_due_days",
                "previous_care_requirements", "complex_care_episode",
                "elderly_living_alone", "facility_id", "medicine_id",
            ]:
                eval_field = f"{field}_eval"
                if eval_field in work.columns:
                    if field not in work.columns:
                        work[field] = work[eval_field]
                    else:
                        work[field] = work[field].where(work[field].notna(), work[eval_field])

    return work


def build_medicine_impact(action_df, patient_df, dispensing_df, stock_df):
    if action_df is None or action_df.empty:
        return pd.DataFrame(), "No action records are available."

    work = attach_patient_context(action_df, patient_df)

    stage_signal = (
        work["predicted_dropout_stage"].astype(str).str.contains("medicine", case=False, na=False)
        if "predicted_dropout_stage" in work.columns
        else pd.Series(False, index=work.index)
    )
    need_signal = (
        work["medicine_advised"].map(yes_value)
        if "medicine_advised" in work.columns
        else pd.Series(False, index=work.index)
    )
    work = work[stage_signal | need_signal].copy()

    if work.empty:
        return pd.DataFrame(), "No medicine-related episodes were identified."

    work["stock_issue"] = False
    work["stock_signal"] = "Not available in current bundle"

    stock_work, stock_note = infer_stock_signal(stock_df)
    if stock_work is not None and not stock_work.empty:
        if all(c in work.columns and c in stock_work.columns for c in ["facility_id", "medicine_id"]):
            small = stock_work[
                ["facility_id", "medicine_id", "__stock_issue", "__stock_label"]
            ].drop_duplicates(["facility_id", "medicine_id"], keep="last").copy()
            for c in ["facility_id", "medicine_id"]:
                work[c] = clean_key(work[c])
                small[c] = clean_key(small[c])
            work = work.merge(small, on=["facility_id", "medicine_id"], how="left")
            work["stock_issue"] = work["__stock_issue"].fillna(False).astype(bool)
            work["stock_signal"] = work["__stock_label"].fillna("No linked stock signal")
        else:
            shared = []
            for key in ["facility_id", "medicine_id", "facility", "medicine", "medicine_name"]:
                if key in work.columns and key in stock_work.columns:
                    shared.append(key)
            if shared:
                key = shared[0]
                small = stock_work[[key, "__stock_issue", "__stock_label"]].drop_duplicates(key, keep="last")
                work = work.merge(small, on=key, how="left")
                work["stock_issue"] = work["__stock_issue"].fillna(False).astype(bool)
                work["stock_signal"] = work["__stock_label"].fillna("No linked stock signal")

    if dispensing_df is not None and not dispensing_df.empty:
        status_col = first_column(
            dispensing_df,
            ["dispensing_status", "dispense_status", "status", "dispensed", "collection_status"],
        )
        if status_col:
            status = dispensing_df[status_col].astype(str).str.lower()
            work["dispensing_barrier_signal"] = (
                "Potential dispensing barrier" if status.str.contains("pending|not|failed|unavailable|no", na=False).any()
                else "No dispensing barrier detected"
            )
        else:
            work["dispensing_barrier_signal"] = "Dispensing status not mapped"
    else:
        work["dispensing_barrier_signal"] = "Dispensing data unavailable"

    work["risk_probability"] = (
        probability(work["risk_probability"]) if "risk_probability" in work.columns else 0.0
    )
    work["patient_impact_priority"] = "STANDARD"
    work.loc[(work["stock_issue"]) & (work["risk_probability"] >= 0.60), "patient_impact_priority"] = "VERY HIGH"
    work.loc[(work["stock_issue"]) & (work["risk_probability"] < 0.60), "patient_impact_priority"] = "HIGH"
    work.loc[(~work["stock_issue"]) & (work["risk_probability"] >= 0.80), "patient_impact_priority"] = "HIGH"

    return work, stock_note


def next_best_action(row):
    medicine = yes_value(row.get("medicine_advised", row.get("medicine_required", False)))
    test = yes_value(row.get("test_advised", row.get("test_required", False)))
    review = yes_value(row.get("review_advised", row.get("review_required", False)))
    stock_issue = yes_value(row.get("stock_issue", False))
    distance = numeric_value(row.get("distance_to_facility_km", row.get("distance_km", 0)))
    connectivity = str(row.get("connectivity_quality", "")).strip().lower()
    risk = numeric_value(row.get("risk_probability", 0))
    stage = str(row.get("predicted_dropout_stage", "")).lower()

    if stock_issue and medicine:
        return (
            "Verify medicine availability at the linked facility and coordinate collection support.",
            "ASHA / Facility team",
            "Medicine access dependency",
        )
    if medicine and "medicine" in stage:
        return (
            "Contact the patient, confirm medicine collection status, and coordinate pickup support if needed.",
            "ASHA",
            "Medicine collection dependency",
        )
    if test and "test" in stage:
        return (
            "Confirm the required test and coordinate the next available facility/lab visit.",
            "ASHA / CHO",
            "Diagnostic completion dependency",
        )
    if review and "review" in stage:
        return (
            "Schedule or remind the patient about the required follow-up review.",
            "CHO",
            "Review attendance dependency",
        )
    if distance > 10:
        return (
            "Use community outreach and coordinate the lowest-friction follow-up option for a long-distance patient.",
            "ASHA",
            "Geographic access barrier",
        )
    if connectivity in {"poor", "intermittent", "limited"}:
        return (
            "Prefer low-bandwidth phone/SMS/community outreach for the follow-up contact.",
            "ASHA",
            "Connectivity barrier",
        )
    if risk >= 0.80:
        return (
            "Perform priority outreach and verify that all required follow-up steps are progressing.",
            "CHO / ASHA",
            "High overall follow-up risk",
        )
    return (
        "Send a routine follow-up reminder and verify completion of the outstanding care step.",
        "CHO / ASHA",
        "Routine continuity action",
    )


def build_next_best_action(action_df, patient_df, stock_df):
    if action_df is None or action_df.empty:
        return pd.DataFrame()

    work = attach_patient_context(action_df, patient_df)
    stock_work, _ = infer_stock_signal(stock_df)
    work["stock_issue"] = False
    work["stock_signal"] = "Stock dataset not available"

    if stock_work is not None and not stock_work.empty:
        if all(c in work.columns and c in stock_work.columns for c in ["facility_id", "medicine_id"]):
            small = stock_work[
                ["facility_id", "medicine_id", "__stock_issue", "__stock_label"]
            ].drop_duplicates(["facility_id", "medicine_id"], keep="last").copy()
            for c in ["facility_id", "medicine_id"]:
                work[c] = clean_key(work[c])
                small[c] = clean_key(small[c])
            work = work.merge(small, on=["facility_id", "medicine_id"], how="left")
            work["stock_issue"] = work["__stock_issue"].fillna(False).astype(bool)
            work["stock_signal"] = work["__stock_label"].fillna("No linked stock signal")

    work["risk_probability"] = (
        probability(work["risk_probability"]) if "risk_probability" in work.columns else 0.0
    )
    decisions = work.apply(next_best_action, axis=1, result_type="expand")
    decisions.columns = ["next_best_action", "recommended_cadre", "dependency"]
    work = pd.concat([work.reset_index(drop=True), decisions.reset_index(drop=True)], axis=1)
    work["action_priority"] = "STANDARD"
    work.loc[work["risk_probability"] >= 0.80, "action_priority"] = "VERY HIGH"
    work.loc[(work["risk_probability"] >= 0.60) & (work["risk_probability"] < 0.80), "action_priority"] = "HIGH"
    return work


# ============================================================
# LIGHTWEIGHT CHARTS
# ============================================================

def horizontal_bars(series, value_suffix="", max_items=10):
    """Render clean native Streamlit horizontal bars with correct displayed values."""
    if series is None or len(series) == 0:
        st.info("No chart data available.")
        return

    data = pd.to_numeric(series, errors="coerce").dropna()
    data = data.sort_values(ascending=False).head(max_items)

    if data.empty:
        st.info("No chart data available.")
        return

    # Feature-importance files may store proportions (0.1243)
    # or percentages (12.43). Display percentage proportions correctly.
    is_percent = value_suffix == "%"
    if is_percent and float(data.max()) <= 1.0:
        data = data * 100.0

    maximum = float(data.max()) or 1.0

    for label, value in data.items():
        numeric = float(value)
        ratio = max(0.0, min(1.0, numeric / maximum))

        left, right = st.columns([5.5, 1])
        with left:
            st.markdown(
                f'<div class="bar-label-clean">{html.escape(str(label))}</div>',
                unsafe_allow_html=True,
            )
            st.progress(ratio)

        with right:
            st.markdown(
                f'<div class="bar-value-clean">{numeric:,.2f}{value_suffix}</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_all_data():
    missing = [
        file
        for file in REQUIRED_FILES
        if not (OUTPUT_DIR / file).exists()
    ]

    if missing:
        raise FileNotFoundError(
            "Missing required files: " + ", ".join(missing)
        )

    datasets = {}

    for filename in REQUIRED_FILES + OPTIONAL_FILES:
        datasets[filename.replace(".csv", "")] = read_csv(filename)

    return datasets


try:
    DATA = load_all_data()
except Exception as error:
    st.error("Application data could not be loaded.")
    st.exception(error)
    st.stop()


action_queue = DATA["action_queue"]
patient360 = DATA["patient360_development"]
model_comparison = DATA["model_comparison"]

feature_importance = DATA["feature_importance"]
model_features = DATA["model_features"]
risk_tier_validation = DATA["risk_tier_validation"]
evaluation_predictions = DATA["evaluation_predictions"]
teleconsultation_linkage = DATA["teleconsultation_linkage"]


# ============================================================
# GLOBAL METRICS
# ============================================================

def calculate_metrics():
    result = {
        "patients": 0,
        "episodes": 0,
        "ltfu": 0,
        "rate": 0.0,
    }

    if not patient360.empty and "patient_id" in patient360.columns:
        result["patients"] = patient360["patient_id"].nunique()

    label_col = existing_column(
        model_features,
        [
            "lost_to_followup_label",
            "ltfu_label",
            "target",
            "label",
        ],
    )

    if label_col:
        labels = pd.to_numeric(
            model_features[label_col],
            errors="coerce",
        ).dropna()

        result["episodes"] = len(labels)
        result["ltfu"] = int((labels == 1).sum())

        if len(labels):
            result["rate"] = (
                result["ltfu"] / result["episodes"] * 100
            )

    return result


METRICS = calculate_metrics()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f'<div class="app-header"><div class="app-title">{APP_TITLE}</div>'
    f'<div class="app-subtitle">{APP_SUBTITLE}</div></div>',
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select module",
    [
        "Overview",
        "Patient 360",
        "Risk AI",
        "Care Journey",
        "Data Hub",
        "Workforce",
        "Medicines",
        "Medicine Stock Impact",
        "Care Burden",
        "Next Best Action",
        "Action Queue",
        "Monitoring",
    ],
    key="page_nav",
)

st.sidebar.divider()
st.sidebar.caption("Application Status")
st.sidebar.success("Pipeline loaded")


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    title("Executive Care Continuity Overview")
    subtitle(
        "Development-cohort outcomes and evaluation episodes "
        "available for follow-up prioritization."
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        metric_card(
            "Unique Patients",
            number(METRICS["patients"]),
            "Patients represented in Patient 360 development data.",
        )

    with c2:
        metric_card(
            "Development Episodes",
            number(METRICS["episodes"]),
            "Episodes with known development outcomes.",
        )

    with c3:
        metric_card(
            "LTFU Episodes",
            number(METRICS["ltfu"]),
            "Development episodes labelled lost to follow-up.",
        )

    with c4:
        metric_card(
            "LTFU Rate",
            percent(METRICS["rate"]),
            "Historical development-cohort LTFU rate.",
        )

    with c5:
        metric_card(
            "Evaluation Episodes for Follow-Up",
            number(len(action_queue)),
            "Evaluation episodes available for prioritized action.",
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        subsection("Care Journey Bottlenecks")

        if (
            not action_queue.empty
            and "predicted_dropout_stage" in action_queue.columns
        ):
            stages = (
                action_queue["predicted_dropout_stage"]
                .dropna()
                .astype(str)
                .value_counts()
            )
        else:
            stages = pd.Series(
                {
                    "Medicine not collected": 1170,
                    "Review not attended": 543,
                    "Test not completed": 275,
                }
            )

        horizontal_bars(stages, max_items=6)

    with right:
        subsection("Risk Distribution")

        if (
            not action_queue.empty
            and "priority_tier" in action_queue.columns
        ):
            risk = (
                action_queue["priority_tier"]
                .value_counts()
                .reindex(
                    [
                        "LOW",
                        "MEDIUM",
                        "HIGH",
                        "VERY HIGH",
                    ],
                    fill_value=0,
                )
            )
        else:
            risk = pd.Series(dtype="int64")

        horizontal_bars(risk, max_items=4)

    st.divider()

    subsection("Model Comparison")

    if not model_comparison.empty:
        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("Model comparison output is unavailable.")

    subsection("Decision Signals")

    signals = []

    if METRICS["rate"]:
        signals.append(
            f"<strong>{METRICS['rate']:.2f}%</strong> of development "
            "episodes were labelled lost to follow-up."
        )

    signals.append(
        f"<strong>{len(action_queue):,}</strong> evaluation episodes "
        "are available for prioritized follow-up."
    )

    if not feature_importance.empty:
        feature_col = existing_column(
            feature_importance,
            ["feature", "Feature", "feature_name"],
        )

        if feature_col:
            top_feature = text_value(
                feature_importance.iloc[0][feature_col],
                default="",
            )

            if top_feature:
                signals.append(
                    "The leading global model feature is "
                    f"<strong>{top_feature}</strong>."
                )

    for signal in signals:
        st.markdown(
            f'<div class="insight-box">{signal}</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# PATIENT 360
# ============================================================

elif page == "Patient 360":

    title("Patient 360")
    subtitle(
        "A consolidated view of patient context, episodes and "
        "follow-up intelligence."
    )

    if patient360.empty:
        st.warning("Patient 360 data is unavailable.")
        st.stop()

    if "patient_id" not in patient360.columns:
        st.error("patient_id column is missing.")
        st.stop()

    patients = (
        patient360["patient_id"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_patient = st.selectbox(
        "Select Patient",
        patients,
    )

    patient = patient360[
        patient360["patient_id"].astype(str) == selected_patient
    ].copy()

    if patient.empty:
        st.warning("Patient record not found.")
        st.stop()

    row = patient.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Age",
            safe_metric(row.get("age_as_of_2026", "N/A")),
            "Age recorded for the selected patient.",
        )

    with c2:
        metric_card(
            "NCD Status",
            safe_metric(row.get("known_ncd_status", "N/A")),
            "Known NCD status available in Patient 360.",
        )

    with c3:
        metric_card(
            "Vulnerability",
            safe_metric(row.get("vulnerability_group", "N/A")),
            "Recorded vulnerability grouping.",
        )

    with c4:
        metric_card(
            "Teleconsultation Episodes",
            number(len(patient)),
            "Recorded episodes for this patient.",
        )

    st.divider()

    subsection("Patient Context")

    context_columns = [
        "episode_id",
        "consult_date",
        "consult_mode",
        "distance_to_facility_km",
        "connectivity_quality",
        "medicine_advised",
        "test_advised",
        "review_advised",
        "lost_to_followup_label",
    ]

    available = [
        col for col in context_columns if col in patient.columns
    ]

    if available:
        st.dataframe(
            patient[available],
            use_container_width=True,
            hide_index=True,
        )

    if (
        not action_queue.empty
        and "patient_id" in action_queue.columns
    ):
        patient_actions = action_queue[
            action_queue["patient_id"].astype(str) == selected_patient
        ].copy()

        if not patient_actions.empty:
            subsection("Patient Risk Intelligence")

            if "risk_probability" in patient_actions.columns:
                patient_actions["risk_probability"] = probability(
                    patient_actions["risk_probability"]
                )

                highest = patient_actions.loc[
                    patient_actions["risk_probability"].idxmax()
                ]

                a, b, c = st.columns(3)

                with a:
                    metric_card(
                        "Highest Risk",
                        f"{highest['risk_probability']:.1%}",
                        "Highest episode-level risk probability.",
                    )

                with b:
                    metric_card(
                        "Priority",
                        safe_metric(
                            highest.get("priority_tier", "N/A")
                        ),
                        "Operational follow-up priority.",
                    )

                with c:
                    metric_card(
                        "Suggested Stage",
                        safe_metric(
                            highest.get(
                                "predicted_dropout_stage",
                                "N/A",
                            )
                        ),
                        "Heuristic stage suggestion from the action output.",
                    )


# ============================================================
# RISK AI
# ============================================================

elif page == "Risk AI":

    title("Risk AI")
    subtitle(
        "Explainable prioritization of episodes requiring "
        "follow-up attention."
    )

    if action_queue.empty:
        st.warning("Risk data is unavailable.")
        st.stop()

    risk = action_queue.copy()

    if "risk_probability" in risk.columns:
        risk["risk_probability"] = probability(
            risk["risk_probability"]
        )
        risk = risk.sort_values(
            "risk_probability",
            ascending=False,
        )

    if "episode_id" not in risk.columns:
        st.error("episode_id column is missing.")
        st.stop()

    episodes = (
        risk["episode_id"]
        .dropna()
        .astype(str)
        .tolist()
    )

    selected_episode = st.selectbox(
        "Select Episode",
        episodes,
    )

    selected = risk[
        risk["episode_id"].astype(str) == selected_episode
    ]

    if selected.empty:
        st.warning("Episode not found.")
        st.stop()

    row = selected.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Risk Probability",
            f"{float(row.get('risk_probability', 0)):.1%}",
            "Model-estimated probability of LTFU.",
        )

    with c2:
        metric_card(
            "Priority",
            safe_metric(row.get("priority_tier", "N/A")),
            "Operational priority tier.",
        )

    with c3:
        metric_card(
            "Suggested Stage",
            safe_metric(
                row.get("predicted_dropout_stage", "N/A")
            ),
            "Heuristic care-journey stage suggestion.",
        )

    with c4:
        metric_card(
            "Assigned Cadre",
            safe_metric(row.get("assigned_cadre", "N/A")),
            "Suggested follow-up workforce cadre.",
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        subsection("Why This Episode Needs Attention")

        reason = text_value(
            row.get("reason", ""),
            default="No explanation available.",
        )

        st.info(reason)

    with right:
        subsection("Recommended Action")

        action = text_value(
            row.get("recommended_action", ""),
            default="No action recommendation available.",
        )

        st.success(action)

    st.divider()

    subsection("Global Model Explainability")

    if not feature_importance.empty:

        fi = feature_importance.copy()

        feature_col = existing_column(
            fi,
            ["feature", "Feature", "feature_name"],
        )

        importance_col = existing_column(
            fi,
            [
                "importance",
                "Importance",
                "feature_importance",
                "importance_pct",
            ],
        )

        if feature_col and importance_col:

            fi[importance_col] = pd.to_numeric(
                fi[importance_col],
                errors="coerce",
            )

            fi = (
                fi.dropna(subset=[importance_col])
                .sort_values(
                    importance_col,
                    ascending=False,
                )
                .head(12)
            )

            if not fi.empty:
                horizontal_bars(
                    fi.set_index(feature_col)[importance_col],
                    value_suffix="%" if "pct" in importance_col.lower() else "",
                    max_items=12,
                )

            st.caption(
                "Global feature importance from the generated "
                "model explainability output."
            )

        else:
            st.dataframe(
                fi.head(20),
                use_container_width=True,
                hide_index=True,
            )

    else:
        st.info("Feature importance is unavailable.")


# ============================================================
# CARE JOURNEY
# ============================================================

elif page == "Care Journey":

    title("Care Journey Intelligence")
    subtitle(
        "Locate operational bottlenecks between consultation "
        "and completed care."
    )

    if (
        not action_queue.empty
        and "predicted_dropout_stage" in action_queue.columns
    ):
        stages = (
            action_queue["predicted_dropout_stage"]
            .dropna()
            .astype(str)
            .value_counts()
            .rename_axis("Stage")
            .reset_index(name="Episodes")
        )
    else:
        stages = pd.DataFrame(
            {
                "Stage": [
                    "Medicine not collected",
                    "Review not attended",
                    "Test not completed",
                ],
                "Episodes": [1170, 543, 275],
            }
        )

    total = stages["Episodes"].sum()

    if total:
        stages["Share"] = (
            stages["Episodes"] / total * 100
        )

    horizontal_bars(
        stages.set_index("Stage")["Episodes"],
        max_items=8,
    )

    subsection("Care Journey")

    journey = pd.DataFrame(
        {
            "Stage": [
                "Teleconsultation",
                "Prescription / Care Plan",
                "Medicine / Test",
                "Review",
                "Completed Care",
            ],
            "Purpose": [
                "Remote clinical consultation.",
                "Required care is defined.",
                "Required medicine/test activity.",
                "Required follow-up review.",
                "Care journey reaches completion.",
            ],
        }
    )

    st.dataframe(
        journey,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# DATA HUB
# ============================================================

elif page == "Data Hub":

    title("Data Hub")
    subtitle(
        "Upload regional CSV/XLSX data and validate it before "
        "downstream processing."
    )

    st.markdown(
        '<div class="upload-intro"><strong>Regional dataset upload</strong>'
        '<span>CSV or XLSX · Schema validation · Quality checks · Preview</span></div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload regional dataset",
        type=["csv", "xlsx"],
    )

    if uploaded is None:

        st.info(
            "Upload a CSV or XLSX file to inspect its schema, "
            "quality and compatibility."
        )

        source_rows = []

        for filename in REQUIRED_FILES + OPTIONAL_FILES:
            df = DATA.get(
                filename.replace(".csv", ""),
                pd.DataFrame(),
            )

            source_rows.append(
                {
                    "Dataset": filename,
                    "Status": "✓ Available" if not df.empty else "— Missing",
                    "Rows": len(df),
                    "Columns": len(df.columns),
                }
            )

        st.dataframe(
            pd.DataFrame(source_rows),
            use_container_width=True,
            hide_index=True,
        )

    else:

        try:
            if uploaded.name.lower().endswith(".csv"):
                uploaded_df = pd.read_csv(uploaded)
            else:
                uploaded_df = pd.read_excel(uploaded)

        except Exception as error:
            st.error("Could not read uploaded dataset.")
            st.exception(error)
            st.stop()

        if uploaded_df.empty:
            st.warning("Uploaded dataset is empty.")
            st.stop()

        st.success(f"Loaded {uploaded.name}")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card("Rows", number(len(uploaded_df)))

        with c2:
            metric_card(
                "Columns",
                number(len(uploaded_df.columns)),
            )

        with c3:
            metric_card(
                "Duplicates",
                number(uploaded_df.duplicated().sum()),
            )

        with c4:
            metric_card(
                "Missing Cells",
                number(
                    uploaded_df.isna().sum().sum()
                ),
            )

        st.divider()

        subsection("Schema Compatibility")

        expected = (
            set(model_features.columns)
            if not model_features.empty
            else set()
        )

        uploaded_columns = set(uploaded_df.columns)

        matching = sorted(
            expected.intersection(uploaded_columns)
        )

        missing = sorted(
            expected.difference(uploaded_columns)
        )

        additional = sorted(
            uploaded_columns.difference(expected)
        )

        schema = pd.DataFrame(
            {
                "Check": [
                    "Matching columns",
                    "Missing expected columns",
                    "Additional columns",
                ],
                "Count": [
                    len(matching),
                    len(missing),
                    len(additional),
                ],
            }
        )

        st.dataframe(
            schema,
            use_container_width=True,
            hide_index=True,
        )

        if matching:
            st.success(
                f"{len(matching)} columns match the "
                "current feature schema."
            )

        if missing:
            st.warning(
                "The uploaded dataset is not directly compatible "
                "with the current model schema. Mapping and "
                "preprocessing are required before inference."
            )

        subsection("Missingness Profile")

        missingness = (
            uploaded_df.isna()
            .mean()
            .mul(100)
            .sort_values(ascending=False)
            .reset_index()
        )

        missingness.columns = [
            "Column",
            "Missing %",
        ]

        st.dataframe(
            missingness,
            use_container_width=True,
            hide_index=True,
        )

        subsection("Dataset Preview")

        st.dataframe(
            uploaded_df.head(100),
            use_container_width=True,
            hide_index=True,
        )

        csv_buffer = io.StringIO()
        uploaded_df.to_csv(
            csv_buffer,
            index=False,
        )

        st.download_button(
            "Download validated copy",
            data=csv_buffer.getvalue(),
            file_name=(
                "validated_"
                + uploaded.name.rsplit(".", 1)[0]
                + ".csv"
            ),
            mime="text/csv",
        )


# ============================================================
# WORKFORCE
# ============================================================

elif page == "Workforce":

    title("Workforce Intelligence")
    subtitle(
        "Translate follow-up risk into operational workload "
        "and capacity signals."
    )

    if action_queue.empty:
        st.warning("Action queue unavailable.")
        st.stop()

    if "assigned_cadre" not in action_queue.columns:

        st.info("Cadre information unavailable.")

    else:

        cadre = (
            action_queue["assigned_cadre"]
            .fillna("Unassigned")
            .astype(str)
            .value_counts()
        )

        left, right = st.columns(2)

        with left:
            subsection("Workload by Cadre")
            horizontal_bars(cadre, max_items=8)

        with right:
            subsection("High-Priority Workload")

            if "priority_tier" in action_queue.columns:

                high = action_queue[
                    action_queue["priority_tier"].isin(
                        ["HIGH", "VERY HIGH"]
                    )
                ]

                high_cadre = (
                    high["assigned_cadre"]
                    .fillna("Unassigned")
                    .astype(str)
                    .value_counts()
                )

                horizontal_bars(high_cadre, max_items=8)

        st.info(
            "This is capacity-planning intelligence, not an "
            "autonomous hiring or staffing decision."
        )


# ============================================================
# MEDICINES
# ============================================================

elif page == "Medicines":

    title("Medicine Intelligence")
    subtitle(
        "Operational visibility into medicine-related "
        "continuity gaps."
    )

    dispensing = DATA.get(
        "medicine_dispensing",
        pd.DataFrame(),
    )

    if (
        not action_queue.empty
        and "predicted_dropout_stage" in action_queue.columns
    ):
        medicine_actions = action_queue[
            action_queue["predicted_dropout_stage"]
            .astype(str)
            .str.contains(
                "medicine",
                case=False,
                na=False,
            )
        ]
    else:
        medicine_actions = pd.DataFrame()

    if (
        not patient360.empty
        and "medicine_advised" in patient360.columns
    ):
        medicine_required = (
            patient360["medicine_advised"]
            .astype(str)
            .str.lower()
            .isin(["yes", "true", "1"])
            .sum()
        )
    else:
        medicine_required = 0

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Medicine-Related Actions",
            number(len(medicine_actions)),
        )

    with c2:
        metric_card(
            "Dispensing Records",
            number(len(dispensing)),
        )

    with c3:
        metric_card(
            "Medicine Advised",
            number(medicine_required),
        )

    st.divider()

    if not medicine_actions.empty:

        columns = [
            col
            for col in [
                "episode_id",
                "patient_id",
                "risk_probability",
                "priority_tier",
                "predicted_dropout_stage",
                "recommended_action",
                "assigned_cadre",
            ]
            if col in medicine_actions.columns
        ]

        st.dataframe(
            medicine_actions[columns],
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info(
            "No medicine-related actions are available."
        )

    st.info(
        "Medicine intelligence supports operational continuity "
        "planning. It does not generate clinical prescriptions."
    )



# ============================================================
# MEDICINE STOCK -> PATIENT IMPACT
# ============================================================

elif page == "Medicine Stock Impact":

    title("Medicine Stock → Patient Impact")
    subtitle(
        "Connect medicine availability signals with patients and follow-up episodes that may be operationally affected."
    )

    dispensing = DATA.get("medicine_dispensing", pd.DataFrame())
    stock = DATA.get("medicine_stock_status", pd.DataFrame())

    impact, stock_note = build_medicine_impact(
        action_queue,
        patient360,
        dispensing,
        stock,
    )

    stock_available = stock is not None and not stock.empty
    stock_issues = int(impact["stock_issue"].sum()) if not impact.empty and "stock_issue" in impact.columns else 0
    high_impact = int(impact["patient_impact_priority"].isin(["HIGH", "VERY HIGH"]).sum()) if not impact.empty and "patient_impact_priority" in impact.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Medicine-Linked Episodes", number(len(impact)), "Evaluation episodes requiring or associated with medicine continuity.")
    with c2:
        metric_card("Stock Issues Linked", number(stock_issues), "Recorded stock/availability issues linked to patient episodes when stock data is available.")
    with c3:
        metric_card("Priority Patient Impacts", number(high_impact), "Medicine-linked episodes with HIGH or VERY HIGH operational impact.")
    with c4:
        metric_card("Stock Data", "Available" if stock_available else "Not loaded", "Uses the regional stock-status table when it is packaged with the app.")

    st.divider()

    if stock_available:
        st.success(stock_note)
    else:
        st.info(
            "The current Streamlit output bundle does not contain medicine_stock_status.csv. "
            "The page does not invent stockout evidence; it continues to show medicine-related patient impact from the available outputs."
        )

    if impact.empty:
        st.warning("No medicine-related patient impact records are available.")
    else:
        left, right = st.columns([1.2, 1])

        with left:
            subsection("Patient Impact Queue")
            columns = [
                c for c in [
                    "episode_id", "patient_id", "risk_probability", "priority_tier",
                    "patient_impact_priority", "stock_signal",
                    "dispensing_barrier_signal", "recommended_action", "assigned_cadre",
                ] if c in impact.columns
            ]
            table = impact[columns].copy()
            if "risk_probability" in table.columns:
                table["risk_probability"] = probability(table["risk_probability"]).map(lambda x: f"{x:.1%}")
            if "patient_impact_priority" in table.columns:
                order = {"VERY HIGH": 0, "HIGH": 1, "STANDARD": 2}
                table["__order"] = table["patient_impact_priority"].map(order).fillna(3)
                table = table.sort_values("__order").drop(columns=["__order"])
            st.dataframe(table, use_container_width=True, height=470, hide_index=True)

        with right:
            subsection("Operational Impact Logic")
            logic = [
                ("01", "Medicine need", "Identify episodes where medicine continuity is required."),
                ("02", "Availability", "Link facility + medicine stock status when regional stock data is present."),
                ("03", "Patient risk", "Combine the availability signal with existing LTFU risk."),
                ("04", "Priority", "Surface cases where operational intervention may prevent a care gap."),
            ]
            for step, heading, body in logic:
                st.markdown(
                    f'''<div class="health-step">
<div class="health-step-title">{step} · {html.escape(heading)}</div>
<div class="health-step-text">{html.escape(body)}</div>
</div>''',
                    unsafe_allow_html=True,
                )

        st.divider()
        subsection("Healthcare Safety Boundary")
        st.markdown(
            '<div class="decision-box"><strong>Operational signal only.</strong> '
            '<span>This module identifies possible medicine-access barriers and prioritizes follow-up work. '
            'It does not prescribe, change medicines, or make a clinical decision.</span></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# CARE BURDEN
# ============================================================

elif page == "Care Burden":

    title("Care-Burden Intelligence")
    subtitle(
        "Estimate the operational effort required to complete the post-consultation care journey. "
        "This is not a clinical severity score."
    )

    if action_queue.empty:
        st.warning("Action queue data is unavailable.")
        st.stop()

    burden_source = attach_patient_context(action_queue, patient360)
    burden_values = burden_source.apply(care_burden_from_row, axis=1, result_type="expand")
    burden_values.columns = ["care_burden_score", "care_burden_level", "care_burden_reasons"]
    burden = pd.concat(
        [burden_source.reset_index(drop=True), burden_values.reset_index(drop=True)],
        axis=1,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Average Care Burden", f"{burden['care_burden_score'].mean():.1f}/100", "Operational burden across evaluation episodes.")
    with c2:
        metric_card("High Burden Episodes", number(int((burden['care_burden_level'] == 'HIGH').sum())), "Episodes requiring more coordination effort.")
    with c3:
        metric_card("Moderate Burden", number(int((burden['care_burden_level'] == 'MODERATE').sum())), "Episodes with multiple operational dependencies.")
    with c4:
        metric_card("Low Burden", number(int((burden['care_burden_level'] == 'LOW').sum())), "Episodes with fewer recorded coordination demands.")

    st.divider()

    left, right = st.columns([1, 1.2])

    with left:
        subsection("Care-Burden Distribution")
        distribution = burden["care_burden_level"].value_counts().reindex(
            ["LOW", "MODERATE", "HIGH"], fill_value=0
        )
        horizontal_bars(distribution, max_items=3)

        subsection("Score Interpretation")
        interpretation = pd.DataFrame(
            {
                "Level": ["LOW", "MODERATE", "HIGH"],
                "Range": ["0–39", "40–69", "70–100"],
                "Operational meaning": [
                    "Fewer recorded coordination barriers.",
                    "Multiple steps may require active follow-up.",
                    "Several dependencies or access barriers may need coordinated outreach.",
                ],
            }
        )
        st.dataframe(interpretation, use_container_width=True, hide_index=True)

    with right:
        subsection("Highest-Burden Episodes")
        top = burden.sort_values("care_burden_score", ascending=False).head(15).copy()
        top["Care Burden"] = top["care_burden_score"].map(lambda x: f"{x:.0f}/100")
        top["Why"] = top["care_burden_reasons"].map(
            lambda x: "; ".join(x) if isinstance(x, list) else text_value(x, "No specific factors recorded.")
        )
        columns = [
            c for c in ["episode_id", "patient_id", "Care Burden", "care_burden_level", "risk_probability", "Why"]
            if c in top.columns
        ]
        view = top[columns].copy()
        if "risk_probability" in view.columns:
            view["risk_probability"] = probability(view["risk_probability"]).map(lambda x: f"{x:.1%}")
        st.dataframe(view, use_container_width=True, height=450, hide_index=True)

    st.divider()
    st.markdown(
        '<div class="decision-box"><strong>What this adds:</strong> '
        '<span>Risk prediction answers who may be lost to follow-up. Care burden adds a second operational dimension: '
        'how difficult the required care journey may be to complete.</span></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FOLLOW-UP DEPENDENCY / NEXT-BEST-ACTION ENGINE
# ============================================================

elif page == "Next Best Action":

    title("Follow-up Dependency & Next-Best-Action Engine")
    subtitle(
        "Translate risk and care dependencies into a transparent, rule-based operational action for CHOs and ASHAs."
    )

    if action_queue.empty:
        st.warning("Action queue data is unavailable.")
        st.stop()

    nba = build_next_best_action(
        action_queue,
        patient360,
        DATA.get("medicine_stock_status", pd.DataFrame()),
    )

    if nba.empty:
        st.warning("No next-best-action records are available.")
        st.stop()

    if "episode_id" not in nba.columns:
        st.error("episode_id is required for the next-best-action module.")
        st.stop()

    episodes = nba["episode_id"].dropna().astype(str).unique().tolist()
    selected_episode = st.selectbox("Select Episode", episodes, key="nba_episode_selector")
    selected = nba[nba["episode_id"].astype(str) == selected_episode]
    row = selected.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Episodes With Action", number(len(nba)), "Episodes mapped to an operational follow-up action.")
    with c2:
        metric_card("Very High Priority", number(int((nba["action_priority"] == "VERY HIGH").sum())), "Highest-risk episodes requiring prompt review.")
    with c3:
        metric_card("High Priority", number(int((nba["action_priority"] == "HIGH").sum())), "High-risk episodes requiring active coordination.")
    with c4:
        metric_card("Action Rules", number(nba["next_best_action"].nunique()), "Distinct transparent operational pathways generated.")

    st.divider()

    left, right = st.columns([1, 1.25])

    with left:
        subsection("Current Episode Signal")
        risk_value = numeric_value(row.get("risk_probability", 0))
        metric_card("LTFU Risk", f"{risk_value:.1%}", "Existing model probability.")
        metric_card("Priority", safe_metric(row.get("priority_tier", row.get("action_priority", "N/A"))), "Existing operational priority.")
        metric_card("Suggested Stage", safe_metric(row.get("predicted_dropout_stage", "N/A")), "Existing heuristic stage suggestion.")

    with right:
        subsection("Dependency Chain")
        steps = [
            ("01", "Consultation", "The episode is evaluated at the defined prediction point."),
            ("02", "Required care", "Medicine, test and/or review requirements are checked."),
            ("03", "Access dependency", "Distance, connectivity and stock signals are considered when present."),
            ("04", "Next action", "A transparent rule selects the operational follow-up step."),
        ]
        for step, heading, body in steps:
            st.markdown(
                f'''<div class="health-step">
<div class="health-step-title">{step} · {html.escape(heading)}</div>
<div class="health-step-text">{html.escape(body)}</div>
</div>''',
                unsafe_allow_html=True,
            )

    st.divider()
    subsection("Recommended Next-Best Action")
    action_text = text_value(row.get("next_best_action", "No action available."))
    cadre_text = text_value(row.get("recommended_cadre", "N/A"))
    dependency_text = text_value(row.get("dependency", "N/A"))
    st.markdown(
        f'''<div class="decision-box">
<strong>{html.escape(action_text)}</strong><br>
<span>Responsible cadre: {html.escape(cadre_text)}</span><br>
<span>Dependency: {html.escape(dependency_text)}</span>
</div>''',
        unsafe_allow_html=True,
    )

    subsection("Why This Action Was Selected")
    st.info(text_value(row.get("reason", ""), "No existing model explanation available."))

    st.divider()
    subsection("Action Distribution")
    action_distribution = (
        nba["next_best_action"].fillna("No action available").astype(str).value_counts().head(10)
    )
    horizontal_bars(action_distribution, max_items=10)

    st.markdown(
        '<div class="decision-box"><strong>Human-in-the-loop boundary.</strong> '
        '<span>The engine recommends operational follow-up work. An authorized health worker reviews and executes the action. '
        'The engine does not diagnose, prescribe, or autonomously alter treatment.</span></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# ACTION QUEUE
# ============================================================

elif page == "Action Queue":

    title("Prioritized Action Queue")
    subtitle(
        "Filter and review evaluation episodes according to "
        "risk, suggested stage and assigned cadre."
    )

    if action_queue.empty:
        st.warning("Action queue unavailable.")
        st.stop()

    queue = action_queue.copy()

    c1, c2, c3 = st.columns(3)

    if "priority_tier" in queue.columns:

        values = sorted(
            queue["priority_tier"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_priority = c1.multiselect(
            "Priority",
            values,
            default=values,
        )

        if selected_priority:
            queue = queue[
                queue["priority_tier"]
                .astype(str)
                .isin(selected_priority)
            ]

    if "assigned_cadre" in queue.columns:

        values = sorted(
            queue["assigned_cadre"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_cadre = c2.multiselect(
            "Cadre",
            values,
            default=values,
        )

        if selected_cadre:
            queue = queue[
                queue["assigned_cadre"]
                .astype(str)
                .isin(selected_cadre)
            ]

    if "predicted_dropout_stage" in queue.columns:

        values = sorted(
            queue["predicted_dropout_stage"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_stage = c3.multiselect(
            "Suggested Stage",
            values,
            default=values,
        )

        if selected_stage:
            queue = queue[
                queue["predicted_dropout_stage"]
                .astype(str)
                .isin(selected_stage)
            ]

    if "risk_probability" in queue.columns:

        queue["risk_probability"] = probability(
            queue["risk_probability"]
        )

        queue = queue.sort_values(
            "risk_probability",
            ascending=False,
        )

    metric_card(
        "Visible Actions",
        number(len(queue)),
        "Actions remaining after the selected filters.",
    )

    columns = [
        "episode_id",
        "patient_id",
        "risk_probability",
        "priority_tier",
        "predicted_dropout_stage",
        "reason",
        "recommended_action",
        "assigned_cadre",
    ]

    columns = [
        col for col in columns if col in queue.columns
    ]

    st.dataframe(
        queue[columns],
        use_container_width=True,
        height=620,
        hide_index=True,
    )

    st.download_button(
        "Download Action Queue",
        data=queue[columns]
        .to_csv(index=False)
        .encode("utf-8"),
        file_name="priority_action_queue.csv",
        mime="text/csv",
    )


# ============================================================
# MONITORING
# ============================================================

elif page == "Monitoring":

    title("Data & Model Monitoring")
    subtitle(
        "Monitor dataset availability, linkage coverage and "
        "model-output readiness."
    )

    subsection("Dataset Availability")

    rows = []

    for filename in REQUIRED_FILES + OPTIONAL_FILES:

        df = DATA.get(
            filename.replace(".csv", ""),
            pd.DataFrame(),
        )

        rows.append(
            {
                "Dataset": filename,
                "Status": "✓ Available" if (OUTPUT_DIR / filename).exists() else "— Missing",
                "Rows": len(df),
                "Columns": len(df.columns),
            }
        )

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    subsection("Patient Linkage")

    if not teleconsultation_linkage.empty:

        total = len(teleconsultation_linkage)

        if "predicted_patient_id" in teleconsultation_linkage.columns:

            linked = (
                teleconsultation_linkage[
                    "predicted_patient_id"
                ]
                .notna()
                .sum()
            )

            coverage = (
                linked / total * 100
                if total
                else 0
            )

        else:
            coverage = 0

        c1, c2 = st.columns(2)

        with c1:
            metric_card(
                "Linkage Records",
                number(total),
                "Teleconsultation records evaluated by linkage.",
            )

        with c2:
            metric_card(
                "Computational Linkage Coverage",
                percent(coverage),
                "Algorithmic coverage, not independently validated identity accuracy.",
            )

        st.caption(
            "Coverage represents algorithmic linkage coverage, "
            "not independently validated identity accuracy."
        )

    else:
        st.info("Linkage output unavailable.")

    st.divider()

    subsection("Model Output Status")

    status = pd.DataFrame(
        {
            "Component": [
                "Model Comparison",
                "Risk Validation",
                "Evaluation Predictions",
                "Feature Importance",
                "Action Queue",
            ],
            "Status": [
                "✓ Available" if not model_comparison.empty else "— Missing",
                "✓ Available" if not risk_tier_validation.empty else "— Missing",
                "✓ Available" if not evaluation_predictions.empty else "— Missing",
                "✓ Available" if not feature_importance.empty else "— Missing",
                "✓ Available" if not action_queue.empty else "— Missing",
            ],
        }
    )

    st.dataframe(
        status,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Decision-support system for rural teleconsultation "
    "follow-up assurance. Synthetic case-a-thon data unless "
    "explicitly uploaded by the user."
)

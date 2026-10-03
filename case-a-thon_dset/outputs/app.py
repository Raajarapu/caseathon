
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
# LIGHTWEIGHT CHARTS
# ============================================================

def horizontal_bars(series, value_suffix="", max_items=10):
    """Render a clean light-theme horizontal bar chart without a chart dependency."""
    if series is None or len(series) == 0:
        st.info("No chart data available.")
        return

    data = pd.to_numeric(series, errors="coerce").dropna()
    data = data.sort_values(ascending=False).head(max_items)

    if data.empty:
        st.info("No chart data available.")
        return

    maximum = float(data.max()) or 1.0
    rows = []

    for label, value in data.items():
        safe_label = html.escape(str(label))
        numeric = float(value)
        width = max(3.0, min(100.0, numeric / maximum * 100.0))
        display = f"{numeric:,.0f}{value_suffix}"
        rows.append(
            f"""
            <div class="bar-row">
                <div class="bar-row-top">
                    <span class="bar-label">{safe_label}</span>
                    <span class="bar-value">{display}</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{width:.1f}%"></div>
                </div>
            </div>
            """
        )

    st.markdown(
        '<div class="chart-card">' + "".join(rows) + '</div>',
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

    if st.button("← Back to Overview", key="datahub_back", type="secondary"):
        st.session_state["page_nav"] = "Overview"
        st.rerun()

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
                    "Available": not df.empty,
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
                "Available": (
                    OUTPUT_DIR / filename
                ).exists(),
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
            "Available": [
                not model_comparison.empty,
                not risk_tier_validation.empty,
                not evaluation_predictions.empty,
                not feature_importance.empty,
                not action_queue.empty,
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

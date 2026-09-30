import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# CONFIG
# -------------------------------------------------

BASE_DIR = Path(
    r"C:\Users\RAAJARAPU SUSWIN\Downloads\case-a-thon_dset"
)

OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(
    page_title="Rural Follow-Up Intelligence",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    action_queue = pd.read_csv(
        OUTPUT_DIR / "action_queue.csv"
    )

    patient360 = pd.read_csv(
        OUTPUT_DIR / "patient360_development.csv"
    )

    model_comparison = pd.read_csv(
        OUTPUT_DIR / "model_comparison.csv"
    )

    return (
        action_queue,
        patient360,
        model_comparison
    )


action_queue, patient360, model_comparison = load_data()

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title(
    "Data-Driven Follow-Up Assurance"
)

st.caption(
    "Rural Teleconsultation Decision-Support Prototype"
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Select view",
    [
        "Overview",
        "Patient 360",
        "Risk Intelligence",
        "Action Queue"
    ]
)

# -------------------------------------------------
# OVERVIEW
# -------------------------------------------------

if page == "Overview":

    st.header("Care Continuity Overview")

    total_episodes = 4132
    ltfu_episodes = 1988
    ltfu_rate = 48.11

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Development Episodes",
        f"{total_episodes:,}"
    )

    col2.metric(
        "LTFU Episodes",
        f"{ltfu_episodes:,}"
    )

    col3.metric(
        "LTFU Rate",
        f"{ltfu_rate:.2f}%"
    )

    st.subheader(
        "Dropout Points"
    )

    stage_data = pd.DataFrame({
        "Stage": [
            "Medicine not collected",
            "Review not attended",
            "Test not completed"
        ],
        "Episodes": [
            1170,
            543,
            275
        ]
    })

    st.bar_chart(
        stage_data.set_index("Stage")
    )

    st.subheader(
        "Model Comparison"
    )

    st.dataframe(
        model_comparison,
        use_container_width=True
    )

# -------------------------------------------------
# PATIENT 360
# -------------------------------------------------

elif page == "Patient 360":

    st.header("Patient 360")

    patients = (
        patient360[
            "patient_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_patient = st.selectbox(
        "Select Patient",
        patients
    )

    patient = patient360[
        patient360["patient_id"]
        == selected_patient
    ]

    if len(patient) > 0:

        row = patient.iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Age",
            str(row.get("age_as_of_2026", "N/A"))
        )

        col2.metric(
            "NCD Status",
            str(row.get("known_ncd_status", "N/A"))
        )

        col3.metric(
            "Vulnerability",
            str(row.get("vulnerability_group", "N/A"))
        )

        st.subheader(
            "Patient Context"
        )

        st.dataframe(
            patient[
                [
                    "episode_id",
                    "consult_date",
                    "consult_mode",
                    "distance_to_facility_km",
                    "connectivity_quality",
                    "medicine_advised",
                    "test_advised",
                    "review_advised",
                    "lost_to_followup_label"
                ]
            ],
            use_container_width=True
        )

# -------------------------------------------------
# RISK INTELLIGENCE
# -------------------------------------------------

elif page == "Risk Intelligence":

    st.header("Risk Intelligence")

    risk_sorted = action_queue.sort_values(
        "risk_probability",
        ascending=False
    )

    selected_episode = st.selectbox(
        "Select Episode",
        risk_sorted["episode_id"].tolist()
    )

    row = risk_sorted[
        risk_sorted["episode_id"]
        == selected_episode
    ].iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Risk Probability",
        f"{row['risk_probability']:.1%}"
    )

    col2.metric(
        "Priority",
        row["priority_tier"]
    )

    col3.metric(
        "Predicted Stage",
        row["predicted_dropout_stage"]
    )

    st.subheader("Why this episode needs attention")

    st.write(
        row["reason"]
    )

    st.subheader("Recommended Action")

    st.info(
        row["recommended_action"]
    )

    st.write(
        "Assigned cadre:",
        row["assigned_cadre"]
    )

# -------------------------------------------------
# ACTION QUEUE
# -------------------------------------------------

elif page == "Action Queue":

    st.header("Prioritized Action Queue")

    st.dataframe(
        action_queue[
            [
                "episode_id",
                "patient_id",
                "risk_probability",
                "priority_tier",
                "predicted_dropout_stage",
                "reason",
                "recommended_action",
                "assigned_cadre"
            ]
        ],
        use_container_width=True,
        height=600
    )
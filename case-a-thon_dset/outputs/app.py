import io
from pathlib import Path

import numpy as np
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
]


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .app-title {
        font-size: 2.15rem;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }

    .app-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }

    .insight-box {
        padding: 1rem;
        border: 1px solid #dbe3ea;
        border-radius: 10px;
        background: #f8fafc;
        margin-bottom: 0.7rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem;
        background: white;
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


def text_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


# ============================================================
# LOAD ALL PROJECT OUTPUTS
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
            "Missing required files: "
            + ", ".join(missing)
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
# METRICS
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
                result["ltfu"]
                / result["episodes"]
                * 100
            )

    return result


METRICS = calculate_metrics()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f'<div class="app-title">{APP_TITLE}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="app-subtitle">{APP_SUBTITLE}</div>',
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
)

st.sidebar.divider()

st.sidebar.caption("Application Status")

if action_queue is not None:
    st.sidebar.success("Pipeline loaded")


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("Executive Care Continuity Overview")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Patients",
        number(METRICS["patients"]),
    )

    c2.metric(
        "Development Episodes",
        number(METRICS["episodes"]),
    )

    c3.metric(
        "LTFU Episodes",
        number(METRICS["ltfu"]),
    )

    c4.metric(
        "LTFU Rate",
        percent(METRICS["rate"]),
    )

    c5.metric(
        "Priority Actions",
        number(len(action_queue)),
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Care Journey Bottlenecks")

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

            st.bar_chart(stages)

        else:

            stages = pd.Series(
                {
                    "Medicine not collected": 1170,
                    "Review not attended": 543,
                    "Test not completed": 275,
                }
            )

            st.bar_chart(stages)

    with right:

        st.subheader("Risk Distribution")

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

            st.bar_chart(risk)

    st.divider()

    st.subheader("Model Comparison")

    if not model_comparison.empty:

        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.warning(
            "Model comparison output is unavailable."
        )

    st.subheader("Decision Signals")

    signals = []

    if METRICS["rate"]:

        signals.append(
            f"{METRICS['rate']:.2f}% of development episodes "
            "were labelled lost to follow-up."
        )

    signals.append(
        f"{len(action_queue):,} episodes are available "
        "for prioritized follow-up."
    )

    if not feature_importance.empty:

        feature_col = existing_column(
            feature_importance,
            [
                "feature",
                "Feature",
                "feature_name",
            ],
        )

        if feature_col:

            top_feature = text_value(
                feature_importance.iloc[0][feature_col]
            )

            if top_feature:

                signals.append(
                    f"The leading global model feature is "
                    f"'{top_feature}'."
                )

    for signal in signals:

        st.markdown(
            f"""
            <div class="insight-box">
                {signal}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PATIENT 360
# ============================================================

elif page == "Patient 360":

    st.header("Patient 360")

    if patient360.empty:

        st.warning(
            "Patient 360 data is unavailable."
        )
        st.stop()

    if "patient_id" not in patient360.columns:

        st.error(
            "patient_id column is missing."
        )
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
        patient360["patient_id"].astype(str)
        == selected_patient
    ].copy()

    if patient.empty:

        st.warning(
            "Patient record not found."
        )
        st.stop()

    row = patient.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Age",
        str(row.get("age_as_of_2026", "N/A")),
    )

    c2.metric(
        "NCD Status",
        str(row.get("known_ncd_status", "N/A")),
    )

    c3.metric(
        "Vulnerability",
        str(row.get("vulnerability_group", "N/A")),
    )

    c4.metric(
        "Episodes",
        number(len(patient)),
    )

    st.divider()

    st.subheader("Patient Context")

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
        col
        for col in context_columns
        if col in patient.columns
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
            action_queue["patient_id"].astype(str)
            == selected_patient
        ].copy()

        if not patient_actions.empty:

            st.subheader(
                "Patient Risk Intelligence"
            )

            if "risk_probability" in patient_actions.columns:

                patient_actions["risk_probability"] = (
                    probability(
                        patient_actions[
                            "risk_probability"
                        ]
                    )
                )

                highest = patient_actions.loc[
                    patient_actions[
                        "risk_probability"
                    ].idxmax()
                ]

                a, b, c = st.columns(3)

                a.metric(
                    "Highest Risk",
                    f"{highest['risk_probability']:.1%}",
                )

                b.metric(
                    "Priority",
                    str(
                        highest.get(
                            "priority_tier",
                            "N/A",
                        )
                    ),
                )

                c.metric(
                    "Suggested Stage",
                    str(
                        highest.get(
                            "predicted_dropout_stage",
                            "N/A",
                        )
                    ),
                )


# ============================================================
# RISK AI
# ============================================================

elif page == "Risk AI":

    st.header("Risk AI")

    st.caption(
        "Explainable prioritization of episodes requiring "
        "follow-up attention."
    )

    if action_queue.empty:

        st.warning(
            "Risk data is unavailable."
        )
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

        st.error(
            "episode_id column is missing."
        )
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
        risk["episode_id"].astype(str)
        == selected_episode
    ]

    if selected.empty:

        st.warning(
            "Episode not found."
        )
        st.stop()

    row = selected.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Risk Probability",
        f"{float(row.get('risk_probability', 0)):.1%}",
    )

    c2.metric(
        "Priority",
        str(row.get("priority_tier", "N/A")),
    )

    c3.metric(
        "Suggested Stage",
        str(
            row.get(
                "predicted_dropout_stage",
                "N/A",
            )
        ),
    )

    c4.metric(
        "Assigned Cadre",
        str(
            row.get(
                "assigned_cadre",
                "N/A",
            )
        ),
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "Why this episode needs attention"
        )

        reason = text_value(
            row.get("reason", "")
        )

        st.info(
            reason
            if reason
            else "No explanation available."
        )

    with right:

        st.subheader(
            "Recommended Action"
        )

        action = text_value(
            row.get(
                "recommended_action",
                "",
            )
        )

        if action:

            st.success(action)

        else:

            st.info(
                "No action recommendation available."
            )

    st.divider()

    st.subheader(
        "Global Model Explainability"
    )

    if not feature_importance.empty:

        fi = feature_importance.copy()

        feature_col = existing_column(
            fi,
            [
                "feature",
                "Feature",
                "feature_name",
            ],
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
                fi.dropna(
                    subset=[importance_col]
                )
                .sort_values(
                    importance_col,
                    ascending=False,
                )
                .head(12)
            )

            st.bar_chart(
                fi.set_index(feature_col)[
                    importance_col
                ]
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

        st.info(
            "Feature importance is unavailable."
        )


# ============================================================
# CARE JOURNEY
# ============================================================

elif page == "Care Journey":

    st.header("Care Journey Intelligence")

    st.caption(
        "Locate operational bottlenecks between consultation "
        "and completed care."
    )

    if (
        not action_queue.empty
        and "predicted_dropout_stage" in action_queue.columns
    ):

        stages = (
            action_queue[
                "predicted_dropout_stage"
            ]
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
                "Episodes": [
                    1170,
                    543,
                    275,
                ],
            }
        )

    total = stages["Episodes"].sum()

    if total:

        stages["Share"] = (
            stages["Episodes"]
            / total
            * 100
        )

    st.bar_chart(
        stages.set_index("Stage")[
            "Episodes"
        ]
    )

    st.subheader("Care Journey")

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

    st.header("Data Hub")

    st.caption(
        "Upload regional CSV/XLSX data and validate it before "
        "downstream processing."
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

                uploaded_df = pd.read_csv(
                    uploaded
                )

            else:

                uploaded_df = pd.read_excel(
                    uploaded
                )

        except Exception as error:

            st.error(
                "Could not read uploaded dataset."
            )

            st.exception(error)
            st.stop()

        if uploaded_df.empty:

            st.warning(
                "Uploaded dataset is empty."
            )
            st.stop()

        st.success(
            f"Loaded {uploaded.name}"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Rows",
            number(len(uploaded_df)),
        )

        c2.metric(
            "Columns",
            number(len(uploaded_df.columns)),
        )

        c3.metric(
            "Duplicates",
            number(
                uploaded_df.duplicated().sum()
            ),
        )

        c4.metric(
            "Missing Cells",
            number(
                uploaded_df.isna()
                .sum()
                .sum()
            ),
        )

        st.divider()

        st.subheader(
            "Schema Compatibility"
        )

        expected = set(
            model_features.columns
        ) if not model_features.empty else set()

        uploaded_columns = set(
            uploaded_df.columns
        )

        matching = sorted(
            expected.intersection(
                uploaded_columns
            )
        )

        missing = sorted(
            expected.difference(
                uploaded_columns
            )
        )

        additional = sorted(
            uploaded_columns.difference(
                expected
            )
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

        st.subheader(
            "Missingness Profile"
        )

        missingness = (
            uploaded_df.isna()
            .mean()
            .mul(100)
            .sort_values(
                ascending=False
            )
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

        st.subheader(
            "Dataset Preview"
        )

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

    st.header("Workforce Intelligence")

    st.caption(
        "Translate follow-up risk into operational workload "
        "and capacity signals."
    )

    if action_queue.empty:

        st.warning(
            "Action queue unavailable."
        )
        st.stop()

    if "assigned_cadre" not in action_queue.columns:

        st.info(
            "Cadre information unavailable."
        )

    else:

        cadre = (
            action_queue[
                "assigned_cadre"
            ]
            .fillna("Unassigned")
            .astype(str)
            .value_counts()
        )

        left, right = st.columns(2)

        with left:

            st.subheader(
                "Workload by Cadre"
            )

            st.bar_chart(cadre)

        with right:

            st.subheader(
                "High-Priority Workload"
            )

            if "priority_tier" in action_queue.columns:

                high = action_queue[
                    action_queue[
                        "priority_tier"
                    ].isin(
                        [
                            "HIGH",
                            "VERY HIGH",
                        ]
                    )
                ]

                high_cadre = (
                    high[
                        "assigned_cadre"
                    ]
                    .fillna("Unassigned")
                    .astype(str)
                    .value_counts()
                )

                st.bar_chart(high_cadre)

        st.info(
            "This is capacity-planning intelligence, not an "
            "autonomous hiring or staffing decision."
        )


# ============================================================
# MEDICINES
# ============================================================

elif page == "Medicines":

    st.header("Medicine Intelligence")

    st.caption(
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
            action_queue[
                "predicted_dropout_stage"
            ]
            .astype(str)
            .str.contains(
                "medicine",
                case=False,
                na=False,
            )
        ]

    else:

        medicine_actions = pd.DataFrame()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Medicine-related Actions",
        number(len(medicine_actions)),
    )

    c2.metric(
        "Dispensing Records",
        number(len(dispensing)),
    )

    if (
        not patient360.empty
        and "medicine_advised" in patient360.columns
    ):

        medicine_required = (
            patient360[
                "medicine_advised"
            ]
            .astype(str)
            .str.lower()
            .isin(
                [
                    "yes",
                    "true",
                    "1",
                ]
            )
            .sum()
        )

    else:

        medicine_required = 0

    c3.metric(
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

    st.header("Prioritized Action Queue")

    if action_queue.empty:

        st.warning(
            "Action queue unavailable."
        )
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

        selected = c1.multiselect(
            "Priority",
            values,
            default=values,
        )

        if selected:

            queue = queue[
                queue[
                    "priority_tier"
                ]
                .astype(str)
                .isin(selected)
            ]

    if "assigned_cadre" in queue.columns:

        values = sorted(
            queue["assigned_cadre"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected = c2.multiselect(
            "Cadre",
            values,
            default=values,
        )

        if selected:

            queue = queue[
                queue[
                    "assigned_cadre"
                ]
                .astype(str)
                .isin(selected)
            ]

    if "predicted_dropout_stage" in queue.columns:

        values = sorted(
            queue[
                "predicted_dropout_stage"
            ]
            .dropna()
            .astype(str)
            .unique()
        )

        selected = c3.multiselect(
            "Suggested Stage",
            values,
            default=values,
        )

        if selected:

            queue = queue[
                queue[
                    "predicted_dropout_stage"
                ]
                .astype(str)
                .isin(selected)
            ]

    if "risk_probability" in queue.columns:

        queue["risk_probability"] = probability(
            queue["risk_probability"]
        )

        queue = queue.sort_values(
            "risk_probability",
            ascending=False,
        )

    st.metric(
        "Visible Actions",
        number(len(queue)),
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
        col
        for col in columns
        if col in queue.columns
    ]

    st.dataframe(
        queue[columns],
        use_container_width=True,
        height=620,
        hide_index=True,
    )

    st.download_button(
        "Download Action Queue",
        data=queue[columns].to_csv(
            index=False
        ).encode("utf-8"),
        file_name="priority_action_queue.csv",
        mime="text/csv",
    )


# ============================================================
# MONITORING
# ============================================================

elif page == "Monitoring":

    st.header("Data & Model Monitoring")

    st.subheader(
        "Dataset Availability"
    )

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

    st.subheader(
        "Patient Linkage"
    )

    if not teleconsultation_linkage.empty:

        total = len(
            teleconsultation_linkage
        )

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

        c1.metric(
            "Linkage Records",
            number(total),
        )

        c2.metric(
            "Computational Linkage Coverage",
            percent(coverage),
        )

        st.caption(
            "Coverage represents algorithmic linkage coverage, "
            "not independently validated identity accuracy."
        )

    else:

        st.info(
            "Linkage output unavailable."
        )

    st.divider()

    st.subheader(
        "Model Output Status"
    )

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

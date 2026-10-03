
# Data-Driven Follow-Up Assurance for Rural Teleconsultations

## 1. Problem Understanding

Rural teleconsultation data is distributed across multiple healthcare systems. This makes it difficult to maintain a complete patient history, identify patients at risk of Lost to Follow-Up (LTFU), understand the reasons behind the risk, and prioritize follow-up actions.

The solution focuses on connecting fragmented records, predicting LTFU risk, explaining the risk, and converting predictions into practical follow-up actions.

---

## 2. Dataset

The solution uses the provided synthetic healthcare dataset containing approximately 5,000 patients and multiple operational healthcare data sources.

Core datasets include:

- Patient 360 reference
- Teleconsultations
- NCD screening
- Prescriptions
- Medicine dispensing
- Medicine stock
- Laboratory tests
- Follow-up visits
- Visit history
- Outreach actions
- Facility reference
- Geography reference
- Episode outcomes

Development data contains known outcomes, while evaluation data contains episodes where outcomes are unavailable.

---

## 3. Data Audit and Standardization

The data was audited for:

- Missing values
- Duplicate records
- Data types
- Date ranges
- Cohorts
- Identifiers
- Data consistency

Names, villages, blocks, districts, gender, age, dates, and other fields were standardized before analysis.

---

## 4. Patient Record Linkage

Different healthcare systems contain different patient identifiers.

The solution links records to the canonical patient reference using:

- Name
- Village
- Block
- District
- Gender
- Age

`RapidFuzz` is used for fuzzy matching.

The resulting linkage information is stored in:

`teleconsultation_linkage.csv`

The reported 100% linkage coverage represents algorithmic matching coverage, not independently validated identity accuracy.

---

## 5. Patient 360

Linked records are combined into a consolidated Patient 360 view.

This brings together information from consultations, prescriptions, medicines, laboratory tests, follow-ups, outreach, facilities, and geography.

Output:

`patient360_development.csv`

This gives healthcare workers a more complete view of an individual's care journey.

---

## 6. Healthcare Analysis

The analysis examined:

- Consultation mode
- Connectivity
- Travel distance
- Care requirements
- NCD conditions
- Vulnerability indicators
- Follow-up requirements
- Dropout stages

The analysis indicates that longer travel distance and higher care requirements are important operational signals associated with LTFU in the development data.

These are associations, not causal conclusions.

---

## 7. Care Journey Analysis

The care journey was analysed across key stages:

- Diagnostic test completion
- Medicine collection
- Review attendance
- Completion of care

This helps identify where a patient may require additional follow-up support.

---

## 8. Feature Engineering

Features were created using information available at the end of the teleconsultation.

Important features include:

- Age
- Distance
- Consultation duration
- Review due period
- Medicine requirement
- Test requirement
- Review requirement
- Care requirement count
- Previous consultations
- Previous care requirements
- Connectivity
- Digital access
- Distance indicators
- Vulnerability indicators
- Temporal features

---

## 9. Leakage Prevention

The prediction point is defined at the end of the teleconsultation.

Future information such as future dispensing, laboratory completion, follow-up attendance, outreach, and final outcomes is excluded from model inputs.

Historical patient information is calculated chronologically.

---

## 10. LTFU Machine Learning

Three models were evaluated:

- Logistic Regression
- Random Forest
- Extra Trees

A temporal validation approach was used.

The models were evaluated using:

- ROC-AUC
- PR-AUC
- Accuracy
- Precision
- Recall
- F1 Score

Logistic Regression achieved the highest PR-AUC among the evaluated models and was selected for the final risk workflow.

---

## 11. Risk Prediction and Explainability

Each evaluation episode receives an operational risk score and risk tier:

- Low
- Medium
- High
- Very High

The solution also identifies important risk factors instead of showing only a score.

Key factors include care requirements, review requirements, medicine requirements, distance, complex care, previous care requirements, and digital access.

Outputs include:

- `evaluation_predictions.csv`
- `feature_importance.csv`
- `risk_tier_validation.csv`

---

## 12. Suggested Follow-Up Stage

The system provides a **Suggested Stage** based on available care requirements and episode information.

Examples include:

- Test completion
- Medicine collection
- Review attendance
- General follow-up

This is an operational rule-based suggestion and not a trained clinical classifier.

---

## 13. Medicine Stock → Patient Impact

Medicine information is connected with patient-level follow-up intelligence.

The application considers available:

- Prescription data
- Dispensing data
- Medicine stock information
- Facility information
- Patient risk information

This helps identify situations where medicine availability or collection may require operational attention.

---

## 14. Care-Burden Intelligence

A Care-Burden Score is used for operational prioritization.

It considers factors such as:

- Number of care requirements
- Medicine requirement
- Test requirement
- Review requirement
- Distance
- Complex care
- Previous care requirements

The score supports workforce prioritization and does not represent clinical severity.

---

## 15. Follow-Up Dependency and Next-Best Action

The system converts patient context into practical operational actions.

Examples include:

- Prioritize medicine follow-up
- Prioritize diagnostic test follow-up
- Prioritize review attendance
- Prioritize outreach
- Continue monitoring

These recommendations are rule-based operational guidance and are not clinical treatment decisions.

---

## 16. Human-Centred Example

Consider a patient living in a remote village who has:

- A long distance to the facility
- Medicine requirements
- A pending diagnostic test
- A scheduled review
- Higher overall care burden
- High predicted LTFU risk

Instead of giving the healthcare worker only a risk score, the system provides the patient's context, explains the important risk factors, identifies the likely follow-up stage, and suggests the next operational action.

This converts **prediction into practical follow-up support** for CHOs and ASHAs.

---

## 17. Action Queue

The final action queue prioritizes cases using:

- Patient information
- Episode information
- Risk score
- Risk tier
- Risk reasons
- Suggested stage
- Care burden
- Recommended action

Output:

`action_queue.csv`

This allows limited healthcare-worker time to be directed towards cases requiring attention.

---

## 18. Key Findings

The analysis identified several operational findings:

- LTFU is substantial within the development cohort.
- Longer travel distance is associated with higher observed LTFU.
- Patients with multiple care requirements show higher observed LTFU.
- Medicine, test, and review requirements create additional follow-up dependencies.
- Patient history provides useful context for risk assessment.
- A risk score alone is insufficient for field operations; healthcare workers need reasons and recommended actions.

---

## 19. Proposed Solution

The solution combines:

**Patient 360 + LTFU Risk Prediction + Explainability + Care-Journey Intelligence + Action Prioritization**

The main objective is to move from fragmented healthcare records to actionable follow-up intelligence.

---

## 20. Recommendations

Based on the analysis, the solution recommends:

- Prioritize patients using risk and care burden.
- Consider travel distance when planning outreach.
- Track medicine, test, and review dependencies.
- Provide explainable reasons with every risk prediction.
- Give CHOs and ASHAs practical next actions rather than only risk scores.
- Maintain audit trails and role-based access for sensitive healthcare data.
- Validate linkage quality before production deployment.
- Monitor model performance when new regional data becomes available.

---

## 21. Streamlit Application

The final application is implemented using Streamlit.

The dashboard provides:

- Overview
- Patient 360
- Risk AI
- Care Journey
- Action Queue
- Workforce Intelligence
- Medicine Impact
- Care-Burden Intelligence
- Next-Best Action
- Monitoring
- Data Hub

Main application:

`outputs/app.py`

---

## 22. Technology Stack

### Data and Programming

- Python
- Pandas
- NumPy
- Regular Expressions
- RapidFuzz

### Machine Learning

- Scikit-learn
- Logistic Regression
- Random Forest
- Extra Trees
- Temporal Validation
- Risk Tiering
- Feature Importance

### Visualization and Application

- Streamlit
- Plotly
- Matplotlib

### Development and Version Control

- Jupyter Notebook
- Git
- GitHub

### Cloud and Deployment

- Streamlit Cloud
- Docker
- AWS EC2
- AWS ECR

The application was also containerized and tested on AWS EC2 using the Docker image. The EC2 deployment was successfully validated as an additional cloud deployment path.

---

## 23. Implementation

The complete data science workflow is implemented through:

```text
01_data_audit.ipynb
02_patient360_eda.ipynb
03_feature_engineering.ipynb
04_ltfu_model.ipynb
05_explainability_actions.ipynb
06_output.ipynb
````

The notebooks generate the required CSV outputs, which are consumed by the Streamlit application.



## 24. Deployment and Regional Reusability

The Feature Branch contains both the Streamlit application and the `Dockerfile`.

The solution supports:

* GitHub-based version control
* Streamlit Cloud deployment
* Docker-based deployment
* AWS cloud deployment when required

The same application and packaged Docker image can be reused for other regions.

Only the **regional data adaptation and corresponding data mapping** need to change. The core Patient 360, prediction, explainability, care-burden, action-generation, and application layers remain reusable.

**Build once, package once, and reuse across regions; adapt the regional data layer for each deployment.**

For organizations requiring AWS infrastructure, the same containerized application can be deployed using AWS services such as EC2 and ECR.

---

## 25. Project Structure

```text
caseathon/
│
├── README.md
│
└── case-a-thon_dset/
    ├── Dockerfile
    ├── requirements.txt
    │
    ├── Infinum_2026_Candidate_Dataset_Pack/
    │
    ├── notebooks/
    │   ├── 01_data_audit.ipynb
    │   ├── 02_patient360_eda.ipynb
    │   ├── 03_feature_engineering.ipynb
    │   ├── 04_ltfu_model.ipynb
    │   ├── 05_explainability_actions.ipynb
    │   └── 06_output.ipynb
    │
    └── outputs/
        ├── app.py
        ├── action_queue.csv
        ├── evaluation_intelligence.csv
        ├── evaluation_predictions.csv
        ├── feature_importance.csv
        ├── feature_metadata.csv
        ├── model_comparison.csv
        ├── model_features.csv
        ├── patient360_development.csv
        ├── risk_tier_validation.csv
        ├── teleconsultation_linkage.csv
        └── EDA output files
```

## Final Outcome

The project provides a practical, data-driven approach to rural follow-up assurance by connecting patient records, identifying LTFU risk, explaining the risk, understanding care dependencies, and converting intelligence into actionable follow-up priorities.

The focus is not only **predicting who may be lost to follow-up**, but helping healthcare workers understand **why the patient may be at risk and what operational action can be considered next**.


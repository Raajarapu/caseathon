# Data-Driven Follow-Up Assurance for Rural Teleconsultations

## Infinum 2026 Case-a-thon

A decision-support prototype for identifying patients at risk of loss to follow-up and helping healthcare workers take timely, actionable follow-up steps.

---

## 1. Problem Statement

Teleconsultation improves access to healthcare, but completing a teleconsultation does not necessarily mean that the patient's care journey is complete.

After a consultation, a patient may still need:

- Medicine collection
- Diagnostic tests
- Follow-up review
- Additional outreach

In rural settings, fragmented healthcare records, long travel distances, limited digital access, connectivity constraints, and limited health-worker time can make it difficult to identify which patients need attention first.

The core challenge is:

> How can fragmented rural healthcare data be transformed into actionable intelligence that helps healthcare workers identify patients at risk of loss to follow-up and intervene before care is interrupted?

---

# 2. Our Solution

We developed a data-driven follow-up assurance prototype that:

- Integrates fragmented healthcare records
- Links records to a canonical patient identity
- Creates a Patient 360 view
- Estimates LTFU risk
- Explains important risk signals
- Identifies a suggested follow-up stage
- Generates a prioritized action queue

The solution is designed as a decision-support system for CHOs and ASHAs.

It does not replace healthcare workers or make clinical decisions.

It helps answer four practical questions:

1. Who needs attention?
2. Why does the patient need attention?
3. Where is the care journey likely to break?
4. What should the healthcare worker do next?

---

# 3. Round 1: Understanding the Problem

Our Round 1 analysis focused on understanding the fragmented rural healthcare ecosystem, patient linkage challenges, care-continuity gaps, and the operational needs of healthcare workers.

The key design principles were:

- Build a unified Patient 360
- Predict LTFU before it occurs
- Make predictions explainable
- Convert predictions into actionable follow-up
- Account for rural access constraints
- Keep healthcare workers in the decision loop

These principles guided the Round 2 implementation.

---

# 4. Round 2: Working Prototype

Round 2 converts the problem analysis into a working analytical and decision-support prototype.

The implementation follows five practical stages:

### Connect

Integrate fragmented healthcare records through patient linkage.

### Predict

Estimate the probability that a teleconsultation episode may be lost to follow-up.

### Explain

Identify important factors associated with the predicted risk.

### Prioritize

Organize episodes into operational risk tiers.

### Act

Provide a suggested follow-up stage, recommended action, and assigned cadre.

The objective is to move from prediction to intervention.

---

# 5. Dataset

The case dataset contains:

- 5,000 synthetic patients
- 5,516 teleconsultation episodes
- Multiple healthcare-related operational datasets
- Development and evaluation cohorts

The development cohort contains episodes with known outcomes and is used for analysis and model development.

The evaluation cohort contains later episodes for which outcome labels are not provided.

The dataset is synthetic and is used only for the case competition prototype.

---

# 6. Patient Linkage

Different operational systems contain different source-level patient identifiers.

The prototype performs multi-signal patient linkage using available information including:

- Name similarity
- Village
- Block
- District
- Gender
- Age

Text values are normalized before matching, and fuzzy matching is used where exact matching is not possible.

The final linkage process achieved:

> 5,516 / 5,516 teleconsultation episodes mapped to a canonical patient record.

This represents **100% computational linkage coverage**.

It should not be interpreted as 100% independently validated identity accuracy because the dataset does not provide a complete ground-truth crosswalk for validating every match.

---

# 7. Key Findings

## 7.1 LTFU is a major care-continuity gap

Among the 4,132 development episodes:

- 2,144 completed the care journey
- 1,988 were classified as lost to follow-up
- Overall LTFU rate: **48.11%**

This demonstrates that teleconsultation alone does not guarantee continuity of care.

The key opportunity is to identify elevated-risk episodes early enough for proactive intervention.

---

## 7.2 LTFU occurs at identifiable stages

The development data identifies three operational dropout points:

| Dropout Point | Episodes |
|---|---:|
| Medicine not collected | 1,170 |
| Review not attended | 543 |
| Test not completed | 275 |

This shows that LTFU is not a single uniform problem.

Different patients may require different interventions depending on where their care journey is likely to break.

---

## 7.3 Distance is associated with observed LTFU

Observed LTFU rates across distance groups were:

| Distance | Observed LTFU |
|---|---:|
| ≤2 km | 20.00% |
| 2–5 km | 34.60% |
| 5–10 km | 37.50% |
| >10 km | 51.28% |

Longer distance is associated with higher observed LTFU in the development data.

This is an observational association and should not be interpreted as proof that distance independently causes LTFU.

---

## 7.4 Additional care requirements are associated with higher LTFU

### Medicine

- Medicine advised: **54.33%**
- No medicine advised: **27.79%**

### Diagnostic test

- Test advised: **57.92%**
- No test advised: **42.62%**

### Review

- Review advised: **54.04%**
- No review advised: **35.53%**

This indicates that additional post-consultation requirements can represent important points where continuity of care may be interrupted.

---

# 8. Machine Learning Approach

The LTFU prediction pipeline is designed around the prediction point:

> **End of the teleconsultation**

Only information available at or before this point is used for prediction.

Future information such as:

- Medicine dispensing
- Future laboratory completion
- Future follow-up visits
- Future outreach actions
- Final outcome labels

is excluded from the model features.

This helps reduce temporal leakage.

---

# 9. Model Features

The model uses multiple categories of features.

### Consultation characteristics

- Age
- Consultation duration
- Distance to facility
- Review due days

### Care requirements

- Medicine required
- Test required
- Review required
- Care requirements count
- Complex care episode

### Historical context

- Previous teleconsultations
- Previous care requirements
- Consultation frequency
- Previous consultation history

### Access and vulnerability indicators

- Long distance
- Poor connectivity
- Low digital access
- Elderly living alone

### Temporal features

- Consultation month
- Day of week
- Weekend indicator

---

# 10. Model Comparison and Validation

Multiple machine-learning models are evaluated using a temporal validation approach.

The development data is ordered chronologically and separated into training and validation periods.

Evaluation includes:

- ROC-AUC
- PR-AUC
- Accuracy
- Precision
- Recall
- F1 score

PR-AUC is particularly useful for assessing performance when the positive class is important for operational prioritization.

The selected model is then retrained using the available development data and used to generate evaluation-cohort risk predictions.

---

# 11. Explainability

The prototype does not provide only a risk score.

Feature-importance analysis identified the following leading model signals:

| Feature | Importance |
|---|---:|
| Care requirements count | 12.43% |
| Review required | 9.75% |
| Medicine required | 8.63% |
| Distance | 8.11% |
| Complex care episode | 7.05% |
| Long distance | 5.34% |
| Previous care requirements | 5.10% |
| Duration | 4.60% |
| Review due days | 4.47% |
| Low digital access | 4.21% |

The strongest signals are concentrated around care complexity, required follow-up, and access constraints.

Feature importance describes model behavior and does not establish causal relationships.

---

# 12. Risk Intelligence

The prototype converts predicted probabilities into operational risk tiers:

| Risk Tier | Operational Purpose |
|---|---|
| LOW | Routine monitoring |
| MEDIUM | Monitor and consider follow-up |
| HIGH | Prioritized follow-up |
| VERY HIGH | Immediate prioritization for proactive outreach |

The purpose of risk tiers is to help healthcare workers manage limited follow-up capacity.

---

# 13. From Prediction to Action

A risk score alone is not enough for operational use.

The prototype therefore combines:

**Risk + Reason + Suggested Stage + Recommended Action + Cadre**

For example, a high-risk episode may show:

### Risk

89.2%

### Priority

VERY HIGH

### Suggested Stage

Medicine not collected

### Reasons

- Long distance to facility
- Medicine collection required
- Diagnostic test required
- Follow-up review required

### Recommended Action

Verify medicine availability and coordinate collection support.

### Assigned Cadre

ASHA

This demonstrates how a model output can be transformed into an operational follow-up task.

---

# 14. Suggested Follow-up Stage

The current prototype provides an operational stage suggestion based on the care requirements recorded at the consultation.

Examples include:

- Medicine not collected
- Review not attended
- Test not completed
- Care journey monitoring

This component is a rule-based operational suggestion and is **not a separately trained ML dropout-stage classifier**.

This distinction is maintained to avoid overstating model capability.

---

# 15. Prioritized Action Queue

The Action Queue converts model outputs into a practical worklist.

Each episode contains:

- Episode ID
- Patient ID
- Risk probability
- Priority tier
- Reason
- Suggested dropout stage
- Recommended action
- Assigned cadre

This changes the operational question from:

> "Which patients should I call?"

to:

> "Which patients need attention first, why, and what should I do next?"

---

# 16. Prototype

The Streamlit prototype contains four views.

## Overview

Provides:

- Development episode count
- LTFU episode count
- LTFU rate
- Observed dropout points
- Model comparison

## Patient 360

Provides:

- Patient information
- Consultation history
- Distance
- Connectivity
- Medicine requirement
- Test requirement
- Review requirement
- Development outcome information

## Risk Intelligence

Provides:

- Risk probability
- Priority tier
- Suggested stage
- Risk reasons
- Recommended action
- Assigned cadre

## Action Queue

Provides a prioritized list of episodes requiring attention.

---

# 17. Operational Recommendations

## 1. Start follow-up planning immediately after consultation

Risk assessment should occur at the end of the consultation instead of waiting until a patient is already lost to follow-up.

## 2. Use stage-specific interventions

Different dropout points require different responses.

Medicine-related risk can trigger medicine availability and collection support.

Review-related risk can trigger reminders and review coordination.

Test-related risk can trigger test availability and completion support.

## 3. Prioritize limited health-worker capacity

CHOs and ASHAs should receive a prioritized action queue rather than an unstructured list of patients.

## 4. Support difficult-to-reach patients

Distance and digital-access indicators can help identify patients who may require more proactive or assisted follow-up.

## 5. Keep healthcare workers in the loop

The system provides recommendations and explanations.

The final operational decision remains with the healthcare worker.

---

# 18. Rural Deployment Considerations

A production implementation should account for rural operating conditions.

### Low connectivity

Support lightweight data exchange and synchronization when connectivity becomes available.

### Low-end devices

The field interface should remain simple and focus on:

- Patient
- Risk
- Reason
- Next action
- Follow-up status

### Limited workforce

The system should prioritize actionable high-risk episodes instead of overwhelming healthcare workers with every patient.

### Privacy and security

A production implementation should include:

- Role-based access control
- Minimum necessary data access
- Secure data transmission
- Audit trails
- Appropriate data retention
- Fairness monitoring
- Explainability

---

# 19. Technical Pipeline

The project is organized into the following notebooks:

```text
01_data_audit.ipynb
    Data audit and patient linkage

02_patient360_eda.ipynb
    Patient 360 construction and exploratory analysis

03_feature_engineering.ipynb
    Leakage-safe feature engineering

04_ltfu_model.ipynb
    LTFU model development and temporal validation

05_explainability_actions.ipynb
    Explainability, risk reasons and action queue

06_output.ipynb
    Reserved for final output work

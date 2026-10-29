# Phishing Detection ML --- System Architecture

**Purpose:** Technical reference for the project report, viva, and
comparison with published research.

> **Implementation note:** This document describes the intended
> architecture based on the project details currently available. Verify
> every component against the active code before presenting it as
> implemented. In particular, confirm which prediction pipeline
> `app/app.py` calls, the exact numeric/NLP fusion formula, and whether
> trusted-domain matching affects the final prediction or is displayed
> only as metadata.

## 1. System overview

The application accepts a URL, processes it in the backend, obtains a
model probability, converts that probability into a risk score, and
returns the result to the web interface.

``` mermaid
flowchart TD
    A[User enters URL] --> B[Web interface]
    B --> C[POST /predict]
    C --> D[FastAPI backend]
    D --> E[Input validation and URL processing]
    E --> F[Active prediction pipeline]
    F --> G[Final probability]
    G --> H[Decision threshold]
    G --> I[Risk score calculation]
    E --> J[Trusted-domain lookup, if enabled]
    H --> K[JSON response]
    I --> K
    J --> K
    K --> L[Dashboard displays results]
```

The diagram is a conceptual overview. Confirm the exact order and
integration of components from the current implementation.

## 2. Main components

### 2.1 Frontend / dashboard

Responsibilities: - Accept a URL from the user. - Send the URL to the
backend using an HTTP request. - Display the returned classification,
probability, risk score, and other available diagnostic fields. - Show
trusted-domain information when that field is returned by the API.

**Technologies:** HTML, CSS, and JavaScript, based on the interface
described during development.

### 2.2 API layer

**Framework:** FastAPI.

The application exposes a prediction endpoint:

-   `POST /predict`
-   Example request body:

``` json
{
  "url": "https://example.com"
}
```

The API validates the request format, calls the configured prediction
function, calculates risk information, and returns a JSON response. API
documentation is normally available at `/docs` while the server is
running.

**Entry-point check:** Previously shared project code showed
`app/app.py` importing `predict_url` from `src.predict` and `Calc_Risk`
from `src.risk_scoring`. Confirm that this remains the active code path.
A separate fusion module does not affect predictions unless the API
calls it.

### 2.3 URL preprocessing and feature extraction

The URL is prepared for model inference. Depending on the active
implementation, preprocessing may include URL normalization, hostname
extraction, and calculation of structural or text features.

Potential numeric features include URL length, hostname characteristics,
counts of selected characters, and other structural indicators. Include
only features confirmed in the actual feature-extraction code in the
final report.

### 2.4 Numeric model

The numeric model uses structured URL features to produce a model output
or probability. The model type, exact feature list, training dataset,
and saved artifact path should be documented from the training code.

Numeric patterns are indicators rather than proof of maliciousness.
Legitimate URLs can also be long or contain unusual characters.

### 2.5 NLP model

The NLP component uses text-based representation of URLs to identify
learned patterns. If the current implementation uses TF-IDF, document
the vectorizer settings and classifier from the training script. Do not
claim TF-IDF or a particular classifier unless verified in the active
pipeline.

### 2.6 Fusion layer

The intended fusion design combines outputs from numeric and NLP
components. The actual formula, weights, and calibration must be taken
from the active prediction code.

For an illustrative weighted fusion:

`P_fusion = w_numeric * P_numeric + w_text * P_text`

where `P_numeric` and `P_text` are model outputs, and the weights
describe their contributions. For a weighted average, weights should be
non-negative and sum to one.

This equation is illustrative; it is not evidence that the current API
uses this exact formula. Evaluate numeric-only, NLP-only, and combined
systems separately to test whether fusion improves results.

### 2.7 Trusted-domain matching

A trusted-domain component can compare the normalized hostname against a
configured set of recognized domains and exclusions.

Important constraints: - A match is not a guarantee that a page is
safe. - No match does not mean a site is malicious. - Subdomains,
lookalike domains, redirects, and incomplete lists require careful
handling. - Broad wildcard rules should not automatically trust every
hostname containing government-related text. - Record whether this
component changes the final prediction, changes the threshold, or only
provides a dashboard indicator. Verify this behavior in code.

### 2.8 Risk scoring and decision threshold

The risk score is calculated from a probability:

`Risk Score = 100 * P`

The classification threshold and risk-level bands are separate settings.
A threshold determines the classification decision; score bands
determine the human-readable risk label.

Proposed display bands discussed during development: - 0--19.9: Very
Low - 20--39.9: Low - 40--69.9: Medium - 70--100: High

These are application-defined display bands, not an industry-standard
risk scale. Confirm that the revised risk-scoring code is active before
documenting these as current behavior. Verify whether the API passes the
fusion probability or another model probability into the scoring
function.

## 3. API data flow

1.  The user submits a URL through the interface.
2.  The frontend sends a `POST /predict` request.
3.  FastAPI validates the JSON request.
4.  The active prediction function processes the URL and returns a
    probability or prediction result.
5.  The risk-scoring function calculates the risk score and risk label.
6.  Trusted-domain metadata or model diagnostics are added if
    implemented.
7.  FastAPI returns a JSON response.
8.  The frontend updates the dashboard with the returned values.

The response schema must be taken from the active API implementation.
Fields such as `Numeric_Probability`, `NLP_Probability`,
`Trusted_Domain`, `Model`, `Numeric_Weight`, and `Threshold` should be
documented only if the running endpoint actually returns them.

## 4. Model evaluation plan

To compare this system with a published paper, evaluate the models on
clearly documented and appropriately separated datasets.

Recommended metrics: - **Accuracy:** fraction of all predictions that
are correct. - **Precision:** fraction of predicted phishing samples
that are actually phishing. - **Recall:** fraction of actual phishing
samples that are detected. - **F1-score:** harmonic mean of precision
and recall. - **False-positive rate:** fraction of legitimate samples
incorrectly flagged as phishing. - **Confusion matrix:** counts of true
positives, true negatives, false positives, and false negatives.

Fair-comparison requirements: 1. Document dataset source, size, class
distribution, and collection date if known. 2. Keep training data
separate from test data. 3. Prefer a domain-aware split to reduce
leakage from near-duplicate URLs or the same domains across splits. 4.
Compare numeric-only, NLP-only, and fused variants on the same test set.
5. Report the decision threshold and how it was selected. 6. Do not
treat metrics from different datasets as directly equivalent. 7. Record
false positives on legitimate websites and false negatives on phishing
samples. 8. Report measured results; do not invent or infer performance
numbers.

## 5. Known issue observed during testing

A test of `https://www.canada.ca/` was classified as phishing, and the
interface showed no trusted-domain match. The displayed numeric-model
probability was substantially higher than the NLP probability.

This is evidence of a test-case false positive, but it does not
establish the root cause. Inspect: - trusted-domain coverage and
hostname normalization; - numeric feature values generated for the
URL; - the active model and preprocessing artifacts; - the fusion
formula and model calibration; - the classification threshold; -
consistency between API response fields and dashboard labels.

A single test does not establish overall model performance. Add this URL
to a regression set and retest after changes.

## 6. Implementation verification checklist

-   [ ] Identify the exact FastAPI entry point and active prediction
    function.
-   [ ] Identify the exact numeric model and its feature list.
-   [ ] Identify the exact NLP vectorizer and classifier.
-   [ ] Confirm whether model fusion is called by the live API.
-   [ ] Record the fusion equation and weights from code.
-   [ ] Confirm the probability passed into risk scoring.
-   [ ] Confirm the active decision threshold and risk-level bands.
-   [ ] Confirm whether trusted-domain matching affects classification
    or is informational.
-   [ ] Record dataset provenance, preprocessing, and train/test split.
-   [ ] Measure accuracy, precision, recall, F1-score, and
    false-positive rate.
-   [ ] Test legitimate URLs and labeled phishing URLs.
-   [ ] Record software versions and required model artifacts.

## 7. Suggested report outline

1.  Abstract
2.  Introduction and problem statement
3.  Related work: the selected published paper
4.  Proposed system architecture
5.  Dataset and preprocessing
6.  Numeric model and NLP model
7.  Fusion method and threshold selection
8.  Experimental setup
9.  Results and comparison with the published paper
10. Error analysis and limitations
11. Conclusion and future work
12. References

## 8. Research integrity note

Do not claim that this system outperforms a published paper until a
reproducible evaluation supports the claim. If datasets or protocols
differ, state that limitation explicitly. A defensible report can
identify improvements in design or deployment while honestly reporting
cases where the model does not improve.

# 🧠 Neural Choice Decoding from IBL Brain-Wide Map Data

Predicting an animal's left/right choice from neural population activity using the **International Brain Laboratory (IBL) Brain-Wide Map** dataset.

This project explores whether neural activity immediately before movement contains enough information to predict the animal's upcoming choice, and which neurons and brain regions carry the strongest choice-related information.

---

## 🎯 Research Question

> **Can neural activity predict whether the animal will make a left or right choice?**

We approach this question at three complementary levels:

1. **Whole-population decoding** — Can neural activity predict choice at all?
2. **Single-neuron modulation** — Which neurons respond differently before left and right choices?
3. **Brain-region analysis** — Which brain regions contain the strongest choice-related information?

---

## 📊 Dataset

The project uses preprocessed neural recordings from the **IBL Brain-Wide Map** dataset provided for the Neuromatch tutorial.

The main analysis uses neural activity aligned to:

```text
firstMove
```

where time `0` represents the animal's first detected movement.

For each trial, the neural activity is represented as:

```text
trials × neurons × time
```

The behavioral information is stored separately in the trial metadata.

The main target variable is:

```text
choice
```

representing the animal's left/right decision.

---

## 🧩 Feature Construction

To predict the animal's upcoming choice, we use neural activity from the:

```text
100 ms immediately before first movement
```

For every trial, activity is averaged across this time window.

This converts the neural activity from:

```text
trials × neurons × time
```

into:

```text
trials × neurons
```

Therefore:

- each **row** represents one trial,
- each **column** represents one recorded neuron,
- and each value represents that neuron's average pre-movement activity.

The resulting matrix is used as the model input:

```python
X = neural activity
y = left/right choice
```

---

## 🔎 Missing-Value Inspection

Before modeling, the neural feature matrix and target labels are checked for missing values.

In the current baseline dataset:

```text
NaNs in X: 0
NaNs in y: 0
```

Some trial metadata variables, particularly `contrastLeft` and `contrastRight`, contain NaN values.

These NaNs are related to the structure of the behavioral task rather than ordinary missing observations. Since these variables are not currently used as model features, no imputation is required for the main decoder.

---

## 🤖 Baseline Choice Decoder

The first model is intentionally simple:

### Logistic Regression

The trials are divided into training and test sets.

```text
Neural activity
      ↓
Train/Test Split
      ↓
Logistic Regression
      ↓
Left / Right prediction
```

The model is trained only on the training trials and evaluated on previously unseen test trials.

This provides a simple and interpretable baseline for determining whether neural population activity contains predictive information about choice.

---

## 🥸 Dummy Baselines

Prediction accuracy alone is not enough.

A classifier might achieve reasonable accuracy simply because one choice occurs more often than the other.

We therefore compare logistic regression with simple **Dummy Classifiers**, including:

- **Most Frequent** — always predicts the most common choice in the training data.
- **Stratified** — generates predictions according to the observed class distribution.

The important comparison is therefore not only:

```text
How accurate is Logistic Regression?
```

but:

```text
Does Logistic Regression perform better than trivial guessing strategies?
```

---

## 🧠 Choice Modulation Index

Decoding tells us whether the neural population can predict choice, but it does not directly tell us which individual neurons are related to the decision.

For each neuron, we therefore calculate a **Choice Modulation Index (Choice MI)**.

Let:

- \(FR_{right}\) = mean pre-movement activity during right-choice trials
- \(FR_{left}\) = mean pre-movement activity during left-choice trials

Then:

$$
\mathrm{Choice\ MI}
=
\frac{
\left|FR_{\mathrm{right}} - FR_{\mathrm{left}}\right|
}{
\left|FR_{\mathrm{right}} + FR_{\mathrm{left}}\right|
}
$$

A small Choice MI indicates similar activity for the two choices.

A larger Choice MI indicates a stronger difference between left- and right-choice trials.

---

## 🎲 Permutation Testing

A large Choice MI can still occur by chance.

To test whether the observed modulation is meaningful, we construct a null distribution by repeatedly shuffling the choice labels.

```text
Real neural activity + real choices
                ↓
          Observed Choice MI


Real neural activity + shuffled choices
                ↓
             Null MI
```

The observed Choice MI is compared with the shuffled distribution to obtain an empirical permutation p-value.

---

## 📉 Multiple-Comparison Correction

Because many neurons are tested simultaneously, some may appear significant simply by chance.

We therefore apply:

```text
Benjamini-Hochberg FDR correction
```

This allows us to identify neurons whose choice-related modulation remains significant after accounting for multiple statistical tests.

---

## 🗺️ Brain-Region Analysis

Each recorded neuron is associated with an anatomical brain-region acronym.

We group neurons by brain region and summarize measures such as:

- number of recorded neurons,
- median Choice MI,
- mean Choice MI,
- fraction of strongly modulated neurons,
- fraction of statistically significant neurons.

This allows us to move from:

```text
Which neurons are choice-related?
```

to:

```text
Which brain regions contain stronger choice-related signals?
```

---

## 🌍 Brain-Wide Choice Modulation

The initial analysis is performed on a single probe insertion.

We then extend the same Choice MI analysis across multiple probe insertions from the Brain-Wide Map dataset.

Importantly, Choice MI is calculated **within each recording session** before neurons are combined by anatomical region.

For descriptive brain-wide comparisons, regions with very small numbers of recorded neurons are excluded.

Following the general strategy of the reference tutorial, a minimum sampling threshold can be applied, for example:

```text
n_clusters >= 200
```

This reduces the influence of poorly sampled brain regions.

---

## 🔬 Region-Wise Choice Decoding

Choice MI measures neural modulation, while decoding asks a different question:

> **Can the neural activity from this brain region actually predict choice?**

We therefore train separate logistic regression models for individual:

```text
brain region × probe insertion
```

Instead of artificially combining neurons from unrelated recording sessions, decoding is performed independently within each insertion.

The results are then aggregated across insertions belonging to the same brain region.

---

## ⚙️ Feature Scaling

For region-wise logistic regression, neural features are standardized using:

```python
StandardScaler
```

To prevent data leakage:

```text
Scaler fit → training data only
Scaler transform → training + test data
```

The test set therefore has no influence on the preprocessing parameters learned during training.

---

## 📈 Region-Wise Evaluation

For every region/insertion combination, we calculate:

```text
Logistic Regression Accuracy
Dummy Accuracy
Accuracy Gain
```

where:

```text
Accuracy Gain =
Logistic Accuracy - Dummy Accuracy
```

This is particularly useful because raw accuracy can be influenced by class imbalance.

A positive accuracy gain indicates that neural activity from that region provides predictive information beyond the simple baseline.

---

## 🔗 Combining Modulation and Decoding

The final analysis combines two complementary measures.

### Neural Modulation

```text
Choice MI
Permutation Test
FDR-corrected significance
```

### Predictive Information

```text
Logistic Regression Accuracy
Dummy Accuracy
Accuracy Gain
```

A brain region becomes particularly interesting when it shows both:

```text
Strong choice-related modulation
              +
Strong decoding performance
```

This provides stronger evidence than relying on either modulation or prediction accuracy alone.

---

## 🧪 Analysis Pipeline

```text
IBL Brain-Wide Map Data
          │
          ▼
firstMove-aligned neural activity
          │
          ▼
Select -100 ms to 0 ms
          │
          ▼
Construct neural feature matrix X
          │
          ├─────────────────────────────┐
          │                             │
          ▼                             ▼
 Logistic Regression              Choice MI
          │                             │
          ▼                             ▼
    Test Accuracy              Permutation Test
          │                             │
          ▼                             ▼
   Dummy Baselines                  FDR
          │                             │
          └──────────────┬──────────────┘
                         │
                         ▼
                 Brain-Region Analysis
                         │
                         ▼
                Region-Wise Decoding
                         │
                         ▼
                Brain-Wide Comparison
```

---

## 📏 Evaluation Strategy

The main results are evaluated using several complementary criteria.

### Model level

- held-out test accuracy,
- comparison with dummy classifiers,
- improvement over baseline.

### Neuron level

- Choice Modulation Index,
- permutation p-values,
- FDR-corrected significance.

### Brain-region level

- median Choice MI,
- fraction of modulated neurons,
- number of recorded clusters,
- region-wise decoding accuracy,
- dummy accuracy,
- accuracy gain across insertions.

---

## 📌 Expected Final Outputs

The final project may include:

### 1. Choice Decoding Performance

A comparison between:

```text
Logistic Regression
vs.
Dummy Baselines
```

### 2. Choice-Modulated Neurons

A table containing:

```text
Neuron
Brain Region
Choice MI
Permutation p-value
FDR q-value
Significant / Not Significant
```

### 3. Brain-Region Ranking

A summary such as:

| Brain Region | Neurons | Median Choice MI | Significant Neurons | Decoder Accuracy | Dummy Accuracy | Accuracy Gain |
|---|---:|---:|---:|---:|---:|---:|
| Region A | ... | ... | ... | ... | ... | ... |
| Region B | ... | ... | ... | ... | ... | ... |
| Region C | ... | ... | ... | ... | ... | ... |

The goal is not only to determine whether choice can be decoded, but also to identify **where in the brain the strongest predictive information is found**.

---

## 🛠️ Main Technologies

- Python
- Jupyter Notebook
- NumPy
- pandas
- SciPy
- scikit-learn
- Matplotlib
- IBL ONE API
- IBL / Neuromatch Brain-Wide Map data

---

## 🚀 Current Project Status

The current implementation includes:

- [x] IBL data loading
- [x] Trial-level PSTH extraction
- [x] Pre-movement feature construction
- [x] Missing-value inspection
- [x] Train/test splitting
- [x] Logistic Regression decoder
- [x] Dummy baseline comparison
- [x] Choice Modulation Index
- [x] Permutation testing
- [x] FDR correction
- [x] Single-insertion region analysis
- [x] Brain-wide Choice MI analysis
- [x] Region-wise choice decoding
- [x] Feature scaling for regional models
- [x] Aggregation across probe insertions
- [x] Combined modulation + decoding analysis

Further work will focus on validating and visualizing the brain-wide results and improving the robustness of model comparisons.

---

## ⚠️ Notes and Limitations

This project currently uses a deliberately simple logistic regression model to provide an interpretable baseline.

Several aspects can be improved in future analyses, including:

- repeated cross-validation,
- confidence intervals for decoding performance,
- permutation-based decoder significance,
- controlling for differences in the number of neurons across regions,
- testing additional pre-movement time windows,
- investigating generalization across sessions or animals.

The current analysis should therefore be interpreted as an exploratory neural-decoding framework rather than a final causal explanation of decision-making.

---

## 🙏 Acknowledgements

This project is based on data from the **International Brain Laboratory (IBL)** Brain-Wide Map and builds on the structure and data-loading utilities provided in the **IBL / Neuromatch tutorial**.

We gratefully acknowledge the researchers and contributors who made these open neuroscience datasets and educational resources available.

---

## 📄 Project Summary

In one sentence:

> **We use neural activity immediately before movement to predict the animal's left/right choice and investigate which neurons and brain regions carry the strongest choice-related information.**

---

**Status:** Work in Progress 🚧  
**Field:** Computational Neuroscience · Neural Decoding · Machine Learning
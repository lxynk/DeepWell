<section class="title-slide">

# DeepWell
## Using spatial data to improve borehole siting in Kenya’s drylands

**From borehole records to spatially informed groundwater research**

</section>

---

## Why groundwater and why boreholes?

<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center">

<div>

<img src="/app/static/borehole_concept.svg" style="width:100%;max-height:390px;object-fit:contain">

</div>

<div style="font-size:0.78em;line-height:1.35">

**Water must be available, reliable, and safe**

In arid and semi-arid regions, groundwater is critical when surface sources are seasonal or scarce.

A borehole can fail: it may be dry, yield too little water, or produce water of unsuitable quality.

**The task**

Use existing borehole records and spatial data to reduce uncertainty before drilling.

**The challenge**

Insufficient records of unsuccessful drillings.

</div>
</div>

---

## Water access remains a global challenge

Progress has been made, but billions of people are still left behind.

![Global water-access statistics](/app/static/global_water_stats.svg)

Source: WHO/UNICEF Joint Monitoring Programme (JMP), 2025 assessment of 2024 data.

---

## The burden is unevenly distributed

Global averages hide large regional gaps

![Regional drinking-water coverage](/app/static/regional_coverage.svg)

These figures describe drinking-water services—not groundwater availability or borehole-drilling success.

Source: WHO/UNICEF JMP, 2025 report and regional estimates.

---

## DeepWell: a study in northern Kenya

### From the global challenge to a local test case

![Locator maps showing Kenya within Africa and the approximate Marsabit and Turkana study areas](/app/static/locator_maps.svg)

DeepWell investigates whether spatial and environmental data can help predict borehole outcomes before drilling, initially using records from **Marsabit and Turkana counties**.

---

## A costly decision under uncertainty

### Can spatial evidence improve the odds?

Amref Health Africa reports that current geological assessments in Kenya’s arid and semi-arid lands lead to successful drilling in around **60% of cases**.

That leaves substantial room to improve site selection and reduce the cost of unsuccessful drilling.

Source: Amref Health Africa

---

## Related work: a shared ambition

### Analytics for a Better World, Amref Health Africa, and ProRail

A parallel initiative is developing a decision-support tool combining satellite, geological, and other spatial data to identify more promising borehole locations in Kenya’s drylands.

Its stated ambition is to increase drilling success from around **60% to above 90%**. The public project description outlines the goal and planned work, but does not report numerical model-validation results or demonstrated field improvements.

DeepWell shares the broader research question. Transparent evaluation, comparable targets, and field validation are essential to judge what any approach achieves.

Source: https://analyticsbetterworld.org/impact/using-spatial-data-to-improve-borehole-drilling-in-kenyas-drylands

Analytics for a Better World, “Using spatial data to improve borehole drilling in Kenya’s drylands” (2026).

---

## What are we trying to predict?

### A useful system will need more than one model

A first step is to predict the likelihood that a proposed drilling location will result in a **successful borehole**.

A full-scale decision-support system should ultimately address three distinct outcomes:

- **Success:** is a borehole likely to hit water?
- **Quantity / yield:** how much water can it reliably supply?
- **Quality / salinity:** is the water suitable for its intended use?

These outcomes need appropriate labels, predictors, and evaluation methods. The current success model is only one component of that larger goal.

---

## The data

![Data cleaning funnel](/app/static/data_funnel.svg)

The original records required substantial cleaning and auditing:
- checking coordinates
- clarifying outcome labels
- identifying ambiguous or conflicting records
- handling missing information
- addressing the intrinsic disbalance in the data

---

## The features

![DeepWell feature groups](/app/static/feature_groups.svg)

The goal is not simply to add more variables. It is to test whether each feature group provides useful information beyond what the model already knows, in an attempt to describe the landscape around each location.

---

## The evaluation

Nearby boreholes can share environmental conditions. A random train/test split may therefore make a model appear more capable of generalising than it really is.

The workflow uses spatially aware cross-validation across geographically distinct groups.

- **Balanced accuracy:** performance across both classes, accounting for class imbalance.
- **Failure recall:** the share of labelled failures correctly identified.
- **Success recall:** the share of labelled successes correctly identified.
- **Fold-to-fold variation:** consistency across spatial partitions.

The reported 60% drilling success rate is not directly comparable to balanced accuracy. Evaluation must reflect the target, sample, and decision risk.

---

### The tuning

Optuna studies have been run for **Random Forest, XGBoost, and LightGBM** to find the best hyperparameter configurations.

![Optuna dashboard](/app/static/assets/obtuna_xgb.png)

---

## The results

![Best current model results](/app/static/model_results.svg)

**Best Random Forest parameters:** `max_depth=16`, `min_samples_leaf=4`, `min_samples_split=2`, `max_features=0.5`.

Feature set **E+T+A15+R+LUP** combines elevation, terrain, hydrological accumulation, distance to rivers, and a hydrological landform measure. The 300 labelled examples comprise 123 failures and 177 successes across 96 spatial groups, using 9 features.

These are the best current exploratory results, not a deployment-ready estimate. Dataset definitions, model selection, and spatial validation must remain consistent when comparing experiments.

---

## From analysis to exploration

### A map-based research interface

The DeepWell Spatial Explorer lets a user select a location and explore a model prediction using the environmental raster features available at that point.

It can help users:

- Understand how the model behaves across the landscape.
- Compare predictions with local environmental context.
- Investigate surprising results and potential failure cases.
- Inspect and communicate model outputs.

---

## The app can do more than display predictions

### A shared data resource—and a way to guide new data collection

![Potential data and analysis feedback loop](/app/static/app_learning_loop.svg)

**1. A practical place to store borehole information.** A shared, structured repository could help drilling teams record locations, outcomes, yield, water quality, and operational status. This requires data governance, quality checks, ownership rules, and appropriate access controls.

**2. Analysis-driven data collection.** Predictions and uncertainty could help identify locations where new investigations would be most informative—filling geographic gaps, testing uncertain predictions, or distinguishing between competing model explanations.

This creates a potential feedback loop: better records support better models, and analysis helps guide what data to collect next.

---

## Could the approach transfer to other regions?

### Transfer the workflow—not blindly the model

The workflow could be useful in other drylands, including parts of Africa, Asia, and Latin America: combine local records with spatial features, audit labels, define success for local decisions, and evaluate using geographically realistic validation.

**But a model trained in one region is not automatically transferable.**

- Geology, aquifer systems, and groundwater conditions differ.
- Borehole records may be sparse, biased, or inconsistent.
- Definitions of success, adequate yield, and acceptable water quality vary.
- Climate, infrastructure, drilling practices, and data availability differ.
- Independent local validation and often recalibration or retraining are needed.

Regional drinking-water coverage alone does not establish where this specific borehole-siting approach would be useful. Transferability must be tested in particular hydrogeological settings.

---

## What comes next?

### Build evidence before building confidence

1. **Strengthen labels:** document cleaning decisions and clarify ambiguous records.
2. **Establish independent baselines:** evaluate Rural Focus and NDMA separately.
3. **Add climate information:** investigate rainfall and aridity features.
4. **Improve evaluation:** examine spatial errors, uncertainty, and failure detection.
5. **Compare models:** continue controlled RF, XGB, and LGBM comparisons.
6. **Expand targets:** develop yield and water-quality/salinity models when suitable labels are available.
7. **Develop the app:** connect predictions with transparent explanations and structured borehole data.
8. **Guide data collection:** test whether uncertainty-aware sampling improves the evidence base.
9. **Test transferability:** assess new regions only where local data and validation are available.

The aim is to determine where spatial data provides dependable, actionable evidence—and where it does not.

---

# DeepWell
## Better evidence for better-informed drilling decisions

**A research prototype for more informed groundwater exploration.**

---

# Sources and notes

- WHO/UNICEF Joint Monitoring Programme (2025), *Progress on household drinking water, sanitation and hygiene 2000–2024*. https://washdata.org/reports/jmp-2025-wash-households
- UNICEF Data, *Drinking water*. https://data.unicef.org/topic/water-and-sanitation/drinking-water/
- Amref Health Africa / Analytics for a Better World (2026), *Using spatial data to improve borehole drilling in Kenya’s drylands*. https://analyticsbetterworld.org/impact/using-spatial-data-to-improve-borehole-drilling-in-kenyas-drylands
- Natural Earth, low-resolution country boundaries: https://www.naturalearthdata.com/

**Interpretation notes:** safely managed drinking water is a household service indicator, not a measure of groundwater potential. The ~60% figure is a reported drilling-success rate for Kenya’s arid and semi-arid lands, not a universal ML baseline. DeepWell metrics are exploratory. Initial dataset counts may differ from stricter prepared modelling subsets.

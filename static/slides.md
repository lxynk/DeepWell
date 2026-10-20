<style>
.reveal {
    font-size: 40px !important;
    color: #263746 !important;
    background-color: #ffffff !important;
}

/* Title Slide Alignments */
.reveal .slides section.title-slide,
.reveal .slides section.title-slide h1,
.reveal .slides section.title-slide h2,
.reveal .slides section.title-slide h3,
.reveal .slides section.title-slide p {
    text-align: left !important;
}

/* Slide Canvas Layout */
.reveal .slides section {
    box-sizing: border-box;
    padding: 24px 24px !important;
    text-align: left;
    line-height: 1.4;
}

/* Clear text shadow properties */
.reveal .slides section,
.reveal .slides section * {
    text-shadow: none !important;
}

/* Cleaned Typography & Structural Hierarchy */
.reveal h1,
.reveal h2,
.reveal h3,
.reveal h4 {
    color: #123047;
    font-weight: 650;
    text-transform: none;
    letter-spacing: -0.025em;
    text-align: left;
    line-height: 1.15;
    overflow-wrap: break-word;
}

.reveal h1 {
    font-size: 1.65em;
    margin: 0 0 0.45em;
}

.reveal h2 {
    font-size: 1.15em;
    color: #247BA0 !important; /* Unified DeepWell Blue Accent */
    margin: 0 0 0.65em;
}

.reveal h3 {
    font-size: 0.9em;
    margin: 0.6em 0 0.35em;
}

.reveal strong {
    color: #123047;
    font-weight: 700;
}

.reveal p,
.reveal li {
    font-size: 0.72em;
    line-height: 1.4;
    font-weight: 400;
}

.reveal p {
    margin: 0 0 0.8em;
}

.reveal ul,
.reveal ol {
    margin: 0.3em 0 0.8em;
    padding-left: 1.25em;
}

.reveal li {
    margin: 0 0 0.4em;
}

/* Consistent List Markers and Hyperlinks */
.reveal li::marker {
    color: #247BA0 !important;
}

.reveal a {
    color: #247BA0 !important;
    text-decoration: underline;
    text-underline-offset: 3px;
}

/* Images and Tables */
.reveal img {
    display: block;
    max-width: 100%;
    max-height: 43vh;
    width: auto;
    height: auto;
    object-fit: contain;
    margin: 0.5em auto 0.8em;
    border: 0;
    box-shadow: none;
    background: transparent;
}

.reveal table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.65em;
    margin: 0.6em 0;
}

.reveal th {
    background: #123047;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 0.45em 0.6em;
}

.reveal th,
.reveal td {
    padding: 0.45em 0.6em;
    border-bottom: 1px solid #DCE5E9;
}

.reveal tr:nth-child(even) td {
    background: #F3F7F8;
}

/* Blockquotes, Inline Code and Dividers */
.reveal blockquote {
    width: 90%;
    box-sizing: border-box;
    margin: 0.8em 0;
    padding: 0.65em 1em;
    background: #EEF5FA !important;
    border-left: 4px solid #247BA0 !important;
    box-shadow: none;
    font-style: normal;
    text-align: left;
}

.reveal blockquote p {
    margin: 0;
}

.reveal code {
    font-size: 0.85em;
    color: #247BA0 !important;
    background: #EEF5FA !important;
    padding: 0.1em 0.25em;
    border-radius: 3px;
}

.reveal hr {
    border: 0;
    border-top: 2px solid #DCE5E9;
    margin: 0.8em 0;
}

/* Navigation Mechanics */
.reveal .slide-number {
    color: #647783;
    background: transparent;
    font-size: 12px;
}

.reveal .progress {
    background-color: #247BA0 !important;
    height: 3px;
}

.reveal .controls,
.reveal .controls * {
    color: #247BA0 !important;
}

/* Responsive Mobile Layout Scaling */
@media (max-width: 700px) {
    .reveal .slides section {
        padding: 16px 20px !important;
    }

    .reveal h1 {
        font-size: 1.4em;
    }

    .reveal h2 {
        font-size: 1em;
    }

    .reveal p,
    .reveal li {
        font-size: 0.68em;
    }

    .reveal img {
        max-height: 34vh;
    }
}
</style>

<section class="title-slide">

<!-- Added min-height, margin, and width to stretch the container across the true vertical center of the viewport -->
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 28px; align-items: center; width: 100%; height: 100%; min-height: 75vh; margin: auto 0;">

<!-- Left Column: Content Block -->
<div style="font-size: 0.78em; line-height: 1.35; text-align: left !important;">
<h1 style="text-align: left !important; margin: 0 0 0.2em 0;">DeepWell</h1>
<h2 style="text-align: left !important; margin: 0 0 1em 0; color: #247BA0;">Using spatial data to improve borehole siting in Kenya’s drylands</h2>

<p style="text-align: left !important; margin: 2em 0 0.2em 0; font-weight: 600;">Sascha Alexeyenko</p>
<p style="text-align: left !important; margin: 0; color: #647783;">DSR Final Project · 20-Oct-26</p>
</div>

<!-- Right Column: Image Block -->
<div style="display: flex; justify-content: center; align-items: center;">
<!-- <img src="/app/static/photo_1.png" style="width: 100%; max-height: 550px; object-fit: contain; margin: 0;"> -->
</div>

</div>

</section>

---

## Why groundwater and why boreholes?

<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center">

<div>
<img src="https://raw.githubusercontent.com/lxynk/DeepWell/main/static/photo_1.png" style="width:100%;max-height:390px;object-fit:contain">
</div>

<div style="font-size:0.78em;line-height:1.35">

**Water must be available, reliable, safe**

In arid and semi-arid regions, groundwater is critical when surface sources are seasonal or scarce.

A borehole can easily fail: it may be dry, yield too little water, or produce water of unsuitable quality.

**The task**

Use existing borehole records and spatial data to reduce uncertainty before drilling.

</div>
</div>

---

## Water access remains a global challenge

### Progress has been made, but billions of people are still left behind.

![Global water-access statistics](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/global_water_stats.svg)

---

## The burden is unevenly distributed

### Global averages hide large regional gaps

![Regional drinking-water coverage](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/regional_coverage.svg)

---

## DeepWell: a study in northern Kenya

### From the global challenge to a local test case: the counties Marsabit and Turkana

![Locator maps showing Kenya within Africa and the approximate Marsabit and Turkana study areas](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/locator_maps.svg)

---

## A costly decision under uncertainty

### Can spatial evidence improve the odds?

Amref Health Africa reports that current geological assessments in Kenya’s arid and semi-arid lands lead to successful drilling in around **60% of cases**.

That leaves substantial room to improve site selection and reduce the cost of unsuccessful drilling.

---

## Related work: a shared ambition

### Analytics for a Better World, Amref Health Africa, ProRail

A parallel initiative is developing a decision-support tool combining satellite, geological, and other spatial data to identify more promising borehole locations in Kenya’s drylands.

Its stated ambition is to increase drilling success from around **60% to above 90%**. The public project description outlines the goal and planned work, but does not report numerical model-validation results or demonstrated field improvements.

---

## What are we trying to predict?

### A useful system will need more than one model

A first step is to predict the likelihood that a proposed drilling location will result in a **successful borehole**.

A full-scale decision-support system should ultimately address three distinct outcomes:

- **Success:** is a borehole likely to hit water?
- **Quantity / yield:** how much water can it reliably supply?
- **Quality / salinity:** is the water suitable for its intended use?

The current success model is only one component of that larger goal.

---

## The data

![Data cleaning funnel](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/data_funnel.svg)

The original records required substantial cleaning and auditing: checking coordinates, clarifying outcome labels, identifying ambiguous or conflicting records, handling missing information, addressing the intrinsic disbalance in the data.

---

## The features

![DeepWell feature groups](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/feature_groups.svg)

The goal is not simply to add more variables. It is to test whether each feature group provides useful information beyond what the model already knows, in an attempt to describe the landscape around each location.

---

## The evaluation

Nearby boreholes can share environmental conditions. A random train/test split may therefore make a model appear more capable of generalising than it really is.

The workflow uses spatially aware cross-validation across geographically distinct groups.

- **Balanced accuracy:** performance across both classes.
- **Failure recall:** the share of labelled failures correctly identified.
- **Success recall:** the share of labelled successes correctly identified.
- **Fold-to-fold variation:** consistency across spatial partitions.

---

## The tuning

Optuna studies have been run for **Random Forest, XGBoost, and LightGBM** to find the best hyperparameter configurations.

![Optuna dashboard](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/optuna_xgb.png)

---

## The results

![Best current model results](https://raw.githubusercontent.com/lxynk/DeepWell/main/static/model_results.svg)

**Feature set E+T+A15+R+LUP:** elevation, terrain, hydrological accumulation, distance to rivers, and a hydrological landform measure.

**Best Random Forest parameters:** `max_depth=16`, `min_samples_leaf=4`, `min_samples_split=2`, `max_features=0.5`.

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

## Thank you!

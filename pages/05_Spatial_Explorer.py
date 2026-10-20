from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import folium
import geopandas as gpd
import joblib
import numpy as np
import pandas as pd
import rasterio
import streamlit as st
from rasterio.warp import transform as transform_coords
from shapely.geometry import Point, box
from streamlit_folium import st_folium

st.set_page_config(page_title="Spatial Explorer", page_icon="🗺️", layout="wide")

# Assumes this page is saved at <project-root>/pages/02_Spatial_Explorer.py.
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
MODEL_DIR = ROOT / "models"
DEFAULT_MODEL = MODEL_DIR / "rf_combined_E_T_A15_R_LUP.joblib"
DEFAULT_METADATA = MODEL_DIR / "rf_combined_E_T_A15_R_LUP.json"
RIVER_PATH_CANDIDATES = [
    DATA_DIR / "raw/HydroRIVERS_v10_af_shp/HydroRIVERS_v10_af.shp",
    DATA_DIR / "raw/kenya_add_features/hydrology/HydroRIVERS_v10_af_shp/HydroRIVERS_v10_af_shp/HydroRIVERS_v10_af.shp",
]
# Same study-area window used to extract rivers_study. The source lines are retained whole.
RIVER_BBOX = (34.0183, 0.97746, 39.64795, 5.52061)
METRIC_CRS = "EPSG:32636"

# Explicit source mapping for the known project rasters. Relative paths are rooted at the
# repository root. Hydrology rasters store raw values; the training-time log transforms are
# reproduced below. Terrain derivative band order: 1=slope, 2=mrrtf, 3=mrvbf.
HYDROLOGY_DIR = DATA_DIR / "raw/kenya_add_features/hydrology/cropped"
TERRAIN_DIR = DATA_DIR / "raw/kenya_add_features/terrain"

TERRAIN_RASTERS = {
    "elevation_srtm": [
        (TERRAIN_DIR / "marsabit_srtm_elevation.tif", 1),
        (TERRAIN_DIR / "turkana_ndma_srtm_elevation.tif", 1),
    ],
    "slope_pct": [
        (TERRAIN_DIR / "marsabit_srtm_deriv.tif", 1),
        (TERRAIN_DIR / "turkana_ndma_srtm_deriv.tif", 1),
    ],
    "mrrtf": [
        (TERRAIN_DIR / "marsabit_srtm_deriv.tif", 2),
        (TERRAIN_DIR / "turkana_ndma_srtm_deriv.tif", 2),
    ],
    "mrvbf": [
        (TERRAIN_DIR / "marsabit_srtm_deriv.tif", 3),
        (TERRAIN_DIR / "turkana_ndma_srtm_deriv.tif", 3),
    ],
}

HYDROLOGY_RASTERS = {
    "log10_acc_15s": HYDROLOGY_DIR / "hyd_af_acc_15s_kenya_study_crop.tif",
    "log10_lup_15s": HYDROLOGY_DIR / "hyd_af_lup_15s_kenya_study_crop.tif",
}

# log1p_distance_hydrorivers is calculated from HydroRIVERS line geometry in a metric CRS,
# not sampled from hyd_af_ldn_15s. The order-3-plus variant is intentionally not used.

DATASET_OPTIONS = {
    "Rural Focus — Marsabit": ["rf_spatial.gpkg", "marsabit_common.gpkg", "rf_prepared.gpkg", "rf_cleaned.gpkg", "rf.gpkg"],
    "Rural Focus — Turkana": ["rf_turkana_spatial.gpkg", "rf_turkana_prepared.gpkg"],
}

LABEL_CANDIDATES = ["target_success", "target", "success", "status", "functionality", "functional_status"]
LAT_CANDIDATES = ["latitude", "lat", "y"]
LON_CANDIDATES = ["longitude", "lon", "long", "x"]


def first_existing(paths: list[Path]) -> Path | None:
    return next((p for p in paths if p.exists()), None)


def find_dataset_path(dataset_label: str) -> Path | None:
    candidates = [PROCESSED_DIR / name for name in DATASET_OPTIONS[dataset_label]]
    return first_existing(candidates)


def load_metadata(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)
    if not isinstance(metadata, dict):
        raise ValueError("Model metadata JSON must contain an object.")
    return metadata


def get_model_features(metadata: dict[str, Any], model: Any) -> list[str]:
    features = metadata.get("features") or metadata.get("feature_names") or metadata.get("required_features")
    if not features:
        features = getattr(model, "feature_names_in_", None)
    if features is None:
        raise ValueError("No feature list found in model metadata or the fitted model.")
    features = [str(x) for x in features]
    if not features:
        raise ValueError("The model feature list is empty.")
    return features


def get_label_column(gdf: gpd.GeoDataFrame, metadata: dict[str, Any]) -> str | None:
    configured = metadata.get("target_column") or metadata.get("label_column")
    if configured and configured in gdf.columns:
        return str(configured)
    return next((c for c in LABEL_CANDIDATES if c in gdf.columns), None)


def label_kind(value: Any) -> str:
    if pd.isna(value):
        return "Unknown"
    if isinstance(value, (int, np.integer, float, np.floating)):
        if int(value) == 0:
            return "Failure"
        if int(value) == 1:
            return "Success"
    text = str(value).strip().lower()
    if text in {"0", "failure", "failed", "non-functional", "nonfunctional", "dry", "broken"}:
        return "Failure"
    if text in {"1", "success", "successful", "functional", "working", "operational"}:
        return "Success"
    return "Unknown"


def map_frame(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.crs is None:
        raise ValueError("The borehole GeoPackage has no CRS. Set its CRS before using the map.")
    result = gdf.copy()
    if result.geometry.name not in result.columns:
        raise ValueError("No geometry column was found in the borehole dataset.")
    result = result[result.geometry.notna() & ~result.geometry.is_empty].copy()
    result = result.to_crs("EPSG:4326")
    return result


def sample_raster(path: Path, longitude: float, latitude: float, band: int = 1) -> float:
    """Sample one raster band at a WGS84 point, rejecting out-of-coverage and NoData cells."""
    if not path.exists():
        raise FileNotFoundError(f"Raster not found: {path}")
    with rasterio.open(path) as src:
        if src.count < band:
            raise ValueError(f"{path.name} has {src.count} band(s); requested band {band}")
        if src.crs is None:
            raise ValueError(f"Raster has no CRS: {path.name}")
        xs, ys = transform_coords("EPSG:4326", src.crs, [longitude], [latitude])
        x, y = float(xs[0]), float(ys[0])
        left, bottom, right, top = src.bounds
        if not (left <= x <= right and bottom <= y <= top):
            raise ValueError(f"Selected point is outside raster coverage: {path.name}")
        sample = next(src.sample([(x, y)], indexes=band, masked=True))
        value = sample[0]
        if np.ma.is_masked(value):
            raise ValueError(f"Selected point falls on NoData in {path.name} (band {band})")
        value = float(value)
        if src.nodata is not None and np.isclose(value, src.nodata, equal_nan=True):
            raise ValueError(f"Selected point falls on NoData in {path.name} (band {band})")
        if not np.isfinite(value):
            raise ValueError(f"Selected point has a non-finite value in {path.name} (band {band})")
        return value


def sample_first_covering(candidates: list[tuple[Path, int]], longitude: float, latitude: float) -> float:
    errors = []
    for path, band in candidates:
        try:
            return sample_raster(path, longitude, latitude, band=band)
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
    if not candidates:
        raise ValueError("No raster candidates are configured")
    raise ValueError("No valid terrain raster covers this point. " + " | ".join(errors))


@st.cache_data(show_spinner="Loading river network…")
def load_rivers_metric(path_str: str, mtime: float) -> gpd.GeoDataFrame:
    """Load study-area river lines and project them to the training-time metric CRS."""
    path = Path(path_str)
    # The bbox read keeps a large continental HydroRIVERS file manageable while preserving
    # complete river segments, as in the project's rivers_study preparation.
    rivers = gpd.read_file(path, bbox=RIVER_BBOX)
    if rivers.empty:
        raise ValueError("No river features intersect the configured study-area bounds.")
    if rivers.crs is None:
        raise ValueError("The river dataset has no CRS; expected a known source CRS such as EPSG:4326.")
    rivers = rivers[rivers.geometry.notna() & ~rivers.geometry.is_empty].copy()
    rivers = rivers.to_crs(METRIC_CRS)
    if rivers.empty:
        raise ValueError("No valid river geometries remain after loading.")
    return rivers


def river_distance_feature(longitude: float, latitude: float, river_path: Path) -> float:
    """Return log1p distance in metres to the nearest river of any order."""
    if not river_path.exists():
        raise FileNotFoundError(f"River dataset not found: {river_path}")
    rivers = load_rivers_metric(str(river_path.resolve()), river_path.stat().st_mtime)
    point = gpd.GeoSeries([Point(longitude, latitude)], crs="EPSG:4326").to_crs(METRIC_CRS).iloc[0]
    # No ORD_STRA filter: this reproduces distance_to_hydrorivers_m, not order-3-plus distance.
    distances = rivers.geometry.distance(point)
    if distances.empty or not np.isfinite(distances.min()):
        raise ValueError("Could not calculate distance to the river network.")
    return float(np.log1p(float(distances.min())))


def raster_value_for_feature(
    feature: str, longitude: float, latitude: float, river_path: Path | None = None
) -> tuple[float | None, str | None]:
    """Resolve a model feature from rasters or the HydroRIVERS geometry source."""
    normalized = feature.strip().lower()
    if normalized in {"longitude", "lon", "long"}:
        return longitude, None
    if normalized in {"latitude", "lat"}:
        return latitude, None

    try:
        if feature in TERRAIN_RASTERS:
            value = sample_first_covering(TERRAIN_RASTERS[feature], longitude, latitude)
            # The model feature is named slope_pct; do not silently convert degrees to percent.
            # This returns the source band's stored value, which must match training-time units.
            return value, None

        if feature in HYDROLOGY_RASTERS:
            raw = sample_raster(HYDROLOGY_RASTERS[feature], longitude, latitude, band=1)
            # Match the training preprocessing: log10(clip(raw, lower=0) + 1).
            return float(np.log10(max(raw, 0.0) + 1.0)), None

        if feature == "log1p_distance_hydrorivers":
            if river_path is None:
                return None, "Configure the HydroRIVERS source file to calculate distance to the nearest river."
            return river_distance_feature(longitude, latitude, river_path), None

        return None, f"No explicit raster mapping is configured for feature '{feature}'."
    except Exception as exc:
        return None, f"{feature}: {exc}"


@st.cache_resource(show_spinner=False)
def load_model(model_path_str: str) -> Any:
    return joblib.load(model_path_str)


@st.cache_data(show_spinner=False)
def load_boreholes(path_str: str) -> gpd.GeoDataFrame:
    return gpd.read_file(path_str)


st.title("Spatial Explorer")
st.caption("Explore labelled Rural Focus boreholes and test a saved baseline model at a clicked location.")

with st.sidebar:
    st.header("Configuration")
    model_path_input = st.text_input("Model artifact", value=str(DEFAULT_MODEL))
    metadata_path_input = st.text_input("Model metadata JSON", value=str(DEFAULT_METADATA))
    dataset_label = st.selectbox("Borehole dataset", list(DATASET_OPTIONS.keys()))
    default_river_path = first_existing(RIVER_PATH_CANDIDATES)
    river_path_input = st.text_input(
        "HydroRIVERS source file",
        value=str(default_river_path or RIVER_PATH_CANDIDATES[2]),
        help="Use the HydroRIVERS shapefile or a saved rivers_study GeoPackage/shapefile.",
    )
    st.caption("This page intentionally excludes NDMA records from the Rural Focus model workflow.")

model_path = Path(model_path_input).expanduser()
metadata_path = Path(metadata_path_input).expanduser()
river_path = Path(river_path_input).expanduser()

model = None
metadata: dict[str, Any] = {}
features: list[str] = []
model_error = None
if model_path.exists() and metadata_path.exists():
    try:
        metadata = load_metadata(metadata_path)
        model = load_model(str(model_path))
        features = get_model_features(metadata, model)
    except Exception as exc:
        model_error = str(exc)
else:
    missing = [str(p) for p in (model_path, metadata_path) if not p.exists()]
    model_error = "Required model file(s) not found: " + ", ".join(missing)

if model_error:
    st.warning("Prediction is not available until the model artifact and matching metadata are configured.")
    with st.expander("Model configuration details"):
        st.code(model_error)

source_path = find_dataset_path(dataset_label)
if source_path is None:
    st.error(
        f"No known GeoPackage found for **{dataset_label}**. Update DATASET_OPTIONS near the top of this page "
        "to match the filenames in data/processed/."
    )
    st.stop()

try:
    raw_gdf = load_boreholes(str(source_path))
    gdf = map_frame(raw_gdf)
except Exception as exc:
    st.error(f"Could not load the borehole layer: {exc}")
    st.stop()

label_column = get_label_column(gdf, metadata)
if label_column:
    gdf["_map_label"] = gdf[label_column].map(label_kind)
else:
    gdf["_map_label"] = "Unknown"

st.caption(f"Loaded **{len(gdf):,}** mapped records from `{source_path.relative_to(ROOT) if source_path.is_relative_to(ROOT) else source_path}`.")

col_filters, col_map = st.columns([1, 3], gap="large")
with col_filters:
    st.subheader("Map filters")
    label_filter = st.multiselect("Label", ["Failure", "Success", "Unknown"], default=["Failure", "Success", "Unknown"])
    filtered = gdf[gdf["_map_label"].isin(label_filter)].copy()
    st.metric("Visible records", f"{len(filtered):,}")
    st.metric("Failures", f"{int((filtered['_map_label'] == 'Failure').sum()):,}")
    st.metric("Successes", f"{int((filtered['_map_label'] == 'Success').sum()):,}")
    st.divider()
    st.markdown("**Choose a point**")
    st.write("Click an empty location on the map to set a prediction point. Click an existing marker only to inspect that borehole; it does not imply a prediction for that record.")

if len(filtered):
    centroid = filtered.geometry.union_all().centroid
    center = [float(centroid.y), float(centroid.x)]
else:
    center = [3.0, 37.0]

map_obj = folium.Map(location=center, zoom_start=7, control_scale=True, tiles="OpenStreetMap")
colors = {"Failure": "red", "Success": "green", "Unknown": "gray"}
# Limit the number of rendered point markers to keep the browser responsive.
MAX_MARKERS = 2500
points_to_draw = filtered.head(MAX_MARKERS)
for idx, row in points_to_draw.iterrows():
    geom = row.geometry
    if geom.geom_type != "Point":
        continue
    props = {"record": str(idx), "label": row["_map_label"]}
    for col in list(gdf.columns)[:20]:
        if col == gdf.geometry.name or col.startswith("_"):
            continue
        value = row.get(col)
        if value is not None and not isinstance(value, (dict, list, tuple)):
            props[col] = str(value)[:160]
    folium.CircleMarker(
        location=[geom.y, geom.x],
        radius=4,
        color=colors.get(row["_map_label"], "gray"),
        fill=True,
        fill_opacity=0.75,
        weight=1,
        tooltip=f"{row['_map_label']} · record {idx}",
        popup=folium.Popup("<br>".join(f"<b>{k}</b>: {v}" for k, v in props.items()), max_width=360),
    ).add_to(map_obj)

selected = st.session_state.get("prediction_point")
if selected:
    folium.Marker(
        location=[selected["latitude"], selected["longitude"]],
        tooltip="Selected prediction point",
        icon=folium.Icon(color="blue", icon="crosshairs", prefix="fa"),
    ).add_to(map_obj)

with col_map:
    map_result = st_folium(
        map_obj,
        height=610,
        use_container_width=True,
        returned_objects=["last_clicked", "last_object_clicked"],
        key=f"spatial-map-{dataset_label}",
    )

clicked = map_result.get("last_clicked") if map_result else None
if clicked and clicked.get("lat") is not None and clicked.get("lng") is not None:
    new_point = {"latitude": float(clicked["lat"]), "longitude": float(clicked["lng"])}
    old_point = st.session_state.get("prediction_point")
    is_new_point = old_point is None or abs(old_point["latitude"] - new_point["latitude"]) > 1e-7 or abs(old_point["longitude"] - new_point["longitude"]) > 1e-7
    if is_new_point:
        st.session_state["prediction_point"] = new_point
        st.rerun()

st.divider()
st.subheader("Selected location prediction")
point = st.session_state.get("prediction_point")
if not point:
    st.info("Click an empty spot on the map to select a location. Prediction requires the saved model, matching metadata, and every required feature raster.")
else:
    point_col, predict_col = st.columns([2, 1], gap="large")
    with point_col:
        st.write(f"**Latitude:** {point['latitude']:.6f}  ")
        st.write(f"**Longitude:** {point['longitude']:.6f}")
        if st.button("Clear selected point"):
            st.session_state.pop("prediction_point", None)
            st.session_state.pop("prediction_values", None)
            st.rerun()

    feature_values: dict[str, float] = {}
    feature_errors: list[str] = []
    if model is not None:
        for feature in features:
            value, error = raster_value_for_feature(
                feature, point["longitude"], point["latitude"], river_path=river_path
            )
            if error:
                feature_errors.append(error)
            elif value is not None:
                feature_values[feature] = value

    with st.expander("Feature values at selected location", expanded=True):
        if features:
            feature_rows = []
            for feature in features:
                if feature in feature_values:
                    feature_rows.append({"Feature": feature, "Value": feature_values[feature], "Status": "Available"})
                else:
                    error = next((e for e in feature_errors if feature in e), "Feature value unavailable")
                    feature_rows.append({"Feature": feature, "Value": None, "Status": error})
            st.dataframe(pd.DataFrame(feature_rows), use_container_width=True, hide_index=True)
        else:
            st.write("Load a valid model and metadata file to inspect required feature values.")

    with predict_col:
        can_predict = model is not None and bool(features) and not feature_errors and len(feature_values) == len(features)
        if not can_predict:
            st.button("Predict", disabled=True, use_container_width=True)
            if model is not None and feature_errors:
                st.warning("Prediction blocked: one or more required feature values are unavailable.")
        elif st.button("Predict", type="primary", use_container_width=True):
            try:
                input_df = pd.DataFrame([[feature_values[f] for f in features]], columns=features)
                predicted_class = int(model.predict(input_df)[0])
                class_names = metadata.get("class_names", {"0": "Failure", "1": "Success"})
                predicted_label = class_names.get(str(predicted_class), {0: "Failure", 1: "Success"}.get(predicted_class, str(predicted_class)))
                probabilities = {}
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_df)[0]
                    for class_value, probability in zip(model.classes_, proba):
                        name = class_names.get(str(int(class_value)), {0: "Failure", 1: "Success"}.get(int(class_value), str(class_value)))
                        probabilities[name] = float(probability)
                st.session_state["prediction_values"] = {
                    "label": predicted_label,
                    "class": predicted_class,
                    "probabilities": probabilities,
                }
            except Exception as exc:
                st.error(f"Prediction failed: {exc}")

    prediction = st.session_state.get("prediction_values")
    if prediction:
        st.markdown("#### Model output")
        st.write(f"**Predicted class:** {prediction['label']}")
        if prediction["probabilities"]:
            probability_cols = st.columns(len(prediction["probabilities"]))
            for col, (name, probability) in zip(probability_cols, prediction["probabilities"].items()):
                col.metric(f"P({name})", f"{probability:.1%}")
        st.caption(
            "Exploratory model output only — not a drilling recommendation. It is only meaningful if the saved "
            "model was validated for the intended geography and the feature rasters use the exact training-time "
            "definitions, units, resolution, and transformations. Probabilities may not be calibrated."
        )


from pathlib import Path

import streamlit as st


st.title("Model Lab")

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"

models = [
    {
        "name": "Random Forest",
        "image": "optuna_rf.png",
        "best_model": "",
        "parameters": [
            "Parameter 1: placeholder",
            "Parameter 2: placeholder",
            "Parameter 3: placeholder",
        ],
    },
    {
        "name": "XGBoost",
        "image": "optuna_xgb.png",
        "best_model": "",
        "parameters": [
            "Parameter 1: placeholder",
            "Parameter 2: placeholder",
            "Parameter 3: placeholder",
        ],
    },
    {
        "name": "LightGBM",
        "image": "optuna_lgbm.png",
        "best_model": "",
        "parameters": [
            "Parameter 1: placeholder",
            "Parameter 2: placeholder",
            "Parameter 3: placeholder",
        ],
    },
]

params_code = """params = {
    'learning_rate': 0.000,
    'max_depth': 0,
    'min_child_weight': 0.000
}"""

for model in models:
    st.subheader(f"Optuna study: {model['name']}")

    image_col, details_col = st.columns([1.6, 1])

    with image_col:
        image_path = STATIC_DIR / model["image"]

        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.warning(f"Image not found: {model['image']}")

    with details_col:
        st.markdown(f"### Best model: {model['best_model']}")
        st.metric("Best score", "0.00000")

        st.markdown("**Model parameters**")
        for parameter in model["parameters"]:
            st.markdown(f"- {parameter}")

        st.code(params_code, language="python")

    st.divider()

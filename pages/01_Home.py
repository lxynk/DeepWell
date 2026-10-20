from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]

dashboard_tab, presentation_tab = st.tabs(
    ["Dashboard", "Presentation"]
)

st.title("DeepWell")
st.subheader("Smarter groundwater exploration")

st.markdown(
    """
    DeepWell explores how machine learning and spatial data can
    improve the selection of borehole drilling sites.

    ### The challenge

    Drilling a borehole is costly, and finding sufficient water of
    adequate quality is not guaranteed. Better information before
    drilling could help reduce unsuccessful investments.

    ### Our approach

    DeepWell combines geological, terrain, and hydrological
    information with historical borehole records to predict the
    likelihood of drilling success.

    ### Explore the project

    - **Spatial Explorer** — explore borehole locations and model
        predictions across the study area.
    - **Model Lab** — inspect model optimisation studies and
        compare candidate models.

    The goal is to support more informed, data-driven decisions
    about where to drill.
    """
)

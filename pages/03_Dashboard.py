from pathlib import Path

import fiona
import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR.parent / "data"

PROJECT_SUMMARY = pd.DataFrame(
    [
        {
            "Dataset": "RF Marsabit",
            "Original records": 352,
            "Usable labelled": 247,
            "Failures": 79,
            "Successes": 168,
        },
        {
            "Dataset": "RF Turkana",
            "Original records": 1062,
            "Usable labelled": 65,
            "Failures": 45,
            "Successes": 20,
        },
        {
            "Dataset": "NDMA Turkana",
            "Original records": 2287,
            "Usable labelled": 147,
            "Failures": 50,
            "Successes": 97,
        },
    ]
)

@st.cache_data
def inspect_geopackages(data_dir: str) -> pd.DataFrame:
    """Inspect GeoPackage layers without loading their geometries."""
    root = Path(data_dir)
    rows = []

    if not root.exists():
        return pd.DataFrame()

    for path in sorted(root.glob("*.gpkg")):
        try:
            layers = fiona.listlayers(str(path))

            if not layers:
                rows.append(
                    {
                        "File": path.name,
                        "Layer": "—",
                        "Records": None,
                        "Geometry": "—",
                        "CRS": "—",
                        "Status": "No layers found",
                    }
                )
                continue

            for layer in layers:
                try:
                    with fiona.open(str(path), layer=layer) as src:
                        rows.append(
                            {
                                "File": path.name,
                                "Layer": layer,
                                "Records": len(src),
                                "Geometry": src.schema.get(
                                    "geometry", "Unknown"
                                ),
                                "CRS": str(src.crs) or "Unknown",
                                "Status": "OK",
                            }
                        )
                except Exception as exc:
                    rows.append(
                        {
                            "File": path.name,
                            "Layer": layer,
                            "Records": None,
                            "Geometry": "—",
                            "CRS": "—",
                            "Status": f"Layer error: {exc}",
                        }
                    )

        except Exception as exc:
            rows.append(
                {
                    "File": path.name,
                    "Layer": "—",
                    "Records": None,
                    "Geometry": "—",
                    "CRS": "—",
                    "Status": f"Read error: {exc}",
                }
            )

    return pd.DataFrame(rows)

st.title("Dashboard")
st.markdown(
    "A research dashboard for exploring borehole data, "
    "data quality, and model development in Marsabit and Turkana."
)

st.info(
    "The project summary below describes the current modeling "
    "cohort. The saved GeoPackages may contain additional records "
    "that have not been included in that cohort."
)

total_original = int(PROJECT_SUMMARY["Original records"].sum())
total_labelled = int(PROJECT_SUMMARY["Usable labelled"].sum())
total_failures = int(PROJECT_SUMMARY["Failures"].sum())
total_successes = int(PROJECT_SUMMARY["Successes"].sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Original records", f"{total_original:,}")
col2.metric("Usable labelled", f"{total_labelled:,}")
col3.metric("Failures", f"{total_failures:,}")
col4.metric("Successes", f"{total_successes:,}")

st.subheader("Current modelling cohort")

display_df = PROJECT_SUMMARY.copy()
total_row = pd.DataFrame(
    [
        {
            "Dataset": "Total",
            "Original records": total_original,
            "Usable labelled": total_labelled,
            "Failures": total_failures,
            "Successes": total_successes,
        }
    ]
)
display_df = pd.concat(
    [display_df, total_row],
    ignore_index=True,
)

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
)

st.subheader("Class balance")

chart_df = PROJECT_SUMMARY.set_index("Dataset")[
    ["Failures", "Successes"]
]
st.bar_chart(chart_df)

col1, col2 = st.columns(2)
col1.metric(
    "Labelled share of original records",
    f"{total_labelled / total_original:.1%}",
)
col2.metric(
    "Failures among labelled records",
    f"{total_failures / total_labelled:.1%}",
)

st.caption(
    "The failure rate describes the labelled cohort, not necessarily "
    "the real-world prevalence of borehole failure. Dataset labels "
    "and collection procedures may differ."
)

st.subheader("Research datasets")

st.markdown(
    """
    - **Rural Focus — Marsabit:** 352 original records.
    - **Rural Focus — Turkana:** 1,062 original records.
    - **NDMA — Turkana:** 2,287 original records.

    The datasets remain separate while we evaluate their labels,
    coverage, and suitability for modelling.
    """
)

st.subheader("Saved data snapshot")

# st.title("Saved data inventory")

# inventory = inspect_geopackages(str(DATA_DIR))

# if inventory.empty:
#     st.warning(f"No GeoPackages found in `{DATA_DIR}`.")
# else:
#     st.write(
#         f"Found {inventory['File'].nunique()} GeoPackage files "
#         f"and {len(inventory)} layer entries."
#     )
#     errors = inventory[
#         inventory["Status"] != "OK"
#     ]

#     if not errors.empty:
#         st.warning(
#             f"{len(errors)} layer or file entries need attention. "
#             "See Saved data inventory for details."
#         )

#     st.dataframe(
#         inventory[
#             ["File", "Layer", "Records", "CRS", "Status"]
#         ],
#         hide_index=True,
#         use_container_width=True,
#     )

st.markdown(
    "Inspect the saved GeoPackage layers without changing the "
    "underlying files."
)

if st.button("Refresh inventory"):
    inspect_geopackages.clear()

inventory = inspect_geopackages(str(DATA_DIR))

if inventory.empty:
    st.warning(f"No GeoPackages found in `{DATA_DIR}`.")
else:
    files = ["All files"] + sorted(inventory["File"].unique())
    selected_file = st.selectbox("File", files)

    filtered = inventory.copy()
    if selected_file != "All files":
        filtered = filtered[
            filtered["File"] == selected_file
        ]

    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
    )

    errors = filtered[filtered["Status"] != "OK"]
    if not errors.empty:
        st.subheader("Files requiring attention")
        st.dataframe(
            errors,
            hide_index=True,
            use_container_width=True,
        )

st.caption(
    "Record counts and metadata describe the files currently saved "
    "under data/processed. They do not necessarily equal the "
    "current modelling cohort."
)

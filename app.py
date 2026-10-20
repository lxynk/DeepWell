import streamlit as st

st.set_page_config(
    page_title="DeepWell",
    page_icon="💧",
    layout="wide",
)

pages = [
    st.Page(
        "pages/01_Home.py",
        title="Home",
        icon="🏠",
        default=True,
    ),
    st.Page(
        "pages/02_Presentation.py",
        title="Presentation",
        icon="🖥️",
    ),
    st.Page(
        "pages/03_Dashboard.py",
        title="Dashboard",
        icon="📊",
    ),
    st.Page(
        "pages/04_Model_Lab.py",
        title="Model Lab",
        icon="🧪",
    ),
    st.Page(
        "pages/05_Spatial_Explorer.py",
        title="Spatial Explorer",
        icon="🗺️",
    ),
]

navigation = st.navigation(pages)
navigation.run()

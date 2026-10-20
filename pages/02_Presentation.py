from pathlib import Path

import reveal_slides as rs
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SLIDES_PATH = PROJECT_ROOT / "static" / "slides.md"
CSS_PATH = PROJECT_ROOT / "static" / "slides.css"

if CSS_PATH.exists():
    css = CSS_PATH.read_text(encoding="utf-8")
    # st.html(f"<style>{css}</style>")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    st.error(f"Could not find CSS file at: {CSS_PATH}")

st.markdown("""
<style>
.reveal .slides section {
    box-sizing: border-box;
    padding: 20px 35px;
    overflow: hidden;
}

.reveal h1 {
    font-size: 2.0em;
}

.reveal h2 {
    font-size: 1.5em;
}

.reveal h3 {
    font-size: 1.2em;
}

.reveal p,
.reveal li {
    font-size: 0.75em;
    line-height: 1.35;
}

.reveal img {
    max-height: 40vh;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

slides = SLIDES_PATH.read_text(encoding="utf-8")

rs.slides(
    slides,
    height=720,
    theme="white",
    display_only=True,
    config={
        "transition": "slide",
        "width": 900,
        "height": 660,
        # "margin": 0.04,
        "slideNumber": True,
        "controls": True,
        "progress": True,
        "center": False,
        "hash": True,
    },
)

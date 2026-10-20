from pathlib import Path

import reveal_slides as rs
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SLIDES_PATH = PROJECT_ROOT / "slides.md"

css = (PROJECT_ROOT / "static" / "slides.css").read_text(encoding="utf-8")

st.html(f"<style>{css}</style>")

slides = SLIDES_PATH.read_text(encoding="utf-8")

rs.slides(
    slides,
    height=720,
    theme="white",
    display_only=True,
    config={
        "transition": "slide",
        "width": 1280,
        "height": 720,
    },
)

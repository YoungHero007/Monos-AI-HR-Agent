from pathlib import Path
import base64

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Monos HR | Employee Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
css = (ROOT / "styles.css").read_text(encoding="utf-8")
javascript = (ROOT / "app.js").read_text(encoding="utf-8")
jobs = (ROOT / "jobs.js").read_text(encoding="utf-8")
template = base64.b64encode((ROOT / "Тодорхойлолт загвар.pdf").read_bytes()).decode("ascii")
html = html.replace(
    '<link rel="stylesheet" href="styles.css" />',
    f"<style>{css}</style>",
).replace(
    '<script src="app.js"></script>',
    f"<script>{javascript}</script>",
).replace(
    '<script src="jobs.js"></script>',
    f"<script>{jobs}</script>",
).replace(
    "./Monos_Calingiin_Todorhoilolt_Template.docx",
    f"data:application/pdf;base64,{template}",
)
components.html(html, height=1100, scrolling=True)

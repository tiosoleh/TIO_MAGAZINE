import streamlit as st

from components.music_player import music_popover
from components.sections import esc, render


def render_navbar(t: dict) -> None:
    ui = t["ui"]
    with st.container(key="navbar"):
        c1, c2, c3, c4 = st.columns([2.2, 4.6, 1.4, 2.0], vertical_alignment="center")
        with c1:
            render(f'<div class="tm-logo">{esc(ui["brand"])}</div>')
        with c2:
            render(f"""<nav class="tm-menu">
            <a href="#page-3">{esc(ui['nav_stories'])}</a>
            <a href="#page-7">{esc(ui['nav_photography'])}</a>
            <a href="#page-2">{esc(ui['nav_about'])}</a>
            <a href="#download">{esc(ui['nav_pdf'])}</a></nav>""")
        with c3:
            music_popover(t)
        with c4:
            st.toggle(ui["lang_toggle"], key="use_id")

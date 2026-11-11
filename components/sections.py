"""Shared HTML helpers for the editorial layout."""
import html as _html
from pathlib import Path

import streamlit as st

from utils import image_handler as ih

ROOT = Path(__file__).resolve().parent.parent


def esc(text: str) -> str:
    return _html.escape(text, quote=True)


def clean(markup: str) -> str:
    """Strip indentation + blank lines so Streamlit's markdown never sees a code block."""
    return "\n".join(line.strip() for line in markup.splitlines() if line.strip())


def render(markup: str) -> None:
    st.markdown(clean(markup), unsafe_allow_html=True)


def inject_css() -> None:
    css = (ROOT / "styles" / "main.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def photo(slot: str, t: dict, ratio: str = "4/5") -> str:
    """HTML for one photo slot: the uploaded photo, or an elegant placeholder."""
    uri = ih.data_uri(slot)
    if uri:
        inner = f'<img src="{uri}" alt="photo">'
    else:
        inner = f'<div class="ph-empty"><b>+</b>{esc(t["ui"]["photo_empty"])}</div>'
    return f'<div class="ph reveal" style="aspect-ratio:{ratio}">{inner}</div>'


def section_open(n: int, title: str, t: dict, grammar: str | None = None, alt: bool = False) -> str:
    ui = t["ui"]
    gram = f'<div class="mag-grammar">{esc(ui["grammar"])}: {esc(grammar)}</div>' if grammar else ""
    return f"""
    <section class="mag-sec{' alt' if alt else ''}" id="page-{n}"><div class="mag-in">
    <div class="mag-eyebrow reveal">{esc(ui['page'])} {n:02d}</div>
    <h2 class="mag-title reveal">{esc(title)}</h2>
    {gram}
    <div class="mag-rule"></div>
    """


def section_close() -> str:
    return "</div></section>"


def download_header(t: dict) -> str:
    ui = t["ui"]
    return f"""
    <section class="mag-dl" id="download"><div class="reveal">
    <div class="mag-eyebrow">{esc(ui['dl_eyebrow'])}</div>
    <h2>{esc(ui['dl_title'])}</h2>
    <p>{esc(ui['dl_text'])}</p>
    </div></section>
    """


def footer(t: dict) -> None:
    ui = t["ui"]
    render(f"""
    <footer class="mag-footer">
    <div class="brand">{esc(ui['brand'])}</div>
    <div class="tag">{esc(ui['footer_tag'])}</div>
    <small>Tio Kati Nuansya · 21 · Cianjur, West Java</small>
    <small>{esc(ui['footer_credit'])}</small>
    <small>{esc(ui['footer_built'])} · © 2026</small>
    </footer>
    """)

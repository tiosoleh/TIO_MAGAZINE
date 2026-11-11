import streamlit as st

from components import sections as s
from utils.content import CONTENT


def _word_counter(text: str, ui: dict) -> str:
    n = len(text.split())
    if n == 0:
        return ""
    if n < 100:
        return f"<div class='mag-wc bad'>{n} {ui['words']} — {s.esc(ui['wc_low'])}</div>"
    if n > 150:
        return f"<div class='mag-wc bad'>{n} {ui['words']} — {s.esc(ui['wc_high'])}</div>"
    return f"<div class='mag-wc ok'>{n} {ui['words']} — {s.esc(ui['wc_ok'])}</div>"


def render(t):
    d, en, ui = t["reading"], CONTENT["reading"], t["ui"]
    is_id = st.session_state.get("use_id", False)

    s.render(f"""
    <section class="mag-sec alt" id="page-8" style="padding-bottom:1.5rem"><div class="mag-in">
    <div class="mag-eyebrow reveal">{s.esc(ui['page'])} 08</div>
    <h2 class="mag-title reveal">{s.esc(d['title'])}</h2>
    <div class="mag-grammar">{s.esc(en['novel'])} · {s.esc(en['author'])}</div>
    <div class="mag-rule" style="margin-bottom:0"></div>
    <p class="mag-p" style="margin-top:1.6rem;font-weight:700">{s.esc(d['chapter'])}</p>
    </div></section>
    """)

    with st.container(key="reading"):
        left, right = st.columns(2, gap="large")
        with left:
            s.render(f"<div class='mag-part'>{s.esc(d['part1'])}</div>")
            s.render(f"<div class='mag-label'>{s.esc(d['keywords_label'])}</div>"
                     + "".join(f"<span class='mag-chip'>{s.esc(k)}</span>" for k in en["keywords"]))
            st.text_area(d["prediction_label"], key="r_prediction", height=190, help=ui["editable"])
            if is_id:
                s.render(f"<div class='mag-trans'>{s.esc(d['prediction'])}</div>")
        with right:
            s.render(f"<div class='mag-part'>{s.esc(d['part2'])}</div>")
            st.text_area(d["main_idea_label"], key="r_main_idea", height=110, help=ui["editable"])
            st.text_input(f"{d['events_label']} — 1", key="r_event1")
            st.text_input(f"{d['events_label']} — 2", key="r_event2")
            if is_id:
                s.render("<div class='mag-trans'>" + "<br>".join(s.esc(x) for x in d["events"]) + "</div>")
            st.text_area(d["eval_label"], key="r_evaluation", height=110, help=ui["editable"])
            if is_id:
                s.render(f"<div class='mag-trans'>{s.esc(d['main_idea'])}<br><br>{s.esc(d['evaluation'])}</div>")

        s.render(f"<div class='mag-label' style='margin-top:2rem'>{s.esc(d['excerpt_label'])}</div>")
        st.text_area(d["excerpt_label"], key="r_excerpt", height=230, help=d["excerpt_help"],
                     placeholder=d["excerpt_help"], label_visibility="collapsed")
        s.render(_word_counter(st.session_state.get("r_excerpt", ""), ui))

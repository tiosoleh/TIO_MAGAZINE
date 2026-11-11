"""TIO MAGAZINE — My Life, My Story (Streamlit).  Run:  streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="TIO Magazine — My Life, My Story", page_icon="📖",
                   layout="wide", initial_sidebar_state="collapsed")

from components import sections as s                       # noqa: E402
from components.navbar import render_navbar                # noqa: E402
from magazine_pages import (page_01_cover, page_02_about, page_03_routine,   # noqa: E402
                            page_04_hobbies, page_05_today, page_06_favorite_place,
                            page_07_photo_story, page_08_reading, page_09_reflection)
from utils import image_handler as ih                      # noqa: E402
from utils.pdf_generator import PDFLayoutError, build_pdf, default_reading   # noqa: E402
from utils.translations import get_text                    # noqa: E402

READING_KEYS = {"r_excerpt": "excerpt", "r_prediction": "prediction", "r_main_idea": "main_idea",
                "r_event1": "event1", "r_event2": "event2", "r_evaluation": "evaluation"}

# JS for scroll-reveal, progress bar and smooth anchor links (runs in the parent page).
FX_JS = """
<script>
(function(){
  var P = window.parent, D = P.document;
  function main(){ return D.querySelector('section.stMain') || D.querySelector('[data-testid="stMain"]'); }
  var bar = D.getElementById('tm-progress');
  if(!bar){ bar = D.createElement('div'); bar.id = 'tm-progress'; D.body.appendChild(bar); }
  var m = main();
  if(m && !m.__tmScroll){
    m.__tmScroll = true;
    m.addEventListener('scroll', function(){
      var max = m.scrollHeight - m.clientHeight;
      bar.style.width = (max > 0 ? (m.scrollTop / max) * 100 : 0) + '%';
    }, {passive:true});
  }
  var io = new P.IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.remove('rv-pending'); e.target.classList.add('rv-in'); io.unobserve(e.target); }
    });
  }, {root: m, threshold: 0.12});
  function scan(){
    D.querySelectorAll('.reveal:not([data-tm])').forEach(function(el){
      el.setAttribute('data-tm','1'); el.classList.add('rv-pending'); io.observe(el);
    });
  }
  scan();
  new P.MutationObserver(scan).observe(D.body, {childList:true, subtree:true});
  if(!D.__tmClicks){
    D.__tmClicks = true;
    D.addEventListener('click', function(ev){
      var a = ev.target.closest && ev.target.closest('a[href^="#"]');
      if(!a) return;
      var t = D.getElementById(a.getAttribute('href').slice(1));
      if(t){ ev.preventDefault(); t.scrollIntoView({behavior:'smooth', block:'start'}); }
    });
  }
})();
</script>
"""


@st.cache_data(show_spinner=False)
def _make_pdf(photo_items: tuple, reading_items: tuple) -> bytes:
    return build_pdf(dict(photo_items), dict(reading_items))


def main() -> None:
    ih.init_state()
    defaults = default_reading()
    for key, field in READING_KEYS.items():
        st.session_state.setdefault(key, defaults[field])

    lang = "id" if st.session_state.get("use_id") else "en"
    t = get_text(lang)

    s.inject_css()
    render_navbar(t)

    page_01_cover.render(t)
    page_02_about.render(t)
    page_03_routine.render(t)
    page_04_hobbies.render(t)
    page_05_today.render(t)
    page_06_favorite_place.render(t)
    page_07_photo_story.render(t)
    page_08_reading.render(t)
    page_09_reflection.render(t)

    # --- PDF download (always English, exactly 9 A4 pages) ---
    s.render(s.download_header(t))
    with st.container(key="dl"):
        try:
            reading = {field: st.session_state[key] for key, field in READING_KEYS.items()}
            pdf = _make_pdf(tuple(sorted(ih.all_photos().items())), tuple(sorted(reading.items())))
            st.download_button(t["ui"]["dl_button"], data=pdf, file_name="TIO_Magazine_My_Life_My_Story.pdf",
                               mime="application/pdf", key="dl_btn")
        except PDFLayoutError as exc:
            st.error(t["ui"]["dl_error"] + str(exc))
        except Exception as exc:                            # never crash the page
            st.error(t["ui"]["dl_error"] + str(exc))

    s.footer(t)
    with st.container(key="fx"):          # invisible helper frame (scroll effects)
        if hasattr(st, "iframe"):          # newer Streamlit
            st.iframe(FX_JS, height=1)
        else:                              # older Streamlit
            import streamlit.components.v1 as components
            components.html(FX_JS, height=0)


main()

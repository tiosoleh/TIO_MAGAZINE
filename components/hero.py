from components.sections import esc, render
from utils import image_handler as ih


def render_hero(t: dict) -> None:
    c, ui = t["cover"], t["ui"]
    uri = ih.data_uri("cover_1")
    style = f"background-image:url('{uri}')" if uri else ""
    cls = "tm-hero-img" if uri else "tm-hero-img nophoto"
    info = "<br>".join(esc(x) for x in c["info"])
    render(f"""
    <section class="tm-hero" id="page-1">
    <div class="{cls}" style="{style}">
    <div class="tm-hero-box reveal">
    <div class="tm-hero-kicker">{esc(ui['brand'])}</div>
    <h1>{esc(c['title'])}</h1>
    <div class="tm-hero-author">{esc(c['author'])}</div>
    <div class="tm-hero-tag">{esc(c['tagline'])}</div>
    <div class="tm-hero-info">{info}</div>
    </div>
    <div class="tm-hero-quote">“{esc(c['quote'])}”</div>
    <a class="tm-scroll" href="#page-2">{esc(ui['scroll'])} <span>↓</span></a>
    </div></section>
    """)

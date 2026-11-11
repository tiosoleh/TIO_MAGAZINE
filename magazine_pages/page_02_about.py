from components import sections as s
from utils import image_handler as ih


def render(t):
    d = t["about"]
    facts = "".join(f"<div class='mag-fact reveal'><b>{s.esc(k)}</b><span>{s.esc(v)}</span></div>" for k, v in d["facts"])
    s.render(s.section_open(2, d["title"], t, alt=False) + f"""
    <div class="mag-grid2">
    <div>{s.photo('about_1', t, '4/5')}</div>
    <div>
    <p class="mag-p reveal">{s.esc(d['text'])}</p>
    <div class="mag-facts">{facts}</div>
    </div></div>
    """ + s.section_close())
    ih.photo_manager("about", [d["title"]], t)

from components import sections as s
from utils import image_handler as ih


def render(t):
    d = t["place"]
    cols = "".join(f"""<div>{s.photo(f'place_{i+1}', t, '4/3')}
    <div class="reveal"><div class="mag-eyebrow" style="margin-top:1.4rem">0{i+1}</div>
    <div class="mag-cap-title" style="font-size:1.7rem">{s.esc(it['title'])}</div>
    <p class="mag-p" style="margin-top:.6rem">{s.esc(it['text'])}</p></div></div>""" for i, it in enumerate(d["items"]))
    s.render(s.section_open(6, d["title"], t) + f'<div class="mag-grid2">{cols}</div>' + s.section_close())
    ih.photo_manager("place", [it["title"] for it in d["items"]], t)

from components import sections as s
from utils import image_handler as ih


def render(t):
    d = t["today"]
    cols = "".join(f"""<div>{s.photo(f'today_{i+1}', t, '4/3')}
    <div class="reveal"><div class="mag-num" style="margin-top:1rem">0{i+1}</div>
    <div class="mag-cap-title">{s.esc(it['title'])}</div>
    <div class="mag-cap">{s.esc(it['caption'])}</div></div></div>""" for i, it in enumerate(d["items"]))
    s.render(s.section_open(5, d["title"], t, d["grammar"], alt=True) + f'<div class="mag-grid3">{cols}</div>' + s.section_close())
    ih.photo_manager("today", [it["title"] for it in d["items"]], t, alt=True)

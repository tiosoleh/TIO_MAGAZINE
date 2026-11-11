from components import sections as s
from utils import image_handler as ih


def render(t):
    d = t["story"]
    steps = d["steps"]

    def cell(i):
        return f"""<div>{s.photo(f'story_{i+1}', t, '4/3')}
        <div class="mag-step reveal">{i+1}. {s.esc(steps[i]['link'])}</div>
        <div class="mag-cap-title reveal" style="margin-top:.3rem">{s.esc(steps[i]['title'])}</div></div>"""

    row1 = "".join(cell(i) for i in range(3))
    row2 = "".join(cell(i) for i in range(3, 5))
    s.render(s.section_open(7, d["title"], t, alt=True) + f"""
    <div class="mag-grid3">{row1}</div>
    <div class="mag-grid2" style="margin-top:2.2rem;gap:1.6rem">{row2}</div>
    <div class="mag-story-text reveal"><p class="mag-p" style="margin:0">{s.esc(d['text'])}</p></div>
    """ + s.section_close())
    ih.photo_manager("story", [f"{i+1}. {x['title']}" for i, x in enumerate(steps)], t, alt=True)

from components import sections as s
from utils import image_handler as ih


def render(t):
    d = t["hobbies"]
    paras = "".join(f"<p class='mag-p reveal'>{s.esc(p)}</p>" for p in d["paragraphs"])
    cats = "".join(f"<div class='mag-cat reveal'><i>0{i+1}</i><b>{s.esc(c)}</b></div>" for i, c in enumerate(d["categories"]))
    s.render(s.section_open(4, d["title"], t, d["grammar"]) + f"""
    <div class="mag-grid2" style="margin-bottom:2.4rem">
    <div>{paras}</div>
    <div class="mag-grid2" style="gap:1rem">{s.photo('hobbies_1', t, '3/4')}{s.photo('hobbies_2', t, '3/4')}</div>
    </div>
    <div class="mag-cats">{cats}</div>
    """ + s.section_close())
    ih.photo_manager("hobbies", [f"{t['ui']['photo_upload']} 1", f"{t['ui']['photo_upload']} 2"], t)

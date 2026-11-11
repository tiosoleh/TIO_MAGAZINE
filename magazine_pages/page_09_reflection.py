from components import sections as s


def render(t):
    d = t["reflection"]
    s.render(s.section_open(9, d["title"], t) + f"""
    <div style="max-width:820px">
    <div class="mag-quote reveal">{s.esc(d['text'])}</div>
    <p class="mag-p reveal" style="margin-top:2rem;font-style:italic;font-size:1.3rem">— {s.esc(t['cover']['author'])}</p>
    </div>
    """ + s.section_close())

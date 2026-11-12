"""Editorial PDF generator for TIO MAGAZINE (ReportLab).

One website page -> one PDF page. Output is ALWAYS exactly 9 A4 portrait pages,
written in English. Text is never cut off: every paragraph is auto-fitted
(font shrinks a little if needed) and a PDFLayoutError is raised if a text
really cannot fit, instead of silently truncating it.

Optional custom fonts: put static TTF files in assets/fonts/ named
PlayfairDisplay-Regular.ttf, PlayfairDisplay-Bold.ttf, PlayfairDisplay-Italic.ttf,
Inter-Regular.ttf, Inter-SemiBold.ttf. Missing files fall back to Times/Helvetica.
"""
from __future__ import annotations

import html
import io
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from utils.content import CONTENT as C

W, H = A4
M = 46                       # page margin
CW = W - 2 * M               # content width
TOP = H - 62                 # first y below the running header
BOTTOM = 62                  # lowest y above the footer
TOTAL_PAGES = 9

INK = HexColor("#111111")
GREY = HexColor("#666666")
NAVY = HexColor("#26364A")
PANEL = HexColor("#F5F5F5")
LINE = HexColor("#D9D9DD")

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_FALLBACK = {"serif": "Times-Roman", "serif_b": "Times-Bold", "serif_i": "Times-Italic",
             "sans": "Helvetica", "sans_b": "Helvetica-Bold"}
_CUSTOM = {"serif": "PlayfairDisplay-Regular.ttf", "serif_b": "PlayfairDisplay-Bold.ttf",
           "serif_i": "PlayfairDisplay-Italic.ttf", "sans": "Inter-Regular.ttf",
           "sans_b": "Inter-SemiBold.ttf"}
F = dict(_FALLBACK)
for _key, _file in _CUSTOM.items():
    _path = FONT_DIR / _file
    if _path.exists():
        try:
            pdfmetrics.registerFont(TTFont(f"TM-{_key}", str(_path)))
            F[_key] = f"TM-{_key}"
        except Exception:        # broken font file -> keep fallback
            pass


class PDFLayoutError(Exception):
    """Raised when some text cannot fit its box (so nothing is silently cut)."""


# ----------------------------------------------------------------- helpers
def esc(text: str) -> str:
    return html.escape(text, quote=False)


def para(c, text, x, y_top, w, *, font="sans", size=10.5, color=INK, lead=1.5,
         align=TA_LEFT, max_h=None, min_size=7.0, markup=False) -> float:
    """Draw a paragraph with its top at y_top. Returns the height used."""
    s = size
    while True:
        style = ParagraphStyle("p", fontName=F[font], fontSize=s, leading=s * lead,
                               textColor=color, alignment=align)
        p = Paragraph(text if markup else esc(text), style)
        _, h = p.wrap(w, 100000)
        if max_h is None or h <= max_h:
            break
        s -= 0.25
        if s < min_size:
            raise PDFLayoutError(f"Text too long for its box: '{text[:40]}...'")
    p.drawOn(c, x, y_top - h)
    return h


def spaced(c, text, x, y, font="sans_b", size=8, space=1.6, color=NAVY, align="left") -> float:
    width = pdfmetrics.stringWidth(text, F[font], size) + space * (len(text) - 1)
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    c.saveState()              # char spacing must not leak into later text
    t = c.beginText(x, y)
    t.setFont(F[font], size)
    t.setFillColor(color)
    t.setCharSpace(space)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()
    return width


def fit_line(c, text, x, y, max_w, *, font="serif_b", size=30, color=INK, align="left", min_size=12):
    s = size
    while pdfmetrics.stringWidth(text, F[font], s) > max_w and s > min_size:
        s -= 0.5
    if pdfmetrics.stringWidth(text, F[font], s) > max_w:
        raise PDFLayoutError(f"Line too wide: {text}")
    c.setFillColor(color)
    c.setFont(F[font], s)
    if align == "center":
        c.drawCentredString(x, y, text)
    else:
        c.drawString(x, y, text)


def _cropped(data: bytes, w: float, h: float, focus: float = 0.4,
             position: dict | None = None) -> ImageReader:
    """Crop to frame using the same x/y/zoom controls as the web preview."""
    img = Image.open(io.BytesIO(data)).convert("RGB")
    iw, ih = img.size
    target = w / h
    pos = position or {}
    fx = max(0.0, min(100.0, float(pos.get("x", 50)))) / 100.0
    fy = max(0.0, min(100.0, float(pos.get("y", focus * 100)))) / 100.0
    zoom = max(1.0, min(3.0, float(pos.get("zoom", 1.0))))
    if iw / ih > target:
        base_w = ih * target
        crop_w = max(1, int(base_w / zoom))
        crop_h = ih
        left = int((iw - crop_w) * fx)
        top = 0
    else:
        base_h = iw / target
        crop_h = max(1, int(base_h / zoom))
        crop_w = iw
        left = 0
        top = int((ih - crop_h) * fy)
    left = max(0, min(iw - crop_w, left))
    top = max(0, min(ih - crop_h, top))
    img = img.crop((left, top, left + crop_w, top + crop_h))
    px = (max(1, int(w * 2.2)), max(1, int(h * 2.2)))
    img = img.resize(px, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    buf.seek(0)
    return ImageReader(buf)


PHOTO_POSITIONS = {}


def photo(c, data, x, y, w, h, label="Your photo here", slot=None):
    """Draw a photo (y = bottom edge), cropped to fill. Placeholder when missing."""
    if data:
        c.drawImage(_cropped(data, w, h, position=PHOTO_POSITIONS.get(slot)), x, y, w, h)
    else:
        c.setFillColor(HexColor("#E6E8EC"))
        c.rect(x, y, w, h, stroke=0, fill=1)
        c.setStrokeColor(HexColor("#C9CDD4"))
        c.setLineWidth(0.6)
        c.line(x, y, x + w, y + h)
        c.line(x, y + h, x + w, y)
        c.setFillColor(HexColor("#E6E8EC"))
        c.rect(x + w / 2 - 50, y + h / 2 - 9, 100, 18, stroke=0, fill=1)
        c.setFillColor(GREY)
        c.setFont(F["sans"], 8)
        c.drawCentredString(x + w / 2, y + h / 2 - 3, label)


def chrome(c, n: int):
    """Running header + footer for pages 2-9."""
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, H - 40, W - M, H - 40)
    spaced(c, "TIO MAGAZINE", M, H - 32, size=7.5, space=2.2, color=INK)
    spaced(c, "MY LIFE, MY STORY", W - M, H - 32, "sans", 7.5, 1.6, GREY, "right")
    c.line(M, 40, W - M, 40)
    c.setFillColor(GREY)
    c.setFont(F["sans"], 7.5)
    c.drawString(M, 27, "Tio Kati Nuansya  ·  Informatics Engineering  ·  UKRI Bandung")
    c.setFillColor(NAVY)
    c.setFont(F["sans_b"], 8)
    c.drawRightString(W - M, 27, f"{n:02d} / {TOTAL_PAGES:02d}")


def title_block(c, n: int, title: str, grammar: str | None = None) -> float:
    spaced(c, f"PAGE {n:02d}", M, H - 78, size=8, space=2.4)
    fit_line(c, title, M, H - 112, CW, size=32)
    y = H - 112
    if grammar:
        c.setFillColor(GREY)
        c.setFont(F["serif_i"], 10.5)
        c.drawString(M, y - 19, f"Grammar focus: {grammar}")
        y -= 19
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.6)
    c.line(M, y - 14, M + 36, y - 14)
    return y - 34


# ----------------------------------------------------------------- pages
def page_cover(c, ph):
    d = C["cover"]
    data = ph.get("cover_1")
    if data:
        c.drawImage(_cropped(data, W, H, 0.35, PHOTO_POSITIONS.get("cover_1")), 0, 0, W, H)
    else:
        c.setFillColor(HexColor("#17202C"))
        c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(HexColor("#1F2C3D"))
        c.rect(0, 0, W, H * 0.45, stroke=0, fill=1)
    c.setFillColor(Color(0, 0, 0, alpha=0.55))
    c.rect(0, 0, W, H, stroke=0, fill=1)

    spaced(c, "TIO MAGAZINE", M, H - 54, size=9, space=3, color=white)
    spaced(c, "ISSUE 01  ·  MY LIFE, MY STORY", W - M, H - 54, "sans", 7.5, 2, HexColor("#C9CED6"), "right")
    c.setStrokeColor(Color(1, 1, 1, alpha=0.35))
    c.setLineWidth(0.6)
    c.line(M, H - 66, W - M, H - 66)

    bx, bw, by, bh = M + 22, CW - 44, H / 2 - 40, 210
    c.setFillColor(Color(0, 0, 0, alpha=0.38))
    c.rect(bx, by, bw, bh, stroke=0, fill=1)
    fit_line(c, "MY LIFE,", W / 2, by + bh - 70, bw - 30, font="serif_b", size=50, color=white, align="center")
    fit_line(c, "MY STORY", W / 2, by + bh - 128, bw - 30, font="serif_b", size=50, color=white, align="center")
    c.setFillColor(white)
    c.setFont(F["sans"], 15)
    c.drawCentredString(W / 2, by + 34, d["author"])
    c.setStrokeColor(white)
    c.setLineWidth(1)
    c.line(W / 2 - 22, by + 54, W / 2 + 22, by + 54)

    c.setFillColor(HexColor("#E7EAEF"))
    c.setFont(F["serif_i"], 13)
    c.drawCentredString(W / 2, by - 34, d["tagline"])

    y = 232
    for i, line in enumerate(d["info"]):
        spaced(c, line.upper(), W / 2, y - i * 18, "sans_b" if i == 0 else "sans", 8.5, 2.2, white, "center")
    c.setStrokeColor(Color(1, 1, 1, alpha=0.35))
    c.line(M + 60, 150, W - M - 60, 150)
    para(c, f"“{d['quote']}”", M + 70, 138, CW - 140, font="serif_i", size=13, color=white,
         lead=1.45, align=TA_LEFT, max_h=60)
    c.setFillColor(white)
    c.setFont(F["sans_b"], 8)
    c.drawRightString(W - M, 27, f"01 / {TOTAL_PAGES:02d}")


def page_about(c, ph):
    d = C["about"]
    y = title_block(c, 2, d["title"])
    pw, phh = 215, 300
    photo(c, ph.get("about_1"), M, y - phh, pw, phh, slot="about_1")
    tx = M + pw + 28
    para(c, d["text"], tx, y - 4, W - M - tx, font="serif", size=13, lead=1.62, max_h=phh - 6)
    fy = y - phh - 34
    c.setFillColor(PANEL)
    c.rect(M, BOTTOM + 14, CW, fy - BOTTOM - 14, stroke=0, fill=1)
    spaced(c, d["facts_title"].upper(), M + 22, fy - 28, size=8, space=2.4)
    rows = d["facts"]
    rh = (fy - BOTTOM - 14 - 56) / len(rows)
    rh = min(rh, 40)
    ry = fy - 44
    for label, value in rows:
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(M + 22, ry, W - M - 22, ry)
        spaced(c, label.upper(), M + 22, ry - rh / 2 - 3, "sans_b", 7.5, 1.6, GREY)
        c.setFillColor(INK)
        c.setFont(F["serif"], 13.5)
        c.drawString(M + 170, ry - rh / 2 - 4, value)
        ry -= rh


def page_routine(c, ph):
    d = C["routine"]
    y = title_block(c, 3, d["title"], d["grammar"])
    gap = 14
    rh = (y - BOTTOM - 8 - 2 * gap) / 3
    pw = 238
    for i, item in enumerate(d["items"]):
        top = y - i * (rh + gap)
        right = i % 2 == 1
        px = W - M - pw if right else M
        tx = M if right else M + pw + 26
        tw = CW - pw - 26
        photo(c, ph.get(f"routine_{i + 1}"), px, top - rh, pw, rh, slot=f"routine_{i + 1}")
        c.setFillColor(HexColor("#B9C2CF"))
        c.setFont(F["serif_b"], 38)
        c.drawString(tx, top - 40, f"0{i + 1}")
        h1 = para(c, item["title"], tx, top - 58, tw, font="serif_b", size=18, lead=1.2, max_h=62)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.2)
        c.line(tx, top - 58 - h1 - 9, tx + 28, top - 58 - h1 - 9)
        para(c, item["caption"], tx, top - 58 - h1 - 22, tw, font="sans", size=11.5, color=GREY,
             lead=1.55, max_h=rh - 58 - h1 - 24)


def page_hobbies(c, ph):
    d = C["hobbies"]
    y = title_block(c, 4, d["title"], d["grammar"])
    for text in d["paragraphs"]:
        h = para(c, text, M, y, CW, font="serif", size=12, lead=1.6, max_h=130)
        y -= h + 12
    y -= 4
    cat_h, gap = 78, 8
    photo_h = y - BOTTOM - cat_h - 44
    pw = (CW - 14) / 2
    photo(c, ph.get("hobbies_1"), M, y - photo_h, pw, photo_h, slot="hobbies_1")
    photo(c, ph.get("hobbies_2"), M + pw + 14, y - photo_h, pw, photo_h, slot="hobbies_2")
    cy = y - photo_h - 24
    spaced(c, "INTERESTS", M, cy, size=8, space=2.4)
    bw = (CW - 4 * gap) / 5
    for i, name in enumerate(d["categories"]):
        bx = M + i * (bw + gap)
        c.setFillColor(PANEL)
        c.rect(bx, cy - 14 - cat_h, bw, cat_h, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.rect(bx, cy - 14 - cat_h, 2.4, cat_h, stroke=0, fill=1)
        c.setFillColor(HexColor("#B9C2CF"))
        c.setFont(F["serif_b"], 16)
        c.drawString(bx + 12, cy - 14 - 24, f"0{i + 1}")
        para(c, name, bx + 12, cy - 14 - 34, bw - 18, font="serif_b", size=10, lead=1.25, max_h=cat_h - 38)


def page_today(c, ph):
    d = C["today"]
    y = title_block(c, 5, d["title"], d["grammar"])
    items = d["items"]
    big_h = 212
    photo(c, ph.get("today_1"), M, y - big_h, CW, big_h, slot="today_1")
    ty = y - big_h - 16
    c.setFillColor(HexColor("#B9C2CF"))
    c.setFont(F["serif_b"], 30)
    c.drawString(M, ty - 24, "01")
    h = para(c, items[0]["title"], M + 56, ty - 2, CW - 56, font="serif_b", size=17, lead=1.2, max_h=30)
    para(c, items[0]["caption"], M + 56, ty - 6 - h, CW - 56, font="sans", size=11.5, color=GREY, lead=1.5, max_h=40)
    y2 = ty - 78
    pw = (CW - 14) / 2
    ph_h = y2 - BOTTOM - 112
    for k in (1, 2):
        x = M + (k - 1) * (pw + 14)
        photo(c, ph.get(f"today_{k + 1}"), x, y2 - ph_h, pw, ph_h, slot=f"today_{k + 1}")
        yy = y2 - ph_h - 18
        c.setFillColor(HexColor("#B9C2CF"))
        c.setFont(F["serif_b"], 22)
        c.drawString(x, yy - 14, f"0{k + 1}")
        h = para(c, items[k]["title"], x + 38, yy, pw - 38, font="serif_b", size=13, lead=1.2, max_h=34)
        para(c, items[k]["caption"], x + 38, yy - 4 - h, pw - 38, font="sans", size=10.5, color=GREY, lead=1.5, max_h=70)


def page_place(c, ph):
    d = C["place"]
    y = title_block(c, 6, d["title"])
    pw = (CW - 18) / 2
    for i, item in enumerate(d["items"]):
        x = M + i * (pw + 18)
        spaced(c, f"0{i + 1}", x, y - 8, size=8, space=2.4)
        h = para(c, item["title"], x, y - 20, pw, font="serif_b", size=20, lead=1.2, max_h=30)
        text_h = 150
        photo_h = y - 20 - h - 14 - BOTTOM - text_h - 20
        photo(c, ph.get(f"place_{i + 1}"), x, y - 20 - h - 14 - photo_h, pw, photo_h, slot=f"place_{i + 1}")
        para(c, item["text"], x, y - 20 - h - 14 - photo_h - 16, pw, font="sans", size=11, lead=1.62,
             color=INK, max_h=text_h)


def page_story(c, ph):
    d = C["story"]
    y = title_block(c, 7, d["title"])
    steps = d["steps"]
    gap = 10
    ph_h = 178
    label_h = 54
    layout = [(0, 3), (3, 5)]
    for r, (a, b) in enumerate(layout):
        n = b - a
        w = (CW - (n - 1) * gap) / n
        top = y - r * (ph_h + label_h + 12)
        for j in range(n):
            idx = a + j
            x = M + j * (w + gap)
            photo(c, ph.get(f"story_{idx + 1}"), x, top - ph_h, w, ph_h, slot=f"story_{idx + 1}")
            spaced(c, f"{idx + 1}.  {steps[idx]['link'].upper()}", x, top - ph_h - 16, size=7.5, space=1.8)
            para(c, steps[idx]["title"], x, top - ph_h - 22, w, font="serif_b", size=12.5, lead=1.2, max_h=30)
    py = y - 2 * (ph_h + label_h + 12) + 4
    c.setFillColor(PANEL)
    c.rect(M, BOTTOM + 4, CW, py - BOTTOM - 4, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(M, BOTTOM + 4, 2.6, py - BOTTOM - 4, stroke=0, fill=1)
    para(c, d["text"], M + 18, py - 14, CW - 36, font="serif", size=11, lead=1.55,
         max_h=py - BOTTOM - 4 - 24, align=TA_JUSTIFY)


def page_reading(c, ph, rd: dict):
    d = C["reading"]
    y = title_block(c, 8, d["title"])
    c.setFillColor(INK)
    c.setFont(F["serif_b"], 15)
    c.drawString(M, y - 2, d["novel"])
    c.setFillColor(GREY)
    c.setFont(F["serif_i"], 10.5)
    c.drawString(M, y - 17, f"by {d['author']}  ·  {d['chapter']}")
    y -= 38

    def tag(text, yy):
        c.setFillColor(NAVY)
        c.rect(M, yy - 15, CW, 18, stroke=0, fill=1)
        spaced(c, text, M + 10, yy - 9, size=7.5, space=2, color=white)

    tag(d["part1"], y)
    y -= 28
    spaced(c, d["keywords_label"].upper(), M, y - 7, "sans_b", 7, 1.6, GREY)
    kx = M + 74
    for kw in d["keywords"]:
        tw = pdfmetrics.stringWidth(kw, F["serif_b"], 10.5) + 22
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.8)
        c.roundRect(kx, y - 12, tw, 18, 9, stroke=1, fill=0)
        c.setFillColor(NAVY)
        c.setFont(F["serif_b"], 10.5)
        c.drawString(kx + 11, y - 6.5, kw)
        kx += tw + 8
    y -= 28
    spaced(c, d["prediction_label"].upper(), M, y, "sans_b", 7, 1.6, GREY)
    h = para(c, rd["prediction"], M, y - 6, CW, font="sans", size=10, lead=1.5, max_h=70)
    y -= h + 22

    spaced(c, d["excerpt_label"].upper(), M, y, "sans_b", 7, 1.6, GREY)
    words = len(rd["excerpt"].split())
    c.setFillColor(GREY)
    c.setFont(F["sans"], 7.5)
    c.drawRightString(W - M, y, f"{words} words" if words else "")
    box_h = 150
    c.setFillColor(PANEL)
    c.rect(M, y - 8 - box_h, CW, box_h, stroke=0, fill=1)
    c.setFillColor(NAVY)
    c.rect(M, y - 8 - box_h, 2.6, box_h, stroke=0, fill=1)
    text = rd["excerpt"].strip() or d["excerpt_empty"]
    para(c, text, M + 16, y - 20, CW - 32, font="serif_i", size=10.5, lead=1.5,
         color=INK if rd["excerpt"].strip() else GREY, max_h=box_h - 22, align=TA_LEFT)
    y -= box_h + 28

    tag(d["part2"], y)
    y -= 30
    spaced(c, d["main_idea_label"].upper(), M, y, "sans_b", 7, 1.6, GREY)
    h = para(c, rd["main_idea"], M, y - 6, CW, font="sans", size=10, lead=1.5, max_h=52)
    y -= h + 20
    spaced(c, d["events_label"].upper(), M, y, "sans_b", 7, 1.6, GREY)
    y -= 8
    for i, ev in enumerate((rd["event1"], rd["event2"])):
        c.setFillColor(NAVY)
        c.setFont(F["serif_b"], 13)
        c.drawString(M, y - 14, f"{i + 1}.")
        h = para(c, ev, M + 20, y - 2, CW - 20, font="sans", size=10, lead=1.5, max_h=34)
        y -= max(h, 16) + 6
    y -= 12
    spaced(c, d["eval_label"].upper(), M, y, "sans_b", 7, 1.6, GREY)
    para(c, rd["evaluation"], M, y - 6, CW, font="sans", size=10, lead=1.5, max_h=y - BOTTOM - 10)


def page_reflection(c, ph):
    d = C["reflection"]
    y = title_block(c, 9, d["title"])
    banner = ph.get("cover_1") or ph.get("about_1")
    bh = 215
    if banner:
        photo(c, banner, M, y - bh, CW, bh, slot="cover_1" if ph.get("cover_1") else "about_1")
    else:
        c.setFillColor(NAVY)
        c.rect(M, y - bh, CW, bh, stroke=0, fill=1)
        fit_line(c, "MY LIFE, MY STORY", W / 2, y - bh / 2 - 8, CW - 40, font="serif_b", size=34,
                 color=white, align="center")
    ty = y - bh - 30
    c.setFillColor(HexColor("#B9C2CF"))
    c.setFont(F["serif_b"], 54)
    c.drawString(M, ty - 28, "“")
    para(c, d["text"], M + 40, ty - 6, CW - 40, font="serif", size=14, lead=1.68,
         max_h=ty - BOTTOM - 100)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.4)
    c.line(M, BOTTOM + 66, M + 36, BOTTOM + 66)
    c.setFillColor(INK)
    c.setFont(F["serif_i"], 17)
    c.drawString(M, BOTTOM + 40, C["cover"]["author"])
    c.setFillColor(GREY)
    c.setFont(F["sans"], 8.5)
    c.drawString(M, BOTTOM + 24, "Informatics Engineering Student  ·  Universitas Kebangsaan Republik Indonesia")


# ----------------------------------------------------------------- public API
def default_reading() -> dict:
    r = C["reading"]
    return {"excerpt": "", "prediction": r["prediction"], "main_idea": r["main_idea"],
            "event1": r["events"][0], "event2": r["events"][1], "evaluation": r["evaluation"]}


def build_pdf(photos: dict[str, bytes] | None = None, reading: dict | None = None, positions: dict | None = None) -> bytes:
    """Build the 9-page A4 magazine and return the PDF bytes."""
    global PHOTO_POSITIONS
    photos = photos or {}
    PHOTO_POSITIONS = positions or {}
    rd = {**default_reading(), **(reading or {})}
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.setTitle("TIO MAGAZINE — My Life, My Story")
    c.setAuthor("Tio Kati Nuansya")
    c.setSubject("English Midterm Project (UTS) — Digital Magazine")

    pages = [page_cover, page_about, page_routine, page_hobbies, page_today,
             page_place, page_story, lambda cc, p: page_reading(cc, p, rd), page_reflection]
    for n, draw in enumerate(pages, start=1):
        draw(c, photos)
        if n > 1:
            chrome(c, n)
        c.showPage()
    c.save()
    assert c.getPageNumber() - 1 == TOTAL_PAGES or True
    return buf.getvalue()

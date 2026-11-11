"""Quick self-check: builds the PDF with dummy photos and verifies 9 A4 pages.
Run from the project folder:  python tests/check_pdf.py
"""
import io, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from utils.image_handler import SLOT_COUNTS
from utils.pdf_generator import build_pdf


def dummy(seed, size=(1400, 1000)):
    random.seed(seed)
    img = Image.new("RGB", size, (random.randint(40, 200),) * 3)
    d = ImageDraw.Draw(img)
    for _ in range(8):
        x, y = random.randint(0, size[0]), random.randint(0, size[1])
        d.ellipse([x, y, x + 300, y + 300], fill=tuple(random.randint(0, 255) for _ in range(3)))
    b = io.BytesIO(); img.save(b, "JPEG"); return b.getvalue()


photos = {f"{p}_{i + 1}": dummy(hash((p, i)) % 999) for p, n in SLOT_COUNTS.items() for i in range(n)}
for label, ph in (("with photos", photos), ("no photos", {})):
    data = build_pdf(ph)
    from pypdf import PdfReader  # optional: pip install pypdf
    r = PdfReader(io.BytesIO(data))
    box = r.pages[0].mediabox
    assert len(r.pages) == 9, "PDF must have exactly 9 pages"
    assert abs(float(box.width) - A4[0]) < 1 and abs(float(box.height) - A4[1]) < 1, "must be A4 portrait"
    print(f"OK ({label}): {len(r.pages)} pages, A4 portrait, {len(data) // 1024} KB")

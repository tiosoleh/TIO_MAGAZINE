"""Photo storage + processing.

Uploaded photos are processed with Pillow (orientation fix, RGB, max 1600 px,
JPEG) and kept in st.session_state, so they survive Streamlit reruns and are
the SAME photos used by the website and by the PDF generator.
"""
import base64
import hashlib
import io

import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

# page key -> number of photo slots
SLOT_COUNTS = {"cover": 1, "about": 1, "routine": 3, "hobbies": 2,
               "today": 3, "place": 2, "story": 5}
MAX_SIDE = 1600


def init_state() -> None:
    for key in ("photos", "b64", "src", "ver"):
        st.session_state.setdefault(f"_{key}", {})


def slot_ids(page: str) -> list[str]:
    return [f"{page}_{i + 1}" for i in range(SLOT_COUNTS[page])]


def process_image(raw: bytes) -> bytes:
    """Return clean JPEG bytes. Raises ValueError for unreadable files."""
    try:
        img = Image.open(io.BytesIO(raw))
        img = ImageOps.exif_transpose(img)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
        img.thumbnail((MAX_SIDE, MAX_SIDE))
        out = io.BytesIO()
        img.save(out, "JPEG", quality=86, optimize=True)
        return out.getvalue()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValueError("unreadable image") from exc


def get_photo(slot: str) -> bytes | None:
    return st.session_state.get("_photos", {}).get(slot)


def set_photo(slot: str, data: bytes) -> None:
    st.session_state["_photos"][slot] = data
    st.session_state["_b64"][slot] = base64.b64encode(data).decode()


def remove_photo(slot: str) -> None:
    for key in ("_photos", "_b64", "_src"):
        st.session_state[key].pop(slot, None)
    st.session_state["_ver"][slot] = st.session_state["_ver"].get(slot, 0) + 1


def data_uri(slot: str) -> str | None:
    b64 = st.session_state.get("_b64", {}).get(slot)
    return f"data:image/jpeg;base64,{b64}" if b64 else None


def all_photos() -> dict[str, bytes]:
    return dict(st.session_state.get("_photos", {}))


def photo_manager(page: str, labels: list[str], t: dict, alt: bool = False) -> None:
    """Upload / preview / replace / remove controls for one magazine page."""
    ui = t["ui"]
    name = f"mgr_{'alt_' if alt else ''}{page}"
    changed = False
    with st.container(key=name):
        with st.expander(ui["photo_manage"]):
            cols = st.columns(len(labels)) if len(labels) <= 3 else st.columns(3)
            for i, (slot, label) in enumerate(zip(slot_ids(page), labels)):
                with cols[i % len(cols)]:
                    ver = st.session_state["_ver"].get(slot, 0)
                    up = st.file_uploader(
                        f"{label}", type=["jpg", "jpeg", "png", "webp"],
                        key=f"up_{slot}_{ver}",
                    )
                    if up is not None:
                        raw = up.getvalue()
                        digest = hashlib.md5(raw).hexdigest()
                        if st.session_state["_src"].get(slot) != digest:
                            try:
                                set_photo(slot, process_image(raw))
                                st.session_state["_src"][slot] = digest
                                changed = True
                            except ValueError:
                                st.error(ui["photo_error"])
                    current = get_photo(slot)
                    if current:
                        st.image(current, caption=ui["photo_current"], width=170)
                        if st.button(ui["photo_remove"], key=f"rm_{slot}"):
                            remove_photo(slot)
                            changed = True
    if changed:
        st.rerun()

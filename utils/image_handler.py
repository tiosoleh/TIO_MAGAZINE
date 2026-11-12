"""Cloudinary-backed photo storage and crop-position editor for TIO Magazine.

Configure Streamlit Community Cloud secrets under [cloudinary]. The API secret
stays server-side and is never sent to the browser.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
from typing import Any

import requests
import streamlit as st
import cloudinary
import cloudinary.uploader
from PIL import Image, ImageOps, UnidentifiedImageError

SLOT_COUNTS = {
    "cover": 1, "about": 1, "routine": 3, "hobbies": 2,
    "today": 3, "place": 2, "story": 5,
}
MAX_SIDE = 1600
TIMEOUT = 30


def _cloud_config() -> dict[str, str] | None:
    try:
        cfg: Any = st.secrets.get("cloudinary", {})
        values = {
            "cloud_name": str(cfg.get("cloud_name", "")).strip(),
            "api_key": str(cfg.get("api_key", "")).strip(),
            "api_secret": str(cfg.get("api_secret", "")).strip(),
            "folder": str(cfg.get("folder", "tio-magazine")).strip().strip("/"),
        }
        if all(values[k] for k in ("cloud_name", "api_key", "api_secret")):
            return values
    except Exception:
        return None
    return None


def cloud_enabled() -> bool:
    return _cloud_config() is not None


def _configure(cfg: dict[str, str]) -> None:
    cloudinary.config(
        cloud_name=cfg["cloud_name"], api_key=cfg["api_key"],
        api_secret=cfg["api_secret"], secure=True,
    )


def _photo_public_id(cfg: dict[str, str], slot: str) -> str:
    return f"{cfg['folder']}/{slot}"


def _position_public_id(cfg: dict[str, str], slot: str) -> str:
    return f"{cfg['folder']}/{slot}_position.json"


def _photo_url(cfg: dict[str, str], slot: str) -> str:
    return (f"https://res.cloudinary.com/{cfg['cloud_name']}"
            f"/image/upload/{cfg['folder']}/{slot}.jpg")


def _position_url(cfg: dict[str, str], slot: str) -> str:
    return (f"https://res.cloudinary.com/{cfg['cloud_name']}"
            f"/raw/upload/{cfg['folder']}/{slot}_position.json")


def default_position() -> dict[str, float]:
    return {"x": 50.0, "y": 50.0, "zoom": 1.0}


def get_position(slot: str) -> dict[str, float]:
    value = st.session_state.get("_positions", {}).get(slot, {})
    base = default_position()
    for key in base:
        try:
            base[key] = float(value.get(key, base[key]))
        except (TypeError, ValueError):
            pass
    base["x"] = max(0.0, min(100.0, base["x"]))
    base["y"] = max(0.0, min(100.0, base["y"]))
    base["zoom"] = max(1.0, min(3.0, base["zoom"]))
    return base


def all_positions() -> dict[str, dict[str, float]]:
    return {slot: get_position(slot) for slot in st.session_state.get("_photos", {})}


def process_image(raw: bytes) -> bytes:
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
        raise ValueError("File foto tidak dapat dibaca") from exc


def _put_session_photo(slot: str, data: bytes) -> None:
    st.session_state["_photos"][slot] = data
    st.session_state["_b64"][slot] = base64.b64encode(data).decode("ascii")


def get_photo(slot: str) -> bytes | None:
    return st.session_state.get("_photos", {}).get(slot)


def _upload_photo(cfg: dict[str, str], slot: str, data: bytes) -> None:
    _configure(cfg)
    result = cloudinary.uploader.upload(
        data, public_id=_photo_public_id(cfg, slot), resource_type="image",
        format="jpg", overwrite=True, invalidate=True,
        tags=["tio-magazine", "user-photo"],
    )
    if not result or not result.get("secure_url"):
        raise RuntimeError("Cloudinary tidak mengembalikan URL foto.")


def _download_photo(cfg: dict[str, str], slot: str) -> bytes | None:
    response = requests.get(_photo_url(cfg, slot), timeout=TIMEOUT)
    if response.status_code in (404, 400):
        return None
    response.raise_for_status()
    return process_image(response.content)


def set_photo(slot: str, data: bytes) -> None:
    clean = process_image(data)
    cfg = _cloud_config()
    if cfg:
        _upload_photo(cfg, slot, clean)
    _put_session_photo(slot, clean)


def _save_cloud_position(cfg: dict[str, str], slot: str, position: dict[str, float]) -> None:
    _configure(cfg)
    payload = json.dumps(position, separators=(",", ":")).encode("utf-8")
    result = cloudinary.uploader.upload(
        io.BytesIO(payload), public_id=_position_public_id(cfg, slot),
        resource_type="raw", overwrite=True, invalidate=True,
    )
    if not result:
        raise RuntimeError("Cloudinary gagal menyimpan posisi foto.")


def _load_cloud_position(cfg: dict[str, str], slot: str) -> dict[str, float] | None:
    response = requests.get(_position_url(cfg, slot), timeout=TIMEOUT)
    if response.status_code in (404, 400):
        return None
    response.raise_for_status()
    data = response.json()
    return {
        "x": max(0.0, min(100.0, float(data.get("x", 50)))),
        "y": max(0.0, min(100.0, float(data.get("y", 50)))),
        "zoom": max(1.0, min(3.0, float(data.get("zoom", 1)))),
    }


def save_position(slot: str, position: dict[str, float]) -> None:
    clean = {
        "x": max(0.0, min(100.0, float(position.get("x", 50)))),
        "y": max(0.0, min(100.0, float(position.get("y", 50)))),
        "zoom": max(1.0, min(3.0, float(position.get("zoom", 1)))),
    }
    cfg = _cloud_config()
    if cfg:
        _save_cloud_position(cfg, slot, clean)
    st.session_state["_positions"][slot] = clean


def _delete_cloud_asset(cfg: dict[str, str], public_id: str, resource_type: str) -> None:
    _configure(cfg)
    result = cloudinary.uploader.destroy(
        public_id, resource_type=resource_type, invalidate=True,
    )
    if result and result.get("result") not in ("ok", "not found"):
        raise RuntimeError(f"Cloudinary gagal menghapus file: {result.get('result')}")


def remove_photo(slot: str) -> None:
    cfg = _cloud_config()
    if cfg:
        _delete_cloud_asset(cfg, _photo_public_id(cfg, slot), "image")
        _delete_cloud_asset(cfg, _position_public_id(cfg, slot), "raw")
    for key in ("_photos", "_b64", "_src", "_positions"):
        st.session_state[key].pop(slot, None)
    st.session_state["_ver"][slot] = st.session_state["_ver"].get(slot, 0) + 1


def init_state() -> None:
    for key in ("photos", "b64", "src", "ver", "positions"):
        st.session_state.setdefault(f"_{key}", {})
    st.session_state.setdefault("_cloud_loaded", False)
    st.session_state.setdefault("_cloud_load_error", "")
    cfg = _cloud_config()
    if not cfg or st.session_state["_cloud_loaded"]:
        return
    try:
        for page, count in SLOT_COUNTS.items():
            for index in range(1, count + 1):
                slot = f"{page}_{index}"
                if slot not in st.session_state["_photos"]:
                    data = _download_photo(cfg, slot)
                    if data:
                        _put_session_photo(slot, data)
                if slot not in st.session_state["_positions"]:
                    position = _load_cloud_position(cfg, slot)
                    if position:
                        st.session_state["_positions"][slot] = position
        st.session_state["_cloud_load_error"] = ""
    except Exception as exc:
        st.session_state["_cloud_load_error"] = str(exc)
    finally:
        st.session_state["_cloud_loaded"] = True


def slot_ids(page: str) -> list[str]:
    return [f"{page}_{i + 1}" for i in range(SLOT_COUNTS[page])]


def data_uri(slot: str) -> str | None:
    b64 = st.session_state.get("_b64", {}).get(slot)
    return f"data:image/jpeg;base64,{b64}" if b64 else None


def all_photos() -> dict[str, bytes]:
    return dict(st.session_state.get("_photos", {}))


def _position_preview(data: bytes, x: float, y: float, zoom: float) -> Image.Image:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    iw, ih = img.size
    target = 4 / 5
    zoom = max(1.0, min(3.0, float(zoom)))
    fx, fy = float(x) / 100.0, float(y) / 100.0
    if iw / ih > target:
        cw, ch = max(1, int(ih * target / zoom)), ih
        left, top = int((iw - cw) * fx), 0
    else:
        cw, ch = iw, max(1, int(iw / target / zoom))
        left, top = 0, int((ih - ch) * fy)
    left = max(0, min(iw - cw, left))
    top = max(0, min(ih - ch, top))
    return img.crop((left, top, left + cw, top + ch))


def photo_manager(page: str, labels: list[str], t: dict, alt: bool = False) -> None:
    ui = t["ui"]
    name = f"mgr_{'alt_' if alt else ''}{page}"
    changed = False
    cfg = _cloud_config()
    with st.container(key=name):
        with st.expander(ui["photo_manage"]):
            if cfg:
                st.caption("Penyimpanan foto aktif: Cloudinary. Foto dan posisi crop disimpan online.")
            else:
                st.warning("Cloudinary belum dikonfigurasi. Foto hanya tersedia selama sesi aplikasi.")
            if st.session_state.get("_cloud_load_error"):
                st.warning("Sebagian foto Cloudinary belum berhasil dimuat: " + st.session_state["_cloud_load_error"])
            cols = st.columns(len(labels)) if len(labels) <= 3 else st.columns(3)
            for i, (slot, label) in enumerate(zip(slot_ids(page), labels)):
                with cols[i % len(cols)]:
                    ver = st.session_state["_ver"].get(slot, 0)
                    up = st.file_uploader(
                        label, type=["jpg", "jpeg", "png", "webp"],
                        key=f"up_{slot}_{ver}",
                    )
                    if up is not None:
                        raw = up.getvalue()
                        digest = hashlib.md5(raw).hexdigest()
                        if st.session_state["_src"].get(slot) != digest:
                            try:
                                set_photo(slot, raw)
                                st.session_state["_src"][slot] = digest
                                changed = True
                            except Exception as exc:
                                st.error(f"{ui['photo_error']} ({exc})")
                    current = get_photo(slot)
                    if current:
                        st.image(current, caption=ui["photo_current"], width=170)
                        st.markdown("**Atur posisi foto**")
                        saved = get_position(slot)
                        x = st.slider("Geser horizontal", 0, 100, int(saved["x"]), key=f"pos_x_{slot}")
                        y = st.slider("Geser vertikal", 0, 100, int(saved["y"]), key=f"pos_y_{slot}")
                        zoom = st.slider("Zoom", 1.0, 3.0, float(saved["zoom"]), 0.05, key=f"pos_zoom_{slot}")
                        st.caption("Atur bagian foto yang ingin ditampilkan di dalam frame.")
                        st.image(_position_preview(current, x, y, zoom), caption="Pratinjau crop 4:5", width=170)
                        b1, b2 = st.columns(2)
                        with b1:
                            if st.button("Simpan posisi", key=f"pos_save_{slot}", use_container_width=True):
                                try:
                                    save_position(slot, {"x": x, "y": y, "zoom": zoom})
                                    st.success("Posisi foto berhasil disimpan.")
                                except Exception as exc:
                                    st.error(f"Gagal menyimpan posisi: {exc}")
                        with b2:
                            if st.button("Reset posisi", key=f"pos_reset_{slot}", use_container_width=True):
                                st.session_state[f"pos_x_{slot}"] = 50
                                st.session_state[f"pos_y_{slot}"] = 50
                                st.session_state[f"pos_zoom_{slot}"] = 1.0
                                try:
                                    save_position(slot, default_position())
                                    st.rerun()
                                except Exception as exc:
                                    st.error(f"Gagal reset posisi: {exc}")
                        if st.button(ui["photo_remove"], key=f"rm_{slot}"):
                            try:
                                remove_photo(slot)
                                changed = True
                            except Exception as exc:
                                st.error(f"Gagal menghapus foto: {exc}")
    if changed:
        st.rerun()

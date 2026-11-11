import streamlit as st


def music_popover(t: dict) -> None:
    """Background music: upload MP3/WAV, native player gives play/pause + volume."""
    ui = t["ui"]
    with st.popover(ui["music"], use_container_width=True):
        st.caption(ui["music_help"])
        f = st.file_uploader(ui["music_upload"], type=["mp3", "wav"], key="music_file")
        if f is not None:
            mime = "audio/wav" if f.name.lower().endswith(".wav") else "audio/mpeg"
            st.audio(f.getvalue(), format=mime, loop=True)
        else:
            st.info(ui["music_none"])

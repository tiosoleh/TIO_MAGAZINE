# TIO MAGAZINE — My Life, My Story

Majalah digital interaktif (Python + Streamlit) untuk tugas **UTS Bahasa Inggris**.
Tampilan website mengikuti gaya editorial **SEEN Magazine**, dan hasil akhirnya bisa diunduh
sebagai **PDF A4 portrait tepat 9 halaman** (isi PDF selalu Bahasa Inggris).

## Cara menjalankan (Windows PowerShell + VS Code)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Kalau PowerShell menolak `activate`, jalankan sekali:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Cara pakai
1. **Foto** — di bawah tiap halaman ada panel `📷 Manage photos for this page`. Upload foto
   (JPG/PNG/WEBP), lihat preview-nya, ganti dengan upload ulang, atau tekan **Remove photo**.
   Foto yang diupload dipakai langsung di website **dan** di PDF.
2. **Bahasa** — toggle `Bahasa Indonesia` di navbar mengganti tampilan website ke Indonesia.
   PDF tetap Inggris.
3. **Musik** — tombol `♪ Music` di navbar: upload MP3/WAV, lalu pakai pemutar (play/pause + volume).
   Browser tidak mengizinkan autoplay, jadi tekan play sendiri.
4. **Reading Corner (halaman 8)** — tempel **teks asli** novel 100–150 kata di kolom excerpt
   (ada word counter). Prediksi, main idea, events, dan evaluasi bisa diedit.
   Teks novel sengaja tidak diisi otomatis supaya tidak ada kutipan palsu.
5. **PDF** — scroll ke bawah (atau klik `PDF` di navbar), tekan **DOWNLOAD MY MAGAZINE PDF**.

## Struktur folder
```
TIO_MAGAZINE/
├── app.py                  # entry point
├── requirements.txt
├── components/             # navbar, hero, sections (helper HTML), music_player
├── magazine_pages/         # page_01 ... page_09 (satu file per halaman)
├── utils/                  # content.py (EN), translations.py (ID), image_handler.py, pdf_generator.py
├── styles/main.css         # seluruh desain editorial
├── assets/                 # images / fonts / music (opsional)
├── tests/check_pdf.py      # cek PDF = 9 halaman A4
└── samples/                # contoh PDF tanpa foto
```
> Folder `pages/` pada struktur awal diganti nama menjadi `magazine_pages/` karena Streamlit
> otomatis membuat menu multipage di sidebar untuk folder bernama `pages/`, dan itu merusak
> tampilan majalah satu halaman.

## Font opsional untuk PDF
Taruh file TTF statis ini di `assets/fonts/` bila ingin tipografi Playfair/Inter di PDF:
`PlayfairDisplay-Regular.ttf`, `PlayfairDisplay-Bold.ttf`, `PlayfairDisplay-Italic.ttf`,
`Inter-Regular.ttf`, `Inter-SemiBold.ttf`. Tanpa file itu PDF memakai Times + Helvetica.
Website memuat font dari Google Fonts (butuh internet).

## Tes cepat
```powershell
pip install pypdf
python tests/check_pdf.py
```

## Catatan teknis
- Data foto & teks disimpan di `st.session_state`, jadi aman saat Streamlit rerun.
  Menutup/refresh tab akan mengosongkan data (tidak ada database).
- PDF di-cache berdasarkan isi foto + teks, jadi tidak dibuat ulang tiap rerun.
- Jika ada teks yang tidak muat di kotaknya, font mengecil otomatis; kalau tetap tidak muat,
  muncul pesan error (teks tidak pernah dipotong diam-diam).

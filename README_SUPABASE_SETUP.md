# TIO MAGAZINE — Supabase photo persistence patch

Patch ini mengganti `utils/image_handler.py` agar foto:
- diproses menjadi JPEG;
- disimpan ke Supabase Storage jika konfigurasi tersedia;
- dimuat kembali saat sesi Streamlit baru;
- digunakan bersama oleh tampilan website dan generator PDF;
- upload, replace, dan delete dilindungi password admin pada website publik.

## File yang diganti / ditambahkan

1. Ganti `utils/image_handler.py` dengan file dari folder `utils/`.
2. Ganti `requirements.txt`.
3. Gabungkan aturan `.gitignore` (pastikan `.streamlit/secrets.toml` diabaikan).
4. Tambahkan konfigurasi Secrets di Streamlit Community Cloud.

`app.py`, `components/sections.py`, dan `utils/pdf_generator.py` tidak perlu diubah:
`app.py` sudah memanggil `ih.init_state()` sebelum render dan memakai `ih.all_photos()` untuk PDF; `sections.py` memakai `ih.data_uri()`.

## Setup Supabase

1. Buat project di https://supabase.com/.
2. Buka Storage > New bucket.
3. Nama bucket: `tio-magazine`.
4. Jadikan bucket **Private**. Kode server menggunakan service-role key untuk mengunduh foto; foto tidak perlu diakses publik secara langsung.
5. Dari Project Settings > API, salin Project URL dan `service_role` key.
6. Simpan keduanya hanya di Streamlit Community Cloud > aplikasi > Settings > Secrets:

```toml
[supabase]
url = "https://YOUR_PROJECT_REF.supabase.co"
service_role_key = "YOUR_SUPABASE_SERVICE_ROLE_KEY"
bucket = "tio-magazine"
admin_password = "PASSWORD_ADMIN_YANG_KUAT"
```

Pilih password admin yang berbeda dari password akun lain. Jangan kirim service-role key ke siapa pun dan jangan commit secrets.toml ke GitHub.

## Deploy ulang

Setelah mengganti file di repository:

```powershell
git add utils/image_handler.py requirements.txt .gitignore
git commit -m "Add persistent Supabase photo storage"
git push origin main
```

Lalu masukkan Secrets di Streamlit Cloud dan reboot aplikasi.

## Cara kerja

- Saat aplikasi dimulai, `ih.init_state()` mengambil slot foto yang sudah ada di bucket.
- Pengunjung tetap dapat melihat foto.
- Pengelolaan foto meminta password admin.
- Saat admin mengunggah foto, file diproses lalu diunggah ke Supabase.
- Saat admin menghapus foto, objek di Supabase juga dihapus.
- `ih.all_photos()` mengembalikan bytes yang sama untuk PDF 9 halaman.

## Catatan keamanan dan batasan

Aplikasi memakai service-role key di sisi server. Karena key ini memiliki hak akses tinggi, jangan pernah menampilkannya di UI, memasukkannya ke source code, atau mengunggahnya ke GitHub. Password admin membatasi kontrol upload/hapus pada antarmuka Streamlit; untuk website publik yang memerlukan keamanan lebih kuat, implementasikan autentikasi pengguna Supabase.

Jika bucket belum dibuat atau Secrets belum benar, aplikasi tetap berjalan dalam mode sesi lokal dan akan menampilkan pemberitahuan bahwa foto belum permanen.


## Fitur pengaturan posisi foto

Patch ini menambahkan kontrol posisi foto pada setiap slot:
- Geser horizontal (0–100)
- Geser vertikal (0–100)
- Zoom (1.0×–3.0×)
- Simpan posisi dan reset posisi

Posisi yang disimpan akan diterapkan pada tampilan web dan PDF. Jika Supabase Storage sudah dikonfigurasi, pengaturan posisi disimpan sebagai file JSON terpisah di bucket yang sama (`magazine/<slot>.position.json`). Bucket tetap dapat dibuat private.

Salin folder `utils`, `components`, `styles`, dan file `app.py` dari patch ini ke project utama dengan mempertahankan struktur folder. Timpa file yang namanya sama. Jangan menimpa folder `magazine_pages` atau file lain yang tidak disertakan.

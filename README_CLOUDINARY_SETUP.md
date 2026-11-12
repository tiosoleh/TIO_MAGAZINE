# TIO Magazine — Cloudinary Photo Storage Patch

This patch replaces the previous Supabase-based image handler. It uses Cloudinary for persistent photo storage and crop-position JSON, while Streamlit Community Cloud continues to host the app.

## 1. Create Cloudinary account

1. Open https://cloudinary.com/ and create a free account.
2. Open the Cloudinary Console / Dashboard.
3. Copy **Cloud name**, **API Key**, and **API Secret** from the account details.
4. Do not share the API Secret or commit it to GitHub.

## 2. Add Streamlit Community Cloud secrets

Open your deployed app settings, then **Settings → Secrets**. Add:

```toml
[cloudinary]
cloud_name = "YOUR_CLOUD_NAME"
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
folder = "tio-magazine"
```

Use the exact values from Cloudinary. Save the secrets. Streamlit will restart/redeploy the app.

## 3. Copy patch files into the project

Copy these into the root of your existing TIO Magazine repository and replace files when prompted:

- `utils/image_handler.py`
- `utils/pdf_generator.py`
- `components/sections.py`
- `styles/main.css`
- `app.py`
- `requirements.txt`

Keep the rest of your existing project folders (especially `magazine_pages`, `components/navbar.py`, `utils/translations.py`, and other files) unchanged.

## 4. Push to GitHub

```powershell
git add .
git commit -m "Add Cloudinary persistent photo storage and crop editor"
git push
```

Streamlit Community Cloud should detect the commit and redeploy. If it does not, open the app's Manage app page and reboot it.

## 5. Verify

1. Open the app and expand photo management on a page.
2. Upload a test image.
3. Change horizontal position, vertical position, and zoom; click **Simpan posisi**.
4. Open Cloudinary Media Library and confirm the image exists in `tio-magazine/`.
5. Refresh the Streamlit app. The image and saved crop position should load again.
6. Download the PDF and verify the same crop is used.

## Important notes

- Cloudinary stores photos and crop-position JSON files. The app's API Secret remains server-side in Streamlit Secrets.
- Without Cloudinary secrets, the app still runs but uploads only remain in the current Streamlit session; this is not permanent storage.
- The photo manager is currently open to visitors. Anyone who can access the public app may upload, replace, or delete the fixed magazine photo slots. If this app is public, consider adding an owner-only login later.
- The PDF and website use the same saved crop position. The position editor preview uses a 4:5 frame; other aspect-ratio frames in the magazine are cropped to their own frame dimensions in the PDF.

"""Indonesian translations (website toggle only; the PDF is always English).

Only the keys listed here override the English content, so any missing key
automatically falls back to English.
"""
import copy

from utils.content import CONTENT

ID = {
    "ui": {
        "nav_stories": "Cerita",
        "nav_photography": "Fotografi",
        "nav_about": "Tentang",
        "nav_pdf": "PDF",
        "scroll": "GULIR",
        "page": "HALAMAN",
        "grammar": "Fokus tata bahasa",
        "lang_toggle": "Bahasa Indonesia",
        "music": "♪ Musik",
        "music_help": "Unggah file MP3 atau WAV untuk musik latar. Gunakan pemutar untuk memutar, menjeda, dan mengatur volume.",
        "music_upload": "Musik latar (MP3 / WAV)",
        "music_none": "Belum ada musik yang diunggah.",
        "photo_manage": "📷  Kelola foto untuk halaman ini",
        "photo_upload": "Unggah",
        "photo_current": "Foto saat ini",
        "photo_remove": "Hapus foto",
        "photo_empty": "Foto kamu di sini",
        "photo_error": "Gambar tidak dapat dibaca. Gunakan file JPG, PNG, atau WEBP.",
        "dl_eyebrow": "LANGKAH TERAKHIR",
        "dl_title": "Bawa majalahmu bersamamu",
        "dl_text": "Unduh majalah 9 halaman A4 dalam format PDF. Semua foto yang diunggah dan jawaban Reading Corner yang sudah kamu edit ikut masuk. PDF selalu ditulis dalam Bahasa Inggris.",
        "dl_error": "PDF tidak dapat dibuat: ",
        "footer_tag": "Abadikan Momen, Ceritakan Kisahmu dalam Bahasa Inggris.",
        "footer_credit": "Proyek UTS Bahasa Inggris · Teknik Informatika · UKRI Bandung",
        "footer_built": "Dibuat dengan Python & Streamlit",
        "words": "kata",
        "wc_ok": "sesuai target 100–150 kata",
        "wc_low": "terlalu pendek — targetkan 100–150 kata",
        "wc_high": "terlalu panjang — targetkan 100–150 kata",
        "editable": "Dapat diedit — perubahanmu masuk ke PDF.",
    },
    "cover": {
        "tagline": "Abadikan Momen, Ceritakan Kisahmu dalam Bahasa Inggris.",
        "info": ["21 Tahun", "Mahasiswa Teknik Informatika", "Universitas Kebangsaan Republik Indonesia"],
        "quote": "Setiap momen punya cerita, dan setiap cerita adalah bagian dari perjalananku.",
    },
    "about": {
        "title": "Tentang Aku",
        "text": (
            "Halo! Namaku Tio Kati Nuansya. Aku berusia 21 tahun dan berasal dari Kabupaten "
            "Cianjur, Jawa Barat. Aku mahasiswa Teknik Informatika di Universitas Kebangsaan "
            "Republik Indonesia (UKRI) di Bandung. Aku menikmati pemrograman, mempelajari "
            "teknologi, dan mengikuti kegiatan organisasi. Di waktu luang, aku suka "
            "mendengarkan musik, menonton film, dan tidur. Musisi favoritku adalah The Jansen dan Bernadya."
        ),
        "facts_title": "Sekilas",
        "facts": [
            ("Nama", "Tio Kati Nuansya"),
            ("Usia", "21 tahun"),
            ("Asal", "Kabupaten Cianjur, Jawa Barat"),
            ("Studi", "Teknik Informatika, UKRI Bandung"),
            ("Musisi favorit", "The Jansen, Bernadya"),
        ],
    },
    "routine": {
        "title": "Rutinitas Harianku",
        "grammar": "Simple Present Tense",
        "items": [
            {"title": "Pergi ke Kampus", "caption": "Aku pergi ke kampus untuk mengikuti kuliah dan belajar hal-hal baru."},
            {"title": "Belajar dan Mengerjakan Tugas", "caption": "Aku belajar pemrograman dan mengerjakan tugas kuliahku."},
            {"title": "Beristirahat", "caption": "Setelah hari yang sibuk, aku meluangkan waktu untuk bersantai dan tidur."},
        ],
    },
    "hobbies": {
        "title": "Hobi dan Minatku",
        "grammar": "Simple Present Tense",
        "paragraphs": [
            "Aku punya beberapa hobi dan minat yang membuat hidupku lebih menyenangkan. Aku menikmati pemrograman karena aku suka menciptakan sesuatu dengan teknologi dan memecahkan masalah. Aku juga tertarik mempelajari hal-hal baru tentang komputer dan pengembangan perangkat lunak.",
            "Selain teknologi, aku menikmati kegiatan organisasi karena aku bisa bertemu orang baru, berbagi ide, dan mendapat pengalaman. Aku juga suka mendengarkan musik, menonton film, dan tidur setiap kali punya waktu luang.",
        ],
        "categories": ["Pemrograman & Teknologi", "Organisasi", "Musik", "Film", "Waktu Santai"],
    },
    "today": {
        "title": "Apa yang Terjadi Hari Ini?",
        "grammar": "Present Continuous Tense",
        "items": [
            {"title": "Belajar Pemrograman", "caption": "Aku sedang menulis kode dan mempelajari teknik pemrograman baru."},
            {"title": "Mengerjakan Tugas", "caption": "Aku sedang mengerjakan tugas kuliahku menggunakan laptop."},
            {"title": "Mengikuti Kegiatan Organisasi", "caption": "Aku sedang berdiskusi dan berbagi ide dengan teman-temanku dalam rapat organisasi."},
        ],
    },
    "place": {
        "title": "Tempat Favoritku",
        "items": [
            {
                "title": "Kampusku",
                "text": "Tempat favoritku adalah kampus dan tempat-tempat yang dikelilingi alam. Kampusku istimewa bagiku karena aku belajar, bertemu teman, dan mendapat pengalaman baru di sana. Kampus adalah tempat aku mempelajari banyak hal tentang teknologi dan membangun masa depanku.",
            },
            {
                "title": "Tempat Hijau dan Tenang",
                "text": "Aku juga menyukai tempat yang hijau dan tenang dengan udara segar. Tempat-tempat ini membuatku merasa rileks dan nyaman. Aku senang menghabiskan waktu di sana karena membantu menyegarkan pikiranku setelah hari yang sibuk.",
            },
        ],
    },
    "story": {
        "title": "Kisah Foto: Sehari dalam Hidupku",
        "steps": [
            {"link": "First", "title": "Memulai Hariku"},
            {"link": "Then", "title": "Pergi ke Kampus"},
            {"link": "After That", "title": "Belajar"},
            {"link": "Next", "title": "Kegiatan Organisasi"},
            {"link": "Finally", "title": "Waktunya Istirahat"},
        ],
        "text": (
            "Kehidupan sehari-hariku sebagai mahasiswa penuh dengan berbagai kegiatan. "
            "Pertama, aku mempersiapkan diri untuk kuliah dan bersiap menyambut hari. "
            "Lalu, aku pergi ke kampus dan mengikuti perkuliahan. Di sana aku belajar hal "
            "baru dan bertemu teman-temanku. Setelah itu, aku mengerjakan tugas dan berlatih "
            "pemrograman. Kadang-kadang, aku sedang mengikuti kegiatan organisasi bersama "
            "teman-temanku. Di waktu luang, aku menikmati musik atau menonton film. "
            "Terakhir, aku beristirahat dan tidur untuk bersiap menghadapi hari berikutnya."
        ),
    },
    "reading": {
        "title": "Pojok Baca",
        "chapter": "Bab 2 — The Pool of Tears (Kolam Air Mata)",
        "part1": "BAGIAN 1 — SEBELUM MEMBACA",
        "keywords_label": "Kata Kunci",
        "prediction_label": "Prediksiku",
        "prediction": "Berdasarkan judul bab, kupikir Alice akan mengalami sesuatu yang tidak biasa yang berkaitan dengan air mata dan air. Aku juga memprediksi Alice akan bertemu tokoh lain saat menjelajahi Wonderland. Bab ini mungkin menceritakan kisah petualangannya yang menarik.",
        "excerpt_label": "Kutipan dari Novel (100–150 kata)",
        "excerpt_help": "Tempel teks ASLI dari novel di sini (100–150 kata). Jangan menulis atau mengarang kutipan.",
        "part2": "BAGIAN 2 — SETELAH MEMBACA",
        "main_idea_label": "Ide Pokok",
        "main_idea": "Bab ini menceritakan Alice yang tumbuh sangat besar lalu jatuh ke kolam air matanya sendiri. Dalam petualangan ini, dia bertemu seekor Tikus.",
        "events_label": "Dua Kejadian Penting",
        "events": [
            "Alice minum dari sebuah botol dan tumbuh sangat besar.",
            "Alice jatuh ke kolam air mata dan bertemu seekor Tikus saat berenang.",
        ],
        "eval_label": "Evaluasi Prediksi",
        "evaluation": "Ya, prediksiku sebagian benar. Alice mengalami petualangan tidak biasa yang berkaitan dengan air mata dan air. Dia juga bertemu seekor Tikus di kolam.",
    },
    "reflection": {
        "title": "Refleksiku",
        "text": (
            "Membuat majalah digital ini adalah pengalaman yang menarik bagiku. Aku senang "
            "membagikan cerita pribadi, hobi, dan kegiatan sehari-hariku lewat foto dan "
            "tulisan. Proyek ini membantuku melatih kemampuan menulis dan kosakata Bahasa "
            "Inggris. Aku juga belajar menggunakan Simple Present dan Present Continuous "
            "Tense dengan benar. Kadang-kadang aku kesulitan menyusun kalimat dalam Bahasa "
            "Inggris, tetapi aku berusaha meningkatkan kemampuanku. Lewat proyek ini, aku "
            "menjadi lebih percaya diri dalam mengungkapkan ide dalam Bahasa Inggris. "
            "Secara keseluruhan, proyek ini adalah pengalaman belajar yang berharga bagiku."
        ),
    },
}


def _merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def get_text(lang: str = "en") -> dict:
    """Return the full text tree for 'en' or 'id' (missing id keys fall back to en)."""
    if lang == "id":
        return _merge(CONTENT, ID)
    return copy.deepcopy(CONTENT)

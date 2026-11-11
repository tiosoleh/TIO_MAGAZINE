"""English content of TIO MAGAZINE.

English is the primary language: it is what the website shows by default
and it is the ONLY language used inside the exported PDF.
Indonesian translations live in utils/translations.py.
"""

CONTENT = {
    "ui": {
        "brand": "TIO Magazine",
        "nav_stories": "Stories",
        "nav_photography": "Photography",
        "nav_about": "About",
        "nav_pdf": "PDF",
        "scroll": "SCROLL",
        "page": "PAGE",
        "grammar": "Grammar focus",
        "lang_toggle": "Bahasa Indonesia",
        "music": "♪ Music",
        "music_help": "Upload an MP3 or WAV file to play background music. Use the player to play, pause and change the volume.",
        "music_upload": "Background music (MP3 / WAV)",
        "music_none": "No music uploaded yet.",
        "photo_manage": "📷  Manage photos for this page",
        "photo_upload": "Upload",
        "photo_current": "Current photo",
        "photo_remove": "Remove photo",
        "photo_empty": "Your photo here",
        "photo_error": "This image could not be read. Please use a JPG, PNG or WEBP file.",
        "dl_eyebrow": "FINAL STEP",
        "dl_title": "Take the magazine with you",
        "dl_text": "Download your 9-page A4 magazine as a PDF. Every uploaded photo and your edited Reading Corner answers are included. The PDF is always written in English.",
        "dl_button": "DOWNLOAD MY MAGAZINE PDF",
        "dl_error": "The PDF could not be created: ",
        "footer_tag": "Capture the Moments, Tell Your Story in English.",
        "footer_credit": "English Midterm Project (UTS) · Informatics Engineering · UKRI Bandung",
        "footer_built": "Built with Python & Streamlit",
        "words": "words",
        "wc_ok": "within the 100–150 word target",
        "wc_low": "too short — aim for 100–150 words",
        "wc_high": "too long — aim for 100–150 words",
        "editable": "Editable — your changes appear in the PDF.",
    },
    "cover": {
        "title": "MY LIFE, MY STORY",
        "tagline": "Capture the Moments, Tell Your Story in English.",
        "author": "Tio Kati Nuansya",
        "info": [
            "21 Years Old",
            "Informatics Engineering Student",
            "Universitas Kebangsaan Republik Indonesia",
        ],
        "quote": "Every moment has a story, and every story is part of my journey.",
    },
    "about": {
        "title": "All About Me",
        "text": (
            "Hello! My name is Tio Kati Nuansya. I am 21 years old, and I come from "
            "Cianjur Regency, West Java. I am an Informatics Engineering student at "
            "Universitas Kebangsaan Republik Indonesia (UKRI) in Bandung. I enjoy "
            "programming, learning about technology, and participating in organizational "
            "activities. In my free time, I love listening to music, watching movies, "
            "and sleeping. My favorite music artists are The Jansen and Bernadya."
        ),
        "facts_title": "At a Glance",
        "facts": [
            ("Name", "Tio Kati Nuansya"),
            ("Age", "21 years old"),
            ("From", "Cianjur Regency, West Java"),
            ("Study", "Informatics Engineering, UKRI Bandung"),
            ("Favorite artists", "The Jansen, Bernadya"),
        ],
    },
    "routine": {
        "title": "My Daily Routine",
        "grammar": "Simple Present Tense",
        "items": [
            {"title": "Going to Campus", "caption": "I go to campus to attend my classes and learn new things."},
            {"title": "Studying and Doing Assignments", "caption": "I study programming and work on my college assignments."},
            {"title": "Taking a Rest", "caption": "After a busy day, I take some time to relax and sleep."},
        ],
    },
    "hobbies": {
        "title": "My Hobbies and Interests",
        "grammar": "Simple Present Tense",
        "paragraphs": [
            "I have several hobbies and interests that make my life more enjoyable. I enjoy programming because I love creating things with technology and solving problems. I am also interested in learning new things about computers and software development.",
            "Besides technology, I enjoy participating in organizational activities because I can meet new people, share ideas, and gain experience. I also love listening to music, watching movies, and sleeping whenever I have free time.",
        ],
        "categories": ["Programming & Technology", "Organization", "Music", "Movies", "Relaxing Time"],
    },
    "today": {
        "title": "What's Happening Today?",
        "grammar": "Present Continuous Tense",
        "items": [
            {"title": "Studying Programming", "caption": "I am writing code and learning new programming techniques."},
            {"title": "Working on Assignments", "caption": "I am working on my college assignments using my laptop."},
            {"title": "Participating in Organizational Activities", "caption": "I am discussing and sharing ideas with my friends in an organizational meeting."},
        ],
    },
    "place": {
        "title": "My Favorite Place",
        "items": [
            {
                "title": "My Campus",
                "text": "My favorite places are my campus and places surrounded by nature. My campus is special to me because I study, meet my friends, and gain new experiences there. It is a place where I learn many things about technology and build my future.",
            },
            {
                "title": "Green and Peaceful Places",
                "text": "I also love green and peaceful places with fresh air. These places make me feel relaxed and comfortable. I enjoy spending time there because they help me refresh my mind after a busy day.",
            },
        ],
    },
    "story": {
        "title": "Photo Story: A Day in My Life",
        "steps": [
            {"link": "First", "title": "Starting My Day"},
            {"link": "Then", "title": "Going to Campus"},
            {"link": "After That", "title": "Studying"},
            {"link": "Next", "title": "Organizational Activities"},
            {"link": "Finally", "title": "Time to Rest"},
        ],
        "text": (
            "My daily life as a university student is full of different activities. "
            "First, I prepare myself for college and get ready for the day. Then, I go to "
            "campus and attend my classes. I learn new things and meet my friends there. "
            "After that, I work on my assignments and practice programming. Sometimes, I am "
            "participating in organizational activities with my friends. In my free time, I "
            "enjoy listening to music or watching movies. Finally, I take a rest and sleep "
            "to prepare for another day."
        ),
    },
    "reading": {
        "title": "Reading Corner",
        "novel": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "chapter": "Chapter 2 — The Pool of Tears",
        "part1": "PART 1 — BEFORE READING",
        "keywords_label": "Keywords",
        "keywords": ["Alice", "Tears", "Mouse"],
        "prediction_label": "My Prediction",
        "prediction": "Based on the chapter title, I think Alice will experience something unusual involving tears and water. I also predict that Alice will meet another character while exploring Wonderland. The chapter may tell an interesting story about her adventure.",
        "excerpt_label": "From the Novel (100–150 words)",
        "excerpt_help": "Paste the ORIGINAL text from the novel here (100–150 words). Do not write or invent quotes.",
        "excerpt_empty": "[Paste the original excerpt from the novel here: 100 to 150 words.]",
        "part2": "PART 2 — AFTER READING",
        "main_idea_label": "Main Idea",
        "main_idea": "The chapter tells the story of Alice growing very large and then falling into a pool of her own tears. During this adventure, she meets a Mouse.",
        "events_label": "Two Important Events",
        "events": [
            "Alice drinks from a bottle and grows very large.",
            "Alice falls into a pool of tears and meets a Mouse while swimming.",
        ],
        "eval_label": "Prediction Evaluation",
        "evaluation": "Yes, my predictions were partly correct. Alice experiences an unusual adventure involving tears and water. She also meets a Mouse in the pool.",
    },
    "reflection": {
        "title": "My Reflection",
        "text": (
            "Creating this digital magazine is an interesting experience for me. I enjoy "
            "sharing my personal stories, hobbies, and daily activities through photographs "
            "and writing. This project helps me practice my English writing and vocabulary. "
            "I also learn how to use Simple Present and Present Continuous Tenses correctly. "
            "Sometimes, I find it difficult to arrange sentences in English, but I try to "
            "improve my skills. Through this project, I become more confident in expressing "
            "my ideas in English. Overall, this project is a valuable learning experience for me."
        ),
    },
}

from flask import Flask, request, render_template_string
import os, uuid, time, sqlite3
from werkzeug.utils import secure_filename
from PIL import Image
import imagehash

#app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_NAME = "images.db"
THRESHOLD = 10

# =========================
# 🗄 DATABASE SETUP
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        filepath TEXT,
        phash TEXT,
        uploaded_at TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# 🔍 VALIDATION
# =========================
def is_valid_file(file):
    if not file or file.filename == "":
        return False

    ext = file.filename.rsplit(".", 1)[-1].lower()
    return ext in {"png", "jpg", "jpeg"}

# =========================
# 💾 SAVE IMAGE
# =========================
def save_image(file):
    filename = secure_filename(file.filename)
    unique_name = f"{int(time.time())}_{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)

    file.save(file_path)

    try:
        img = Image.open(file_path)
        img.verify()
    except:
        os.remove(file_path)
        return None

    return file_path

# =========================
# 🔐 SECURITY MODULE (DB + pHash)
# =========================
def security_module(file_path):
    image = Image.open(file_path)
    new_hash = str(imagehash.phash(image))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT phash FROM images")
    rows = cursor.fetchall()

    for (old_hash,) in rows:
        diff = imagehash.hex_to_hash(old_hash) - imagehash.hex_to_hash(new_hash)
        if diff < THRESHOLD:
            conn.close()
            return f"🚫 BLOCKED (Similar Image Found, diff={diff})"

    # Store if safe
    cursor.execute("""
    INSERT INTO images (filename, filepath, phash, uploaded_at)
    VALUES (?, ?, ?, ?)
    """, (
        os.path.basename(file_path),
        file_path,
        new_hash,
        time.strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return "✅ SAFE (Stored in database)"


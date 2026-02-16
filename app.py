import os
import sqlite3
from flask import Flask, render_template, request, redirect, send_from_directory

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB_PATH = os.path.join(BASE_DIR, "products.db")


# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            model TEXT
        )
    """)
    conn.close()

init_db()


# ---------- HOME PAGE ----------
@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)


# ---------- ADMIN PAGE ----------
@app.route("/admin")
def admin():
    return render_template("admin.html")


# ---------- UPLOAD MODEL ----------
@app.route("/upload-model", methods=["POST"])
def upload_model():
    name = request.form.get("name")
    file = request.files.get("file")

    if not file:
        return "No file uploaded"

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO products(name, model) VALUES (?, ?)",
        (name, filename)
    )
    conn.commit()
    conn.close()

    return redirect("/")


# ---------- SERVE UPLOADED FILES ----------
@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

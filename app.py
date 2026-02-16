from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("products.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            model TEXT
        )
    """)
    conn.close()

init_db()


# ---------- HOME ----------
@app.route("/")
def home():
    conn = sqlite3.connect("products.db")
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("index.html", products=products)


# ---------- ADMIN PAGE ----------
@app.route("/admin")
def admin():
    return render_template("admin.html")


# ---------- MODEL UPLOAD ----------
@app.route("/upload-model", methods=["POST"])
def upload_model():
    name = request.form["name"]
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    conn = sqlite3.connect("products.db")
    conn.execute(
        "INSERT INTO products(name, model) VALUES (?, ?)",
        (name, file.filename)
    )
    conn.commit()
    conn.close()

    return redirect("/")


# ---------- SERVE MODEL FILES ----------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
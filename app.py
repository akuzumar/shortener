from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "links.db"

# bikin database & tabel (kalau belum ada)
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS links (
            code TEXT PRIMARY KEY,
            url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        code = request.form["code"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # cek apakah kode sudah dipakai
        cur.execute("SELECT code FROM links WHERE code = ?", (code,))
        if cur.fetchone():
            conn.close()
            return "Kode sudah dipakai, coba yang lain"

        cur.execute(
            "INSERT INTO links (code, url) VALUES (?, ?)",
            (code, url)
        )
        conn.commit()
        conn.close()

        return f"""
        <p>Link pendek kamu:</p>
        <a href="/{code}">
        http://127.0.0.1:5000/{code}
        </a>
        """

    return """
    <h2>URL Shortener (SQLite)</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Masukkan URL panjang" required>
        <br><br>
        <input type="text" name="code" placeholder="Kode pendek (bebas)" required>
        <br><br>
        <button type="submit">Shorten</button>
    </form>
    """

@app.route("/<code>")
def go(code):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT url FROM links WHERE code = ?", (code,))
    result = cur.fetchone()
    conn.close()

    if result:
        return redirect(result[0])

    return "Link tidak ditemukan"

app.run(host="0.0.0.0", port=10000)

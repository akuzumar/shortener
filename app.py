from flask import Flask, render_template, request, redirect
import json, string, random, os, re

app = Flask(__name__)
DATA_FILE = "urls.json"

def load_urls():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_urls(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def valid_alias(alias):
    return re.match("^[a-zA-Z0-9_-]+$", alias)

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        long_url = request.form["url"]
        custom = request.form.get("custom")

        data = load_urls()

        if custom:
            if not valid_alias(custom):
                error = "Alias hanya boleh huruf, angka, - dan _"
            elif custom in data:
                error = "Alias sudah dipakai"
            else:
                data[custom] = long_url
                save_urls(data)
                short_url = request.host_url + custom
        else:
            code = generate_code()
            data[code] = long_url
            save_urls(data)
            short_url = request.host_url + code

    return render_template("index.html", short_url=short_url, error=error)

@app.route("/<code>")
def redirect_url(code):
    data = load_urls()
    if code in data:
        return redirect(data[code])
    return "URL tidak ditemukan", 404

if __name__ == "__main__":
    app.run(debug=True)

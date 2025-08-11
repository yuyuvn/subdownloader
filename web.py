#!/usr/bin/env python3
import os
from flask import Flask, request, render_template_string, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)

LANG_CODES = [
    ("eng", "English"),
    ("spa", "Spanish"),
    ("fre", "French"),
    ("ger", "German"),
    ("ita", "Italian"),
    ("por", "Portuguese"),
    ("rus", "Russian"),
    ("jpn", "Japanese"),
    ("chi", "Chinese"),
    ("vie", "Vietnames"),
    # Add more as needed
]

def get_default_lang():
    return os.environ.get("DEFAULT_LANG", "eng")

def get_base_path():
    return os.environ.get("BASE_PATH", "/data")

FORM_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Subtitle Downloader</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background: #f7f7fa;
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 420px;
      margin: 60px auto;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
      padding: 32px 28px 24px 28px;
    }
    h1 {
      text-align: center;
      color: #2d3748;
      margin-bottom: 28px;
      font-size: 2rem;
      letter-spacing: 0.01em;
    }
    label {
      display: block;
      margin-bottom: 8px;
      color: #4a5568;
      font-weight: 500;
    }
    input[type="text"], select {
      width: 100%;
      padding: 10px 12px;
      margin-bottom: 20px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 1rem;
      background: #f9fafb;
      transition: border 0.2s;
    }
    input[type="text"]:focus, select:focus {
      border-color: #3182ce;
      outline: none;
      background: #fff;
    }
    .submit-btn {
      width: 100%;
      padding: 12px 0;
      background: linear-gradient(90deg, #3182ce 0%, #63b3ed 100%);
      color: #fff;
      border: none;
      border-radius: 6px;
      font-size: 1.1rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(49,130,206,0.08);
      transition: background 0.2s;
    }
    .submit-btn:hover {
      background: linear-gradient(90deg, #2563eb 0%, #4299e1 100%);
    }
    .note {
      font-size: 0.95em;
      color: #718096;
      margin-top: 8px;
      margin-bottom: 18px;
      text-align: center;
    }
    .footer {
      text-align: center;
      color: #a0aec0;
      font-size: 0.9em;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="container">
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <div>
          {% for category, message in messages %}
            <div class="flash flash-{{ category }}">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}
    <h1>🎬 Subtitle Downloader</h1>
    <form method="post" action="{{ url_for('submit') }}">
      <label for="filename">Video File Name (relative to base folder):</label>
      <input type="text" id="filename" name="filename" placeholder="e.g. movies/yourfile.mkv" required autocomplete="off">

      <label for="lang">Subtitle Language:</label>
      <select id="lang" name="lang">
        {% for code, name in lang_codes %}
          <option value="{{ code }}" {% if code == default_lang %}selected{% endif %}>{{ name }} ({{ code }})</option>
        {% endfor %}
      </select>

      <div class="note">
        <span>Base folder: <code>{{ base_path }}</code></span>
      </div>

      <button class="submit-btn" type="submit">⬇️ Download &amp; Sync Subtitle</button>
    </form>
  </div>
  <div class="footer">
    &copy; {{ 2025 }} Pepperoni AI
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    default_lang = get_default_lang()
    return render_template_string(FORM_HTML, lang_codes=LANG_CODES, default_lang=default_lang, base_path=get_base_path())

@app.route("/submit", methods=["POST"])
def submit():
    filename = request.form.get("filename")
    base_path = get_base_path()
    lang = request.form.get("lang", get_default_lang())
    if not filename:
        return "Filename is required", 400
    # Call subdownloader.py with filename and lang
    import subprocess
    try:
        print(f"Call python subdownloader.py \"{base_path}/{filename}\" \"{lang}\"")
        result = subprocess.run(
            ["python", "subdownloader.py", f"{base_path}/{filename}", lang],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
        flash("Subtitle downloaded and synced successfully!", "success")
        return redirect(url_for("index"))
    except subprocess.CalledProcessError as e:
        flash(f"Error: {e.stderr or str(e)}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    bind = os.environ.get("BIND", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    print(f"Bind to http://{bind}:{port}/")
    app.secret_key = os.environ.get("SECRET_KEY", "random_secret_key")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.environ.get("SESSION_FILE_DIR", "/tmp/sessions")
    app.run(debug=True, port=port, host=bind)

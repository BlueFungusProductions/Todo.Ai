from flask import Flask, request, jsonify, send_from_directory, render_template
import sys
from datetime import datetime
import os
from server.journal import chat

app = Flask(__name__, template_folder="uitemplates")
app.add_url_rule("/journal", view_func=chat, methods=["POST"])


@app.route("/")
def index():
    shortcut_dir = "Siri"
    shortcut_files = [f for f in os.listdir(shortcut_dir) if f.endswith(".shortcut")]
    return render_template("index.html", shortcut_files=shortcut_files)


@app.route("/siri/<path:filename>")
def serve_shortcut(filename):
    return send_from_directory("Siri", filename)


def run_server(debug=False):
    print(f"🌐 Starting web server at http://localhost:5000 (debug={debug})")
    app.run(host="0.0.0.0", port=5000, debug=debug)

if __name__ == "__main__":  
    run_server(debug=True)

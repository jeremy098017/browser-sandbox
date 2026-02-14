from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def home():
    return "Browser sandbox running!"

@app.route("/browse", methods=["POST"])
def browse():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing url"}), 400

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        content = page.content()
        title = page.title()

        browser.close()

    return jsonify({
        "title": title,
        "html": content
    })

app.run(host="0.0.0.0", port=8080)

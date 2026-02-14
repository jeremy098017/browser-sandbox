from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# root health check
@app.route("/")
def root():
    return "browser sandbox running", 200

# explicit health endpoint
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


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

        result = {
            "title": page.title(),
            "html": page.content()
        }

        browser.close()
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

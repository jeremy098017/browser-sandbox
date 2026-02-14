from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/")
def root():
    return "OK", 200

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
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)

        result = {
            "title": page.title(),
            "html": page.content()
        }

        browser.close()
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

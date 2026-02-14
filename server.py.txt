from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

browser = None
page = None

@app.on_event("startup")
def start_browser():
    global browser, page
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox"]
    )
    page = browser.new_page()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/goto")
def goto(url: str):
    page.goto(url)
    return {"status": "ok"}

@app.get("/html")
def html():
    return {"html": page.content()}

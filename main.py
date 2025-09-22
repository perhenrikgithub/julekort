import uuid
import os
import shutil
import sqlite3
from fastapi import FastAPI, Query, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_PATH = "cards.db"
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id TEXT PRIMARY KEY,
                text TEXT,
                image_url TEXT,
                display_on_board INTEGER DEFAULT 0,
                sender TEXT,
                recipient TEXT
            )
        """)
init_db()

@app.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_card(
    request: Request,
    card_image: UploadFile = File(...),
    card_text: str = Form(...),
    sender: str = Form(...),
    recipient: str = Form(...)
):
    # Lagre bilde
    file_location = f"{UPLOAD_DIR}/{card_image.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(card_image.file, f)

    # Opprett ID og lagre til database
    card_id = str(uuid.uuid4())[:8]
    image_url = f"/static/uploads/{card_image.filename}"

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO cards (id, text, image_url, display_on_board, sender, recipient)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (card_id, card_text, image_url, 0, sender, recipient)
        )

    return templates.TemplateResponse("uploaded.html", {
        "request": request,
        "card_id": card_id
    })

@app.get("/envelope/{card_id}", response_class=HTMLResponse)
async def envelope_card(request: Request, card_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT text, image_url FROM cards WHERE id = ?",
            (card_id,)
        ).fetchone()

    if not row:
        return HTMLResponse("<h1>Card not found</h1>", status_code=404)

    card_text, image_url = row
    return templates.TemplateResponse("envelope.html", {
        "request": request,
        "letter_text": card_text,
        "card_image_url": image_url
    })

@app.get("/uploaded", response_class=HTMLResponse)
async def uploaded(request: Request, card_id: str = Query(...)):
    return templates.TemplateResponse("uploaded.html", {
        "request": request,
        "card_id": card_id
    })
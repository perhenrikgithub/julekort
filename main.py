import re
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
templates = Jinja2Templates(directory="templates")

@app.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    # Try to read cookie values (defaults to empty strings if none found)
    prefill_sender = request.cookies.get("sender", "")
    prefill_sender_email = request.cookies.get("sender_email", "")
    prefill_recipient = request.cookies.get("recipient", "")
    card_text = request.cookies.get("card_text", "")

    return templates.TemplateResponse("upload.html", {
        "request": request,
        "prefill_sender": prefill_sender,
        "prefill_sender_email": prefill_sender_email,
        "prefill_recipient": prefill_recipient,
        "card_text": card_text
    })

@app.post("/upload", response_class=HTMLResponse)
async def upload_card(
    request: Request,
    card_image: UploadFile = File(None),
    card_text: str = Form(...),
    sender: str = Form(...),
    sender_email: str = Form(...),
    recipient: str = Form(...),
    display_on_corkboard: str = Form(None)
):
    image_url = request.cookies.get("image_url", "")
    card_id = str(uuid.uuid4())[:8]

    # validate inputs
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    # Validate sender email
    if not re.match(email_pattern, sender_email):
        return HTMLResponse(
            f"<h1>400 Bad Request</h1><p>Ho ho ho! Avsenderens epost '{sender_email}' ser ut til å ikke være gyldig. Sjekk reinsdyrposten!</p>",
            status_code=400
            )

    # Validate recipient email(s)
    if "," in recipient:
        # Split recipients by comma, strip whitespace
        recipients = [r.strip() for r in recipient.split(",") if r.strip()]
    else:
        recipients = [recipient.strip()]

    for rec in recipients:
        if not re.match(email_pattern, rec):
            return HTMLResponse(
                f"<h1>400 Bad Request</h1><p>Uh-oh! Eposten '{rec}' ser ikke ut til å være en gyldig epost. Julenissens nissehjelpere kan ikke levere hit!</p>",
                status_code=400
            )
        
    # validate for 418
    if "kaffe" in sender.lower():
        return HTMLResponse(
            f"<h1>418 I'm a Teapot</h1><p>Kaffe funnet i navnet: {sender.split('kaffe')[0]}<b>kaffe</b>{sender.split('kaffe')[1]}. Julenissen postkasse er en tekanne, ikke en kaffebar.</p>",
            status_code=418
        )
    
    # =============
    # Validate file
    # =============

    # If no file uploaded, check if URL provided
    if not (card_image and card_image.filename) and not image_url:
        print(f"card_image: {card_image} | filename: '{card_image.filename}'")
        print(f"image_url: {image_url}")
        return HTMLResponse(
            f"""
                <h1>400 Bad Request</h1>
                <p>Ingen bilde ble lastet opp! Julenissen trenger et bilde for å levere kortet.</p>
                <p>card_image: {card_image} | {card_image.filename} | card_image_url: {image_url}</p>
                """,
            status_code=400
        )
    
    if card_image and card_image.filename:
        # filetype
        if card_image.content_type not in ["image/jpeg", "image/png"]:
            return HTMLResponse(f"<h1>415 Unsupported Media Type</h1><p>Julenissens lager kan kun lagre bilder i JPEG eller PNG format. Din filtype er {card_image.content_type}</p>", status_code=415)

        # Validate file size (1MB max)
        card_image.file.seek(0, os.SEEK_END)
        file_size = card_image.file.tell()
        card_image.file.seek(0)
        if file_size > 1 * 1024 * 1024:
            return HTMLResponse(
                "<h1>413 Payload Too Large</h1><p>Å nei! Filen er for stor for julenissens slede! (maks 1MB).</p>",
                status_code=413
            )

        # Validate filename exists
        if not card_image.filename:
            return HTMLResponse(
                "<h1>400 Bad Request</h1><p>Ingen bilde ble lastet opp! Julenissen trenger et bilde for å levere kortet.</p>",
                status_code=400
            )
        
        # Generate unique filename
        file_ext = card_image.filename.split(".")[-1]
        image_filename = f"{card_id}.{file_ext}"
        image_url = f"/static/uploads/{image_filename}"
        file_location = os.path.join(UPLOAD_DIR, image_filename)

        # Save image
        with open(file_location, "wb") as f:
            shutil.copyfileobj(card_image.file, f)

    elif image_url:
        card_id = str(uuid.uuid4())[:8]
        image_url = image_url

    # Checkbox value as boolean
    display = 1 if display_on_corkboard == "on" else 0

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT INTO cards
                (id, text, image_url, display_on_board, sender, sender_email, recipient)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (card_id, card_text, image_url, display, sender, sender_email, recipient)
        )

    response = templates.TemplateResponse("uploaded.html", {
        "request": request,
        "card_id": card_id
    })

    response.set_cookie(key="image_url", value=image_url)
    response.set_cookie(key="sender", value=sender)
    response.set_cookie(key="sender_email", value=sender_email)
    response.set_cookie(key="recipient", value=recipient)
    response.set_cookie(key="card_text", value=card_text.encode("latin-1", "ignore").decode("latin-1"))

    return response

@app.get("/card/{card_id}", response_class=HTMLResponse)
async def envelope_card(request: Request, card_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT text, image_url FROM cards WHERE id = ?",
            (card_id,)
        ).fetchone()

    if not row:
        return HTMLResponse(
            f"<h1>404 Not found</h1><p>Nissens verksted finner ikke julekortet med ID {card_id} </p>",
            status_code=404
        )

    card_text, image_url = row

    return templates.TemplateResponse(
        "envelope.html", 
        {
            "request": request,
            "letter_text": card_text,
            "card_image_url": image_url
        }
    )

@app.get("/uploaded", response_class=HTMLResponse)
async def uploaded(request: Request, card_id: str = Query(...)):
    return templates.TemplateResponse("uploaded.html", {
        "request": request,
        "card_id": card_id
    })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/corkboard", response_class=HTMLResponse)
async def view_corkboard(request: Request):
    with sqlite3.connect(DB_PATH) as conn:
        image_urls = conn.execute(
            "SELECT DISTINCT image_url FROM cards WHERE display_on_board = 1 ORDER BY RANDOM()"
        ).fetchall()

    return templates.TemplateResponse(
        "corkboard.html",
        {"request": request, "images": [url[0] for url in image_urls]}
    )

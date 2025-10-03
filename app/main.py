from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import os, smtplib
from email.message import EmailMessage
from typing import List

app = FastAPI(title="fake-api", version="0.1.0")

class EmailPayload(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str

ITEMS = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]

@app.get("/health")
def health():
    return {"ok": True, "ts": "2025-10-03T11:17:54.536463+00:00"}

@app.get("/items")
def get_items():
    return {"items": ITEMS}

def _send_email_sync(msg: EmailPayload):
    host = os.getenv("MAIL_HOST")
    port = int(os.getenv("MAIL_PORT", "1025"))
    user = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASS")
    dry = os.getenv("DRY_RUN", "1") == "1"

    if dry or not host:
        # Simulación sin SMTP real
        print(f"[DRY_RUN] Enviando a {msg.to}: {msg.subject}")
        return

    m = EmailMessage()
    m["From"] = os.getenv("MAIL_FROM", "noreply@example.com")
    m["To"] = ", ".join(msg.to)
    m["Subject"] = msg.subject
    m.set_content(msg.body)

    with smtplib.SMTP(host, port) as s:
        if user and password:
            s.starttls()
            s.login(user, password)
        s.send_message(m)

@app.post("/send-email")
def send_email(payload: EmailPayload, bg: BackgroundTasks):
    bg.add_task(_send_email_sync, payload)
    return {"queued": True, "to": payload.to}

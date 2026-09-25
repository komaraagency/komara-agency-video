"""
Komara Agency — Application web déployable sur Railway.

- GET /        : page vitrine (scénario vidéo publicitaire)
- GET /health  : vérification de santé pour Railway
- Bot Telegram : démarré automatiquement si TELEGRAM_BOT_TOKEN est défini
"""

import logging
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from telegram_bot import start_polling

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Komara Agency")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.on_event("startup")
async def startup():
    start_polling()


@app.get("/")
async def home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok", "app": "komara-agency"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI(title="RisparmioSmart Automatico")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HERE = os.path.dirname(__file__)
OFFERS_FILE = os.path.join(HERE, "offers.json")

@app.get("/offers")
def list_offers():
    if os.path.exists(OFFERS_FILE):
        with open(OFFERS_FILE, "r", encoding="utf-8") as f:
            offers = json.load(f)
    else:
        offers = []
    return {"offers": offers}

@app.get("/health")
def health():
    return {"status": "ok"}

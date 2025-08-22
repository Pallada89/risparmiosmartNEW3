import os, json, re
from PIL import Image
import pytesseract

HERE = os.path.dirname(__file__)
FLYERS_DIR = os.path.join(HERE, "flyers")
OUTPUT_FILE = os.path.join(HERE, "offers.json")

os.makedirs(FLYERS_DIR, exist_ok=True)

def extract_offers(text):
    # Pattern base: 'Nome Prodotto 500g 0,99 €' o 'Nome Prodotto 0,99 €'
    pattern = r"([A-Za-zÀ-ÿ'\-\s]{3,})\s+(\d+[gGmMlLkK]?(?:\s?x\s?\d+)?)?\s*(\d+,\d{2})\s?€"
    matches = re.findall(pattern, text)
    offers = []
    for product, quantity, price in matches:
        offers.append({
            "product": product.strip(),
            "quantity": (quantity or "").strip(),
            "price": price
        })
    return offers

def process_flyers():
    all_offers = []
    for fname in os.listdir(FLYERS_DIR):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        path = os.path.join(FLYERS_DIR, fname)
        try:
            img = Image.open(path)
            text = pytesseract.image_to_string(img, lang="ita")
        except Exception as e:
            print(f"[WARN] errore OCR {fname}: {e}")
            continue
        offers = extract_offers(text)
        for o in offers:
            o["file"] = fname
            all_offers.append(o)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_offers, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Estrazione completata: {len(all_offers)} offerte salvate in {OUTPUT_FILE}")

if __name__ == "__main__":
    process_flyers()

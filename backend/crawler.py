# Esempio dimostrativo: adattare lo scraping a ciascun sito rispettando robots.txt e Termini d'Uso
import requests, os
from bs4 import BeautifulSoup

BASE_DIR = os.path.join(os.path.dirname(__file__), "flyers")
os.makedirs(BASE_DIR, exist_ok=True)

SUPERMARKETS = {
    "Esselunga": "https://www.esserlungo.example/volantini",  # placeholder
    "Conad": "https://www.conad.example/volantini"             # placeholder
}

def absolute(url, src):
    if src.startswith("http"):
        return src
    if src.startswith("/"):
        return url.rstrip("/") + src
    return url.rstrip("/") + "/" + src

def download_flyers():
    for name, url in SUPERMARKETS.items():
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
        except Exception as e:
            print(f"[WARN] {name}: impossibile scaricare pagina: {e}")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        imgs = soup.find_all("img")
        count = 0
        for i, img in enumerate(imgs):
            src = img.get("src") or img.get("data-src") or ""
            if not src:
                continue
            full = absolute(url, src)
            try:
                resp = requests.get(full, timeout=20)
                if resp.status_code != 200 or not resp.content:
                    continue
                filename = os.path.join(BASE_DIR, f"{name}_{i}.jpg")
                with open(filename, "wb") as f:
                    f.write(resp.content)
                count += 1
            except Exception:
                continue
        print(f"[INFO] {name}: scaricate {count} immagini candidate volantino")

if __name__ == "__main__":
    download_flyers()

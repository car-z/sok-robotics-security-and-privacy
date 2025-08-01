import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import time
import os

# ------------------ CONFIG ------------------
INPUT_CSV = "scraped_data/filtered.csv" 
OUTPUT_DIR = "abstract_batches"
CHUNK_SIZE = 1000
SLEEP_TIME = 1

# HEADER
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://dl.acm.org/",
    "DNT": "1",  # Do Not Track Request Header
    "Connection": "keep-alive",
}

# ---------------- HELPERS --------------------
def is_acm(url):
    if pd.isna(url) or "10." not in str(url):
        return False
    return True

def is_usenix(url):
    if pd.isna(url) or "usenix.org" not in str(url):
        return False
    return True

def extract_doi(url):
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", str(url), flags=re.IGNORECASE)
    return match.group(0)

def get_acm_abstract(doi):
    url = f"https://dl.acm.org/doi/abs/{doi}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            print("request went through")
            soup = BeautifulSoup(r.text, "html.parser")
            abstract_section = soup.select_one('#abstract div[role="paragraph"]')
            if abstract_section:
                print("found abstract")
                return abstract_section.get_text(strip=True)
    except Exception as e:
        print(f"Error scraping DOI: {e}")
    print(r.status_code)
    return None

def get_usenix_abstract(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            abstract_section = soup.select_one(
                'div.field.field-name-field-paper-description.field-type-text-long.field-label-above '
                'div.field-items div.field-item'
            )
            if abstract_section:
                return abstract_section.get_text(strip=True)
    except Exception as e:
        print(f"Error scraping Usenix: {e}")
    return None

# ---------- PROCESSING ---------------------
df = pd.read_csv(INPUT_CSV)
total_rows = len(df)

for start in range(0, total_rows, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, total_rows)
    batch_df = df.iloc[start:end].copy()
    abstracts = []

    print(f"\n🔄 Processing rows {start} to {end - 1}")

    for idx, row in tqdm(df.iterrows(), total=len(batch_df), desc=f"Batch {(start // CHUNK_SIZE) + 1}"):
        url = row.get("ee","")
        abstract = None

        if is_acm(url):
            abstracts.append(abstract)
            doi = extract_doi(url)
            try:
                abstract = get_acm_abstract(doi)
            except Exception as e:
                print(f"Error scraping abstract from ACM: {e}")
        elif is_usenix(url):
            try:
                abstract = get_usenix_abstract(url)     
            except Exception as e:
                print(f"Error scraping abstact from Usenix: {e}")           

        abstracts.append(abstract)
        time.sleep(SLEEP_TIME)

    df['abstract'] = abstracts

    batch_num = (start // CHUNK_SIZE) + 1
    output_file = os.path.join(OUTPUT_DIR, f"abstracts_batch_{batch_num}.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ Saved to {output_file}")

print("\n🎉 Done processing all batches!")
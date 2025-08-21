# STILL DOESN'T WORK

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
from tqdm import tqdm

# --- CONFIG ---
INPUT_CSV = "scraped_data/filtered.csv"
OUTPUT_DIR = "abstract_batches"
CHUNK_SIZE = 5
SLEEP_TIME = 1

# --- Selenium setup ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # remove if you want to see the browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- Helpers ---
def is_acm(url):
    if pd.isna(url) or "10." not in str(url):
        return False
    return True

def is_usenix(url):
    if pd.isna(url) or "usenix.org" not in str(url):
        return False
    return True

def is_ceur(url):
    if pd.isna(url) or "ceur" not in str(url):
        return False
    return True

def extract_doi(url):
    match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", str(url), flags=re.IGNORECASE)
    return match.group(0)

def get_acm_abstract(doi):
    url = f"https://dl.acm.org/doi/abs/{doi}"
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        abstract_section = soup.select_one('#abstract div[role="paragraph"]')
        if abstract_section:
            print("found abstract")
            return abstract_section.get_text(strip=True)                
    except Exception as e:
        print(f"ACM Error for{doi}: {e}")
    return None

def get_usenix_abstract(url):
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        abstract_section = soup.select_one(
            'div.field.field-name-field-paper-description.field-type-text-long.field-label-above '
            'div.field-items div.field-item'
        )
        if abstract_section:
            return abstract_section.get_text(strip=True)
    except Exception as e:
        print(f"Usenix error for{url}: {e}")
    return None

# ---------- PROCESSING ---------------------
df = pd.read_csv(INPUT_CSV)
total_rows = len(df)

for start in range(0, total_rows, CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, total_rows)
    batch_df = df.iloc[start:end].copy()
    abstracts = []

    print(f"\n🔄 Processing rows {start} to {end - 1}")

    for idx, row in tqdm(batch_df.iterrows(), total=len(batch_df), desc=f"Batch {(start // CHUNK_SIZE) + 1}"):
        url = row.get("ee","")
        abstract = None

        if is_acm(url):
            doi = extract_doi(url)
            if doi:
                try:
                    abstract = get_acm_abstract(doi)
                except Exception as e:
                    print(f"Error scraping abstract from Usenix: {e}")
        elif is_usenix(url):
            try:
                abstract = get_usenix_abstract(url)     
            except Exception as e:
                print(f"Error scraping abstact from Usenix: {e}")           

        abstracts.append(abstract)
        time.sleep(SLEEP_TIME)

    batch_df['abstract'] = abstracts

    batch_num = (start // CHUNK_SIZE) + 1
    output_file = os.path.join(OUTPUT_DIR, f"abstracts_batch_{batch_num}.csv")
    batch_df.to_csv(output_file, index=False)
    print(f"✅ Saved to {output_file}")

driver.quit()
print("\n🎉 Done processing all batches!")
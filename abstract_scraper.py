import pandas as pd
import requests
import time
import os
import re
from tqdm import tqdm

# ------------------ CONFIG ------------------
INPUT_CSV = "filtered.csv" 
OUTPUT_DIR = "abstract_batches"
CHUNK_SIZE = 1000
SLEEP_TIME = 1                        # Seconds between requests
USER_AGENT = "Caroline Zhao/caruozhao@gmail.com" 

# ---- HELPER FUNCTION----
def get_abstract(doi):
    headers = {"User-Agent": USER_AGENT}
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            message = data.get("message", {})
            print(message)
            if "abstract" in message:
                abstract = message["abstract"]
                return abstract
            else:
                return None
    except Exception as e:
        print(f"Error for DOI {doi}: {e}")
    return None

def extract_doi(raw_doi):
    if pd.isna(raw_doi):
        return None
    if "10." in raw_doi:
        match = re.search(r"(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", raw_doi, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return None

# ---- MAIN BATCHING LOOP ----
df = pd.read_csv(INPUT_CSV)
total_rows = len(df)

for start in range(0, len(df), CHUNK_SIZE):
    end = min(start + CHUNK_SIZE, total_rows)
    batch_df = df.iloc[start:end].copy()
    abstracts = []

    print(f"\n🔄 Processing rows {start} to {end - 1}")

    for idx, row in tqdm(batch_df.iterrows(), total=len(batch_df), desc=f"Batch {(start // CHUNK_SIZE) + 1}"):
        raw_doi = row.get("ee", None)
        cleaned_doi = extract_doi(raw_doi)

        if cleaned_doi:
            abstract = get_abstract(cleaned_doi)
            abstracts.append(abstract)
            time.sleep(SLEEP_TIME)
        else:
            abstracts.append(None)

    batch_df['abstract'] = abstracts

    batch_num = (start // CHUNK_SIZE) + 1
    output_file = os.path.join(OUTPUT_DIR, f"with_abstracts_batch_{batch_num}.csv")
    batch_df.to_csv(output_file, index=False)
    print(f"✅ Saved batch {batch_num} to {output_file}")

print("\n🎉 Done processing all batches!")
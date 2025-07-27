from lxml import etree
from tqdm import tqdm
import pandas as pd

# --- PARAMETERS ---
TARGET_VENUES = {
    "mobisys", "mobicom", "sensys", "chi", "ubicomp", "imwut", "sigcomm", "nsdi"
}
START_YEAR = 2020 # 2020 - 2025
TYPE = {"inproceedings", "article"} # only pull papers

# --- HELPER FUNCTIONS ---

# checks if entry is a journal article
def is_journal(entry):
    return entry.tag == "article"

# finds and extracts the information for the given tag for the given entry, if it exists
def extract_tag(entry, tag):
    t = entry.find(tag)
    # if the tag and info exist, returns that info
    return t.text.strip() if t is not None and t.text else None

# checks if entry is from valid year
def valid_year(entry):
    year = extract_tag(entry, "year")
    try:
        if int(year.strip()) >= START_YEAR:
            return year.strip()
    except (TypeError, ValueError):
        return None

# checks if entry is from valid venue
def valid_venue(entry):
    if is_journal(entry):
        key = entry.get("key")
        if "imwut" in key:
            return "IMWUT"
    else:
        v = extract_tag(entry, "booktitle")
        if v:
            v_lower = v.lower()
            for venue in TARGET_VENUES:
                if venue in v_lower:
                    return v
    return None

# checks if entry is valid, and returns all necessary info if valid
def extract_entry(entry):
    year = valid_year(entry)
    venue = valid_venue(entry)
    
    if not year or not venue:
        return None
   
    title = extract_tag(entry, "title")
    if not title:
        return None
   
    ee = extract_tag(entry, "ee")
    url = extract_tag(entry, "url")
    
    if url and not url.startswith("http"):
        url = "https://dblp.org/" + url
   
    authors = [a.text.strip() for a in entry.findall("author") if a.text]
    if not authors:
        authors = ["N/A"]

    return {
        "title": title,
        "authors": "; ".join(authors),
        "year": year,
        "venue": venue,
        "ee": ee,
        "url": url,
    }

# --- PARSER ---
def parse_dblp(xml_file):
    results = []
    total = 0

    context = etree.iterparse(xml_file, events=('end',), tag=TYPE)

    print("Parsing DBLP... (this may take several minutes)")
    for _, element in tqdm(context, desc="Entries processed", unit="entry"):
        total += 1
        
        try:
            record = extract_entry(element)
        except Exception as e:
            print(f"Skipping entry due to error: {e}")
            continue
    
        if record:
            results.append(record)

        # Free memory
        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]

    print(f"\nTotal entries parsed: {total}")
    print(f"Total matching papers: {len(results)}")
    return results

# --- MAIN ---
if __name__ == "__main__":
    xml_file = "test.xml" 
    papers = parse_dblp(xml_file)

    df = pd.DataFrame(papers)
    output_file = "test_filtered.csv"
    df.to_csv(output_file, index=False)
    print("Saved to " + output_file)
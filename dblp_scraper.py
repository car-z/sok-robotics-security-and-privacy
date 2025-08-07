from lxml import etree
from tqdm import tqdm
import pandas as pd
import html
import re
from html.entities import name2codepoint

# --- PARAMETERS ---
# TARGET_VENUES = {
#     "mobisys", "mobicom", "sensys", "chi", "ubicomp", "imwut", "sigcomm", "nsdi"
# }
TARGET_VENUES = {
     "SP", "USENIX Security Symposium", "CCS", "NDSS", "SOUPS @ USENIX Security Symposium", "EuroS&P", "ICCPS", "IROS", "ICRA"
 }

START_YEAR = 2020 # 2020 - 2025
TYPE = ("inproceedings", "article") # only pull papers

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
    if year is None:
        return None
    try:
        if int(year) >= START_YEAR:
            return year
    except ValueError:
        return None

# checks if entry is from valid venue
def valid_venue(entry):
    if is_journal(entry):
        key = entry.get("key")
        if "popets" in key:
            return "PETS"
    else:
        v = extract_tag(entry, "booktitle")
        if v:
            for venue in TARGET_VENUES:
                if re.search(rf'\b{re.escape(venue)}\b', v):
                    return venue
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
def parse_dblp(xml_file, skip=0, max=None):
    results = []
    total = 0
    skipped = 0

    parser = etree.XMLParser(load_dtd=False, no_network=True, recover=True, resolve_entities=False)
    
    with open(xml_file, 'rb') as file:  # open file as binary
        try:
            context = etree.iterparse(
                file,
                events=('end',),
                tag=TYPE,
                load_dtd=False,
                no_network=True,
                resolve_entities=False,
                recover=True,
                huge_tree=True
            )
        except Exception as e:
            print(f"Could not initialize parser: {e}")
            return []
        
        print("Parsing DBLP... (this may take several minutes)")
        for _, element in tqdm(context, desc="Entries processed", unit="entry"):
            total += 1

            if total < skip:
                continue

            if max and total >= max:
                break
        
            try:
                record = extract_entry(element)
                if record:
                    results.append(record)
            except Exception as e:
                skipped += 1
                print(f"Skipping entry {total} due to error: {e}")
                try:
                    print(etree.tostring(element, pretty_print=True, encoding="unicode"))
                except Exception as sub_e:
                    print(f"Could not print element {total}: {sub_e}")
            finally:
                # Free memory
                try:
                    element.clear()
                    while element.getprevious() is not None:
                        del element.getparent()[0]
                except Exception as cleanup_e:
                    print(f"Cleanup error at entry {total}: {cleanup_e}")
                    continue

    print(f"\nTotal entries parsed: {total}")
    print(f"Total matching papers: {len(results)}")
    print(f"Total skipped entries: {skipped}")
    return results

# --- MAIN ---
if __name__ == "__main__":
    papers = parse_dblp("dblp/dblp.xml")

    df = pd.DataFrame(papers)
    output_file = "security conference scrape.csv"
    df.to_csv(output_file, index=False)
    print("Saved to " + output_file)
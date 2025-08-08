# script to search for papers with these new keywords, provided they haven't already been added
import pandas as pd
import re

# -- PARAMETERS ----

CATEGORIES = {
    "NEW KEYWORDS": {
        'privacy preserving', 'resilience', 'fidelity', 'quadcopter', 'cyberattack', 
        'eavesdropping', 'self-driving', 'phishing', 'intrusion', 
        'digital signature', 'unmaned', 'penetration testing',
        'blockchain', 'authentication', 'automated vehicle', 'exploit', 
        'cybersecurity', 'access control', 'side channel', 'autonomous', 'automated',
        'blurring', 'side-channel', 'key management', 'attack', 'data exfiltration', 
        'ZPK', 'privacy enhancing', 'manipulator', 'zero-proof knowledge', 
        'identity management', 'pentest', 'spoofing', 'secure', 'cyber attack', 
        'agrobot', 'cobot', 'quadrotor', 'safety', 'breach', 'replay attack', 
        'identification', 'multirotor'
    }
}

RISKY_KEYWORDS = {
    "uav", "ugv", "rov", "auv", "usv"
}

CATEGORIES["RISKY_KEYWORDS"] = RISKY_KEYWORDS

# -- HELPERS --
def keyword_match(title, keyword):
    title = title.lower()
    keyword = keyword.lower()
    if keyword in RISKY_KEYWORDS:
        return re.search(rf'\b{re.escape(keyword)}\b', title, re.IGNORECASE) is not None
    else:
        return keyword in title

# -- MAIN FILTERING FUNCTION --  
def save_keywords(input):
    input = input.copy()
    matched_categories = []
    match_counts = []

    for i in range(len(input)):
        title = input.at[i, 'title']
        paper_categories = []
        num_matches = 0

        if pd.isna(title):
            matched_categories.append([])
            match_counts.append(0)
            continue

        for category_name, keyword_set in CATEGORIES.items():
            for keyword in keyword_set:
                if keyword_match(title, keyword):
                    paper_categories.append(category_name)
                    num_matches += 1
        
        matched_categories.append(paper_categories)
        match_counts.append(num_matches)
    
    input['matched categories'] = matched_categories
    input['match counts'] = match_counts

    filtered_rows = []
    for i in range(len(input)):
        if match_counts[i] > 0:
            input.at[i, 'matched categories'] = ', '.join(sorted(set(matched_categories[i])))
            filtered_rows.append(input.iloc[i])

    filtered = pd.DataFrame(filtered_rows)
    return filtered

# -- MAIN -- 
df = pd.read_csv('scraped_data/mobile_systems/filtered.csv')
print("Original length:",len(df))

output_df = save_keywords(df)
print("NEW keyword pulls:",len(output_df))

og_title_filter_df = pd.read_csv('scraped_data/mobile_systems/filtered_by_title.csv')
print("ORIGINAL keyword pulls: ",len(og_title_filter_df))

result = output_df[~output_df['title'].isin(og_title_filter_df['title'])]

print("NEW keyword pulls not in original: ", len(result))

result.to_csv("scraped_data/mobile_systems/new_keyword_pulls.csv",index=False)
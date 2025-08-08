# script to cut down papers to only those containing specified keywords in title
import pandas as pd
import re

# -- PARAMETERS --

CATEGORIES = {
    "ROBOT": {
        "robot", "robotics", "mobile robot", "robot mobility", "autonomous vehicle", "automated vehicle", "automated",
        "autonomous", "self-driving", "cobot", "manipulator", "unmaned", "agrobot", 
        "delivery robot", "vacuum", "drone", "telepresence robot", "humanoid robot", "rover",
        "inspection robot", "service robot", "home robot", "domestic robot", "assistive robot",
        "companion robot", "food service robot", "surveillance robot", "robot navigation", "multirotor",
        "quadrotor", "quadcopter",
    },
    "VISUAL": {
        "camera", "rgb camera", "vision", "visual", "thermal imaging", "infrared camera", "infrared imaging",
        "depth", "lidar", "structured light", "3d sensing", "stereo vision"
    }, 
    "AUDIO": {
        "microphone", "acoustic", "ultrasonic", "ultrasound",
        "passive listening", "active audio sensing", "doppler sensing", "sound localization"
    },
    "RADAR": {
        "radar", "radio frequency", "mmwave", "millimeter wave", "wifi sensing",
        "fmcw", "rf sensing", "wireless sensing", 
    },
    "OTHER_SENSORS": {
        "accelerometer", "gyroscope", "ambient light", "light sensor", "temperature sensor",
        "sensor fusion", "multi-modal sensing", "multimodal sensing", "light-based sensor"
    }, 
    "PRIVACY_AND_SECURITY": {
        "privacy", "security", "sensor privacy", "data privacy", "user privacy", "privacy-preserving",
        "privacy preserving", "privacy enhancing", "safety", "resilience", "attack",
        "privacy-aware", "privacy control", "data leakage", "privacy risk", "sensor leakage",
        "user privacy", "data collection", "context-aware privacy", "surveillance", "anonymization",
        "obfuscation", "masking", "cloaking", "blurring", "spoofing", "jamming", "sensor blocking",
        "invisibility cloak", "retroreflective material", "adversarial", "privacy paradox", "trusted execution", "authentication", "fidelity",
        "selective sensing", "privacy-aware sensing", "cybersecurity", "cyber attack", "cyberattack", "breach", "intrusion", "exploit", 
        "penetration testing", "pentest", "side-channel", "side channel", "replay attack", "eavesdropping", "data exfiltration", "phishing", 
        "secure", "digital signature", "blockchain", "access control", "key management", "identity management", "identification", "zero-proof knowledge", 
        "ZPK"
    }, 
}

RISKY_KEYWORDS = {
    "ir", "rf", "imu", "ros", "uav", "ugv", "auv", "uav", "rov", "usv"
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
df = pd.read_csv('scraped_data/SP/filtered.csv')
print("Original length:",len(df))

output_df = save_keywords(df)
print("Length after keyword filtering:",len(output_df))

output_df.to_csv("scraped_data/SP/revised_filtered_by_title.csv",index=False)
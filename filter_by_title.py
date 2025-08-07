import pandas as pd
import re

# -- PARAMETERS --

CATEGORIES = {
    "ROBOT": {
        "robot", "robotics", "mobile robot", "robot mobility", "autonomous vehicle", "automated vehicle",
        "delivery robot", "vacuum", "drone", "telepresence robot", "humanoid robot", "rover",
        "inspection robot", "service robot", "home robot", "domestic robot", "assistive robot",
        "companion robot", "food service robot", "surveillance robot", "robot navigation"
    },
    "VISUAL": {
        "camera", "rgb camera", "vision", "visual", "thermal imaging", "infrared camera", "infrared imaging",
        "depth", "lidar", "structured light", "3d sensing", "stereo vision"
    }, 
    "AUDIO": {
        "microphone", "acoustic", "ultrasonic", "ultrasound", "voice assistant",
        "passive listening", "active audio sensing", "doppler sensing", "sound localization"
    },
    "RADAR": {
        "radar", "radio frequency", "mmwave", "millimeter wave", "wifi sensing",
        "fmcw", "rf sensing", "wireless sensing", "channel state information"
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
        "obfuscation", "masking", "cloaking", "sensor spoofing", "jamming", "sensor blocking",
        "invisibility cloak", "retroreflective material", "adversarial", "privacy paradox", "trusted execution", "authentication"
    },
    "SENSOR_USE_CASES": {
        "activity recognition", "behavior inference", "presence detection", "people tracking",
        "indoor localization", "occupancy detection", "gesture recognition", "gait recognition",
        "sleep monitoring", "health monitoring", "facial recognition", "emotion recognition",
    },
    "PRIVACY_SOLUTIONS": {
        "edge computing", "on-device processing", "data minimization", "fidelity reduction",
        "granular privacy control", "sensor calibration", "differential privacy",
        "selective sensing", "privacy budget", "facial blurring", "sensor shutoff",
        "privacy-aware sensing", "trusted execution environment",
        "trusted platform", "secure enclave", "hardware isolation"
    },
    "DEPLOYMENT": {
        "smart home", "smart device", "smart speaker", "cloud processing",
        "data governance", "user consent", "privacy settings", "manufacturer privacy",
        "industrial robot", "consumer robot", "edge intelligence", "server security",
        "os-level security", "firmware attack", "robot operating system",   
    }
}

RISKY_KEYWORDS = {
    "ir", "rf", "csi", "imu", "tpm", "tee", "ros", "iot"
}

CATEGORIES["RISKY_KEYWORDS"] = RISKY_KEYWORDS

# KEYWORDS = {
#     "robot", "robotics", "privacy", "mobile robot", "robot mobility", "sensing",
#     "autonomous", "sensor", "audio", "microphone", "voice assistant","acoustic",
#     "activity recognition", "visual", "RGB", "camera", "LiDAR", "thermal", "vision",
#     "image", "radar", "radio frequency", "imaging", "light", "surveillance",
#     "privacy-preserving", "jamming", "privacy-aware", "edge computing", "adversarial",
#     "spoof", "cloaking", "wearable", "invisibility", "fidelity", "millimeter wave",
#     "mm wave", "ultrasonic", "ultrasound", "infrared", "depth", "data collection",
#     "minimization", "on-device", "tradeoff", "risk", "context-aware", "leakage",
#     "edge inference", "drone", "telepresence", "vacuum", "assistive", "navigation",
#     "mapping", "localization", "pose estimation", "masking", "obfuscation",
#     "anonymization", "smart"
# }

# RISKY_KEYWORDS = {
#     "imu", "rf", "ir", "data", "slam", "fov"
# }

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
df = pd.read_csv('filtered.csv')
print("Original length:",len(df))

output_df = save_keywords(df)
print("Length after keyword filtering:",len(output_df))

# output_df.to_csv("filtered_by_category.csv",index=False)
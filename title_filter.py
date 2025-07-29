import pandas as pd

# -- PARAMETERS --
KEYWORDS = {
    "robot",
    "robotics"
    "privacy",
    "mobile",
    "sensing",
    "autonomous",
    "sensor",
    "audio",
    "microphone",
    "voice assistant",
    "ultrasonic",
    "acoustic",
    "activity recognition",
    "visual",
    "RGB",
    "camera",
    "LiDAR",
    "thermal imaging",
    "vision",
    "image",
    "radar",
    "RF",
    "imaging",
    "IMU",
    "light",
    "surveillance",
    "privacy-preserving",
    "jamming",
    "privacy-aware",
    "edge computing",
    "data",
    "adversarial",
    "spoofing",
    "spoof",
    "jamming",
    "jam",
    "cloaking",
    "wearable",
    "invisibility",
    "FOV",
    "fidelity"
}

# -- HELPERS --
def save_keywords(input, output):
    for keyword in KEYWORDS:
        keyword = keyword.lower()
        keyword_output = input[input['title'].str.lower().str.contains(keyword, na=False)]
        output = pd.concat([output, keyword_output], ignore_index=True)
    output = output.drop_duplicates()
    return output

# -- MAIN -- 
df = pd.read_csv('filtered.csv')
print("Original length: " + str(len(df)))

output_df = pd.DataFrame(columns=list(df.columns))
output_df = save_keywords(df, output_df)
print("Length after keyword filtering: " + str(len(output_df)))

output_df.to_csv("keyword_filtering.csv",index=False)

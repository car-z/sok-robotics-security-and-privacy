# used to write temporary scripts for data analysis lol

# ---- looking for what new keywords I added -------------------------------
second_set_of_keywords = {
    
    "robot", "robotics", "mobile robot", "robot mobility", "autonomous vehicle", "automated vehicle",
    "autonomous", "self-driving", "cobot", "manipulator", "unmaned", "agrobot", 
    "delivery robot", "vacuum", "drone", "telepresence robot", "humanoid robot", "rover",
    "inspection robot", "service robot", "home robot", "domestic robot", "assistive robot",
    "companion robot", "food service robot", "surveillance robot", "robot navigation", "multirotor",
    "quadrotor", "quadcopter",
 
    "camera", "rgb camera", "vision", "visual", "thermal imaging", "infrared camera", "infrared imaging",
    "depth", "lidar", "structured light", "3d sensing", "stereo vision",

    "microphone", "acoustic", "ultrasonic", "ultrasound",
    "passive listening", "active audio sensing", "doppler sensing", "sound localization",

    "radar", "radio frequency", "mmwave", "millimeter wave", "wifi sensing",
    "fmcw", "rf sensing", "wireless sensing", 

    "accelerometer", "gyroscope", "ambient light", "light sensor", "temperature sensor",
    "sensor fusion", "multi-modal sensing", "multimodal sensing", "light-based sensor",
   
    "privacy", "security", "sensor privacy", "data privacy", "user privacy", "privacy-preserving",
    "privacy preserving", "privacy enhancing", "safety", "resilience", "attack",
    "privacy-aware", "privacy control", "data leakage", "privacy risk", "sensor leakage",
    "user privacy", "data collection", "context-aware privacy", "surveillance", "anonymization",
    "obfuscation", "masking", "cloaking", "blurring", "spoofing", "jamming", "sensor blocking",
    "invisibility cloak", "retroreflective material", "adversarial", "privacy paradox", "trusted execution", "authentication", "fidelity",
    "selective sensing", "privacy-aware sensing", "cybersecurity", "cyber attack", "cyberattack", "breach", "intrusion", "exploit", 
    "penetration testing", "pentest", "side-channel", "side channel", "replay attack", "eavesdropping", "data exfiltration", "phishing", 
    "secure", "digital signature", "blockchain", "access control", "key management", "identity management", "identification", "zero-proof knowledge", 
    "ZPK",

    "ir", "rf", "imu", "ros", "uav", "ugv", "auv", "uav", "rov", "usv"
}

first_set_of_keywords = {
       
    "robot", "robotics", "mobile robot", "robot mobility", "autonomous vehicle",
    "delivery robot", "vacuum", "drone", "telepresence robot", "humanoid robot", "rover",
    "inspection robot", "service robot", "home robot", "domestic robot", "assistive robot",
    "companion robot", "food service robot", "surveillance robot", "robot navigation",
   
    "camera", "rgb camera", "vision", "visual", "thermal imaging", "infrared camera", "infrared imaging",
    "depth", "lidar", "structured light", "3d sensing", "stereo vision",
    
    "microphone", "acoustic", "ultrasonic", "ultrasound", "voice assistant",
    "passive listening", "active audio sensing", "doppler sensing", "sound localization",
   
    "radar", "radio frequency", "mmwave", "millimeter wave", "wifi sensing",
    "fmcw", "rf sensing", "wireless sensing", "channel state information",
    
    "accelerometer", "gyroscope", "ambient light", "light sensor", "temperature sensor",
    "sensor fusion", "multi-modal sensing", "multimodal sensing", "light-based sensor",
  
   
    "privacy", "security", "sensor privacy", "data privacy", "user privacy", "privacy-preserving",
    "privacy-aware", "privacy control", "data leakage", "privacy risk", "sensor leakage",
    "user privacy", "data collection", "context-aware privacy", "surveillance", "anonymization",
    "obfuscation", "masking", "cloaking", "sensor spoofing", "jamming", "sensor blocking",
    "invisibility cloak", "retroreflective material", "adversarial", "privacy paradox", "trusted execution",
   
    "activity recognition", "behavior inference", "presence detection", "people tracking",
    "indoor localization", "occupancy detection", "gesture recognition", "gait recognition",
    "sleep monitoring", "health monitoring", "facial recognition", "emotion recognition",

    "edge computing", "on-device processing", "data minimization", "fidelity reduction",
    "granular privacy control", "sensor calibration", "differential privacy",
    "selective sensing", "privacy budget", "facial blurring", "sensor shutoff",
    "privacy-aware sensing", "trusted execution environment",
    "trusted platform", "secure enclave", "hardware isolation",
 
    "smart home", "smart device", "smart speaker", "cloud processing",
    "data governance", "user consent", "privacy settings", "manufacturer privacy",
    "industrial robot", "consumer robot", "edge intelligence", "server security",
    "os-level security", "firmware attack", "robot operating system",   

    "ir", "rf", "csi", "imu", "tpm", "tee", "ros", "iot"
}

only_in_second_set = second_set_of_keywords - first_set_of_keywords
print(only_in_second_set)
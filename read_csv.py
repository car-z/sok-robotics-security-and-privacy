import pandas as pd

# df = pd.read_csv("dblp_07_25_2025_filtered.csv")
# print(len(df))

# poster = "poster"
# df_filtered = df[~df['title'].str.lower().str.contains(poster)]
# df_filtered = df_filtered[~df_filtered['venue'].str.lower().str.contains(poster)]
# print(len(df_filtered))

# removed = len(df) - len(df_filtered)

# print("Removed: " + str(removed))

# df_filtered.to_csv("no_posters.csv", index=False)

# df = pd.read_csv("no_posters.csv")
# print("Original length: " + str(len(df)))

# df_chi = df[df['venue'].str.lower().str.contains('chi')]
# df_extended_abstract = df[df['venue'].str.lower().str.contains('extended abstracts')]
# print("# CHI papers: " + str(len(df_chi)))
# print ("# non-CHI papers: " + str(len(df) - len(df_chi)))
# print("# Extended Abstracts: " + str(len(df_extended_abstract)))

# df_no_extended_abstracts = df[~df['venue'].str.lower().str.contains('extended abstracts')]
# removed = len(df) - len(df_no_extended_abstracts)

# print("Removed: " + str(removed))

# df_no_extended_abstracts.to_csv("no_extended_abstracts.csv", index=False)

df = pd.read_csv("no_extended_abstracts.csv")
print("Original length: " + str(len(df)))
df_chi = df[df['venue'].str.lower().str.contains('chi')]
print("# CHI papers: " + str(len(df_chi)))
print ("# non-CHI papers: " + str(len(df) - len(df_chi)))
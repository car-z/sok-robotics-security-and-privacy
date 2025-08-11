import pandas as pd

def remove_venue(name, input):
    name = name.lower()
    print("Original length: " + str(len(input)))
    output = input[~input['venue'].str.lower().str.contains(name)]
    removed = len(input) - len(output)
    print("Removed: " + str(removed))
    return output

def count_occurrence(field, keyword, input):
    keyword = keyword.lower()
    key = input[input[field].str.lower().str.contains(keyword)]
    count = str(len(key))
    # key.to_csv('only_robot_papers.csv', index=False)
    print("# " + keyword + " papers: " + count)
    return

def remove_from_title(title, input):
    title = title.lower()
    print("Original length: " + str(len(input)))
    output = input[~input['title'].str.lower().str.contains(title)]
    removed = len(input) - len(output)
    print("Removed: " + str(removed))
    return output

def remove_from_ee(ee, input):
    ee = ee.lower()
    print("Original length: " + str(len(input)))
    output = input[~input['ee'].str.lower().str.contains(ee)]
    removed = len(input) - len(output)
    print("Removed: " + str(removed))
    return output

def only_keep(field, keyword, input):
    keyword = keyword.lower()
    output = pd.DataFrame(columns=input.columns)
    for index, row in df.iterrows():
        value = str(row[field]).lower()
        if keyword in value:
            output = pd.concat([output, df.iloc[[index]]],ignore_index=True)
    return output


# OPERATIONS
df = pd.read_csv('scraped_data/SP/revised_filtered_by_title.csv')
count_occurrence('matched categories','RISKY_KEYWORDS',df)
output = only_keep('matched categories','RISKY_KEYWORDS',df)
print(len(output))

only_privacy = pd.read_csv('scraped_data/SP/only_privacy.csv')
print(len(only_privacy))

intersection_df = only_privacy[only_privacy['title'].isin(output['title'])].copy()
print(len(intersection_df))

intersection_df.to_csv("scraped_data/SP/abbrevSP.csv",index=False)
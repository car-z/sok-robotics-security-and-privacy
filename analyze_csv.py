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
    key.to_csv('only_robot_papers.csv', index=False)
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


# OPERATIONS
df = pd.read_csv('scraped_data/SP/filtered.csv')
output = remove_from_title("Poster abstract", df)
# output = remove_from_title("(poster)", output)
output = remove_from_title("poster ", output)
print(len(output))
output.to_csv("scraped_data/SP/filtered.csv",index=False)


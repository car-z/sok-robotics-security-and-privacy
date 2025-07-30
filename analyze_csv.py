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


# OPERATIONS
df = pd.read_csv('filtered_by_category.csv')
count_occurrence('matched categories','ROBOT',df)

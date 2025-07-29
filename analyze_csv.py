import pandas as pd

def remove_venue(name, input):
    name = name.lower()
    print("Original length: " + str(len(input)))
    output = input[~input['venue'].str.lower().str.contains(name)]
    removed = len(input) - len(output)
    print("Removed: " + str(removed))
    return output

def count_occurence(field, keyword, input):
    keyword = keyword.lower()
    key = input[input[field].str.lower().str.contains(keyword)]
    count = str(len(key))
    print("# " + keyword + " papers: " + count)
    return

df = pd.read_csv('filtered.csv')
print(len(df))
venue_counts_df = df['venue'].value_counts(dropna=False).reset_index()
venue_counts_df.columns = ['venue', 'count']
venue_counts_df.to_csv('venue_counts.csv', index=False)
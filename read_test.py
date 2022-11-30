import pandas as pd




def find_index1(item):
    matched = list(record[record == item].index)
    return matched


record = pd.Series(['Japan', 'America', 'China', 'Canada','Japan'])
print(record)

print(find_index1('Japan'))
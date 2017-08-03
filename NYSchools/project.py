import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}

for file in data_files:
    data_key = file.split(".")[0]
    data[data_key] = pd.read_csv("schools/" + file)

#explore the sat_scores data set. print the first 5 rows

print(data["sat_results"].head())
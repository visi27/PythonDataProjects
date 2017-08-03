import pandas as pd
pd.set_option('display.width', 200)
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

# explore the sat_scores data set. print the first 5 rows

for key in data:
    print(key)
    print(data[key].head())

# Read survey files
all_survey = pd.read_csv("schools/survey_all.txt", delimiter="\t", encoding="windows-1252")
d75_survey = pd.read_csv("schools/survey_d75.txt", delimiter="\t", encoding="windows-1252")

# Combine survey data sets in a single data set
survey = pd.concat([all_survey, d75_survey], axis=0)

print(survey.head())

# Uppercase DBN so it is consistent with the other data sets in data dictionary
survey["DBN"] = survey["dbn"]

# Columns we want to keep from surveys
columns_to_keep = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11",
                   "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11",
                   "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]

# filter the dataframe
survey = survey.loc[:, columns_to_keep]
data["survey"] = survey
data["survey"].head()

# Uppercase DBN so it is consistent with the other data sets in data dictionary
data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

# Generate DBN for class_size data set. First convert to string and  zerofill CSD so it is always 2 characters long
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(lambda x: str(x).zfill(2))

# Concat the newly created padded_csd with SCHOOL CODE to get DBN
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]
data["class_size"].head()

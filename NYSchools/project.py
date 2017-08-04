import pandas as pd
import re
import numpy

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

# Uppercase DBN so it is consistent with the other data sets in data dictionary
data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

# Generate DBN for class_size data set. First convert to string and  zerofill CSD so it is always 2 characters long
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(lambda x: str(x).zfill(2))

# Concat the newly created padded_csd with SCHOOL CODE to get DBN
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]

# Calculate total SAT score from individual sat scores
data["sat_results"]["SAT Math Avg. Score"] = pd.to_numeric(data["sat_results"]["SAT Math Avg. Score"], errors='coerce')
data["sat_results"]["SAT Critical Reading Avg. Score"] = pd.to_numeric(
    data["sat_results"]["SAT Critical Reading Avg. Score"], errors='coerce')
data["sat_results"]["SAT Writing Avg. Score"] = pd.to_numeric(data["sat_results"]["SAT Writing Avg. Score"],
                                                              errors='coerce')
data["sat_results"]["sat_score"] = data["sat_results"]["SAT Math Avg. Score"] + data["sat_results"][
    "SAT Critical Reading Avg. Score"] + data["sat_results"]["SAT Writing Avg. Score"]

print(data["sat_results"]["sat_score"].head())


# Extract location coordinate of schools
# Define functions to extract latitude and longitude
def extract_lat(loc):
    coords = re.findall("\(.+\)", loc)
    if len(coords) > 0:
        lat = coords[0].split(",")[0].replace("(", "")
        return lat
    return ""


def extract_lon(loc):
    coords = re.findall("\(.+\)", loc)
    if len(coords) > 0:
        lat = coords[0].split(",")[1].replace(")", "")
        return lat
    return ""

# apply the functions
data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(lambda x: extract_lat(x))
data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(lambda x: extract_lon(x))

# Convert latitude and longitude values to numeric
data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors='coerce')
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors='coerce')

# Explore the class_size dataset
print(data["class_size"])
print(data["class_size"].keys())
print(data["class_size"]["GRADE "].unique())
print(data["class_size"]["PROGRAM TYPE"].unique())

# Lets filter the class size dataset to only contain rows with GRADE '09-12' and PROGRAM TYPE 'GEN ED'
class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == '09-12']
class_size = class_size[class_size["PROGRAM TYPE"] == 'GEN ED']
print(class_size.head())

# Group the dataframe by DBN, compute aggregated values using numpy.mean, reindex and reassign back to data dictionary
class_size = class_size.groupby("DBN").agg({
    'NUMBER OF STUDENTS / SEATS FILLED': numpy.mean,
    'NUMBER OF SECTIONS': numpy.mean,
    'AVERAGE CLASS SIZE': numpy.mean,
    'SIZE OF SMALLEST CLASS': numpy.min,
    'SIZE OF LARGEST CLASS': numpy.max,
    'SCHOOLWIDE PUPIL-TEACHER RATIO': numpy.mean
})

class_size.reset_index(inplace=True)
data['class_size'] = class_size
print(data['class_size'].head())

# Filter demographics, keep only data for schoolyear 20112012
data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012]
print(data["demographics"].head())

# Filter graduation dataset and keep only records with Demographics 'Total Cohort' and latest Cohort of 2006
data["graduation"] = data["graduation"][(data["graduation"]["Cohort"] == '2006') & (data["graduation"]["Demographic"] == 'Total Cohort')]
print(data["graduation"].head())

# Convert columns for the ap_2010 dataset to numeric values
cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

for col in cols:
    data["ap_2010"][col] = pd.to_numeric(data["ap_2010"][col], errors="coerce")
print(data["ap_2010"].head())


# Merge sat_results dataset with ap_2010 and graduation datasets. We will use a left join to preserve sat_results rows
combined = data["sat_results"]
combined = combined.merge(data["ap_2010"], how='left')
combined = combined.merge(data["graduation"], how='left')

print(combined.head())

# Merge the combined dataset with class_size, demographics, survey, and hs_directory. This time we will use
# inner join because this data sets have few missing DBNs
combined = combined.merge(data["class_size"], on="DBN", how="inner")
combined = combined.merge(data["demographics"], on="DBN", how="inner")
combined = combined.merge(data["survey"], on="DBN", how="inner")
combined = combined.merge(data["hs_directory"], on="DBN", how="inner")
print(combined.shape)

# lets fill nan values in the dataset with numbers. Try to fill the missing values with average values from that column.
# First calculate mean values for dataset
means = combined.mean()

# Fill nan-s with mean values
combined = combined.fillna(means)

# Fill remaining nan-s with 0
combined = combined.fillna(0)

# Generate school district values (first 2 characters of DBN) and store them to the column "school_dist"
# This will be usefull for mapping
combined["school_dist"] = combined["DBN"].apply(lambda x: x[0:2])

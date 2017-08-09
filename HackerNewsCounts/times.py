from dateutil.parser import parse

from read import load_data

def extract_hour(timestamp):
    date_time = parse(timestamp)
    return date_time.hour

data = load_data()
data['submission_hour'] = data['submission_time'].apply(extract_hour)
hour_counts = data['submission_hour'].value_counts()
print(hour_counts) 
#
# Analysis of the hvorg screenshots
#

import os
import datetime
import pickle
import json
import numpy as np
import pandas as pd
from sunpy.time import parse_time, is_time

# The sources ids
get_sources_ids = 'getDataSources.json'

# Save the data
save_directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/source')
hvorg_screenshots = 'screenshots.csv'
hvorg_screenshots = 'screenshots_test.csv'
f = os.path.join(directory, hvorg_screenshots)
print('Loading ' + f)
path = os.path.expanduser(f)
df = pd.read_csv(path)

hvorg_screenshots_legacy = 'screenshots_legacy.csv'
hvorg_screenshots_legacy = 'screenshots_test.csv'
f = os.path.join(directory, hvorg_screenshots_legacy)
print('Loading ' + f)
path = os.path.expanduser(f)
df_legacy = pd.read_csv(path)

# Change the IDs of the legacy movies so they are unique
df_legacy.loc[:, "id"] = df_legacy.loc[:, "id"] + 10**(1 + np.int(np.ceil(np.log10(len(df)))))

# Append the legacy movies
df = df.append(df_legacy, ignore_index=True)


# Get some figures of merit for the screenshots
def parse_timestamps(dtlist):
    t = []
    validity = []
    for x in dtlist:
        valid = is_time(x)
        validity.append(valid)
        if valid:
            t.append(parse_time(x))
        else:
            t.append(-1)
    return validity, t

# When was the screenshot requested?
print('Calculating screenshot request times')
request_time_validity, request_time = parse_timestamps(df.timestamp.tolist())

# What was the screenshot start time?
print('Calculating screenshot observation time')
observation_time_validity, obs_time = parse_timestamps(df.ObservationDate.tolist())



# Calculate the time difference between the time of the request and the
# screenshot time.  The start time is used since this is the only one that
# can
print('Calculating time difference between request time and observation time')
n = len(request_time_validity)
time_difference = []
for i in range(0, n):
    if request_time_validity[i] and observation_time_validity[i]:
        time_difference.append([(request_time[i] - obs_time[i]).total_seconds()])
request_time_validity = np.asarray(time_difference)

f = os.path.join(save_directory, 'hvorg_screenshot_time_difference_seconds.npy')
np.save(f, time_difference)

f = os.path.join(save_directory, 'hvorg_screenshot_request_time.pkl')
pickle.dump(request_time, open(f, 'wb'))


# Analyze the Helioviewer getsourcesid return - map the sourceIds to the nicknames
f = os.path.expanduser(os.path.join(directory, get_sources_ids))
j = json.load(open(f, 'r'))


def id_generator(dict_var):
    for k, v in dict_var.items():
        if k == "sourceId":
            yield dict_var["sourceId"], dict_var["nickname"]
        elif isinstance(v, dict):
            for id_val in id_generator(v):
                yield id_val

source_ids_and_nicknames = list(id_generator(j))
f = os.path.join(save_directory, 'hvorg_screenshot_sourceids_and_nicknames.pkl')
pickle.dump(source_ids_and_nicknames, open(f, 'wb'))

all_sources = [str(sian[0]) for sian in source_ids_and_nicknames]


# Create a new dataframe that explicitly holds which data source was used in each screenshot
df_new = pd.DataFrame(0, index=df.index, columns=all_sources)
df_new.index.name = 'screenshot number'
for this_index in df.index:
    source_id = df.loc[this_index, "DataSourceID"]
    ids = source_id.split(',')
    for id in ids:
        df_new.loc[this_index, id] = 1

# Change the column names to the easier to understand source nicknames
df_new_column_names = list(df_new.columns.values)
for df_new_column_name in df_new_column_names:
    for source_id_and_nickname in source_ids_and_nicknames:
        this_source_id = source_id_and_nickname[0]
        this_nickname = source_id_and_nickname[1]
        if df_new_column_name == str(this_source_id):
            df_new.rename(columns={df_new_column_name: this_nickname}, inplace=True)


# Save the source ID information
f = os.path.join(save_directory, 'hvorg_screenshot_data_source_ids.csv')
df_new.to_csv(f)

# Save the data source IDs
f = os.path.join(save_directory, 'hvorg_screenshot_data_source_ids.pkl')
pickle.dump(all_sources, open(f, 'wb'))

#
# Analysis of the hvorg_movies
#

import os
import datetime
import pickle
import numpy as np
import pandas as pd
from sunpy.time import parse_time

# Save the data
save_directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/source')
hvorg_movies = 'movies.csv'
path = os.path.expanduser(os.path.join(directory, hvorg_movies))
df = pd.read_csv(path)

hvorg_legacy_movies = 'movies_legacy.csv'
path = os.path.expanduser(os.path.join(directory, hvorg_legacy_movies))
df_legacy = pd.read_csv(path)

# Change the IDs of the legacy movies so they are unique
df_legacy.loc[:, "id"] = df_legacy.loc[:, "id"] + 10**(1 + np.int(np.ceil(np.log10(len(df)))))

# Append the legacy movies
df = df.append(df_legacy, ignore_index=True)


data_type = 'helioviewer.org movies'

# Get some figures of merit for the movies
# When was the movie requested?
request_time = [parse_time(x) for x in df.timestamp.tolist()]

# What was the movie start time?
movie_start_time = [parse_time(x) for x in df.StartDate.tolist()]

# What was the movie end time?
movie_end_time = [parse_time(x) for x in df.EndDate.tolist()]

# How many movies in the CSV file?
nmovies = len(request_time)

# How much time did the movie cover?
movie_durations = np.asarray([(movie_end_time[i] - movie_start_time[i]).total_seconds() for i in range(0, nmovies)])

# What was the mid point of the movie?
movie_mid_point = [movie_start_time[i] + datetime.timedelta(seconds=0.5*movie_durations[i]) for i in range(0, nmovies)]

# Calculate the time difference between the time of the request and the
# movie time.  The start time is used since this is the only one that
# can
time_difference = np.asarray([(request_time[i] - movie_start_time[i]).total_seconds() for i in range(0, nmovies)])

# Save the time information
f = os.path.join(save_directory, 'hvorg_movie_durations_seconds.npy')
np.save(f, movie_durations)

f = os.path.join(save_directory, 'hvorg_movie_mid_point_seconds.npy')
np.save(f, movie_mid_point)

f = os.path.join(save_directory, 'hvorg_movie_time_difference_seconds.npy')
np.save(f, time_difference)

f = os.path.join(save_directory, 'hvorg_movie_request_time.pkl')
pickle.dump(request_time, open(f, 'wb'))

f = os.path.join(save_directory, 'hvorg_movie_start_time.pkl')
pickle.dump(movie_start_time, open(f, 'wb'))

f = os.path.join(save_directory, 'hvorg_movie_end_time.pkl')
pickle.dump(movie_end_time, open(f, 'wb'))


# Analyze the sourceID column.  Split it up, find the unique elements,
# and create a data frame.
all_sources = []
for source_id in df.DataSourceID.tolist():
    ids = source_id.split(',')
    for id in ids:
        if id not in all_sources:
            all_sources.append(id)


def extract_data_source_names(a, removal_type='all'):
    if removal_type == 'all':
        b = a.replace(" ", "")
        b = b.split(',')
    if removal_type == 'lr':
        b = a.strip()
        b = b.split(' , ')
    return b

all_data_source_names = []
for i, data_source_names in enumerate(df.DataSourceNames.tolist()):
    if isinstance(data_source_names, str):
        dsns = extract_data_source_names(data_source_names, removal_type='lr')
        for dsn in dsns:
            if dsn not in all_data_source_names:
                all_data_source_names.append(dsn)


df_new = pd.DataFrame(0, index=df.index, columns=all_sources)
df_new.index.name = 'movie number'

# Save the source ID information
for this_index in df.index:
    source_id = df.loc[this_index, "DataSourceID"]
    ids = source_id.split(',')
    for id in ids:
        df_new.loc[this_index, id] = 1

# Save the source ID information
f = os.path.join(save_directory, 'hvorg_data_source_ids.csv')
df_new.to_csv(f)

# Save the data source names
f = os.path.join(save_directory, 'hvorg_data_source_names.pkl')
pickle.dump(all_data_source_names, open(f, 'wb'))

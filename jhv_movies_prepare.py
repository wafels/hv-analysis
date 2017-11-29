#
# Analysis of the jhvorg_movies
#

import os
import datetime
import pickle
import json
import numpy as np
import pandas as pd
from sunpy.time import parse_time

# Save the data
save_directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/source')
jhv_movies = 'movies.csv'
path = os.path.expanduser(os.path.join(directory, jhv_movies))
df = pd.read_csv(path)

data_type = 'Jhelioviewer movies'

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
f = os.path.join(save_directory, 'jhv_movie_durations_seconds.npy')
np.save(f, movie_durations)

f = os.path.join(save_directory, 'jhv_movie_mid_point_seconds.npy')
np.save(f, movie_mid_point)

f = os.path.join(save_directory, 'jhv_movie_time_difference_seconds.npy')
np.save(f, time_difference)

f = os.path.join(save_directory, 'jhv_movie_request_time.pkl')
pickle.dump(request_time, open(f, 'wb'))

f = os.path.join(save_directory, 'jhv_movie_start_time.pkl')
pickle.dump(movie_start_time, open(f, 'wb'))

f = os.path.join(save_directory, 'jhv_movie_end_time.pkl')
pickle.dump(movie_end_time, open(f, 'wb'))


# Change the column names to the easier to understand source nicknames
df_new_column_names = list(df_new.columns.values)
for df_new_column_name in df_new_column_names:
    for source_id_and_nickname in source_ids_and_nicknames:
        this_source_id = source_id_and_nickname[0]
        this_nickname = source_id_and_nickname[1]
        if df_new_column_name == str(this_source_id):
            df_new.rename(columns={df_new_column_name: this_nickname}, inplace=True)


# Save the source ID information
f = os.path.join(save_directory, 'jhv_data_source_ids.csv')
df_new.to_csv(f)

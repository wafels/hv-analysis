#
# Analysis of the hvorg_movies
#

import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as u
from sunpy.time import parse_time

# Read in the data
directory = '~/Data/hvanalysis'
hvorg_movies = 'movies.csv'
path = os.path.expanduser(os.path.join(directory, hvorg_movies))
df = pd.read_csv(path)

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

# Clean for negative values of time differences
positive_duration = time_difference > 0
td = time_difference[positive_duration]
md = movie_durations[positive_duration]

# Save the time information


# Analyze the sourceID column.  Split it up, find the unique elements,
# and create a data frame.


# Save the source ID information

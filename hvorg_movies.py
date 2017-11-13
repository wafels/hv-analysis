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
# various movie times
time_difference = np.asarray([(request_time[i] - movie_start_time[i]).total_seconds() for i in range(0, nmovies)])

# Clean for negative values
td = time_difference[time_difference > 0]

# How many good movies?
ngood = len(td)

# Apply units for ease
td = td * u.s

# Minimum and maximum values
td_min = td.min()
td_max = td.max()

# Time difference in days
td_range = td_max - td_min

# Histogram the data
this_unit = u.day
overall_td_bins = 100
overall_td = np.histogram(td.to(this_unit).value, bins=overall_td_bins)

# Make a simple plot
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td.to(this_unit).value, bins=overall_td_bins)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel('time difference ({:s})'.format(str(this_unit)))
plt.ylabel('number of movies')
plt.title('helioviewer.org movies\n time difference between time of request and movie start time')
plt.show()

# Look at the movies with less than 30 days
td_short_limit = 30*u.day
td_short = td[td < td_short_limit]
td_short_unit = u.day
td_short_fraction = 24

fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td_short.to(td_short_unit).value, bins=int(td_short_limit.to(td_short_unit).value*td_short_fraction))
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel('time difference ({:s})'.format(str(td_short_unit)))
plt.ylabel('number of movies')
plt.title('helioviewer.org movies\n time difference between time of request and movie start time < {:s}'.format(td_short_limit))
plt.show()

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

# How many good movies?
ngood = len(td)

# Apply units - makes handling time durations much easier.
td = td * u.s
md = md * u.s

# Minimum and maximum values
td_min = td.min()
td_max = td.max()

# Time difference in days
td_range = td_max - td_min

# Figure 1
# A plot of all the time differences
this_unit = u.day
overall_td_bins = 100
overall_td = np.histogram(td.to(this_unit).value, bins=overall_td_bins)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td.to(this_unit).value, bins=overall_td_bins)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel('time difference ({:s})'.format(str(this_unit)))
plt.ylabel('number of movies')
plt.title('{:s}\n time difference between time of request and movie start time'.format(data_type))
plt.show()

# Figure 2
# Look at the time differences of movies with time differences less than 30 days
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
plt.title('{:s}\n time difference between time of request and movie start time < {:s}'.format(data_type, td_short_limit))
plt.show()

# Figure 3
# Plot a histogram of movie durations
md_unit = u.hour
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(md, bins=100)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel('duration ({:s})'.format(str(md_unit)))
plt.ylabel('number of movies')
plt.title('{:s}\n duration histogram'.format(data_type))
plt.show()


# Figure 4
# Plot a histogram of movie durations
md_short_limit = 1*u.day
md_short = md[md < md_short_limit]
md_short_unit = u.hour
md_short_fraction = 4
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(md_short.to(md_short_unit).value, bins=int(md_short_limit.to(md_short_unit).value*md_short_fraction))
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel('duration ({:s})'.format(str(md_short_unit)))
plt.ylabel('number of movies')
plt.title('{:s}\n duration histogram for durations < {:s}'.format(data_type, md_short_limit))
plt.show()


# Figure 5
# Scatter plot of time difference versus movie duration
md_scatter_unit = u.day
td_scatter_unit = u.day
fig = plt.figure()
ax = fig.add_subplot(111)
plt.scatter(md.to(md_scatter_unit).value, td.to(td_scatter_unit).value, s=1)
plt.yscale('log')
plt.xscale('log')
mtd_min = np.min([md.to(md_scatter_unit).min().value, md.to(md_scatter_unit).min().value])
mtd_max = np.max([md.to(md_scatter_unit).max().value, md.to(md_scatter_unit).max().value])
plt.plot([mtd_min, mtd_max], [mtd_min, mtd_max], color='k', label='equality')
plt.axvline((1*u.day).to(md_scatter_unit).value, color='r', linestyle='dashed', label='1 day')
plt.axvline((7*u.day).to(md_scatter_unit).value, color='k', linestyle='dashed', label='1 week')
plt.axvline((28*u.day).to(md_scatter_unit).value, color='orange', linestyle='dashed', label='28 days')
plt.axvline((1*u.hour).to(md_scatter_unit).value, color='r', linestyle='dotted', label='1 hour')
plt.axvline((3*u.hour).to(md_scatter_unit).value, color='k', linestyle='dotted', label='3 hours')
plt.axvline((6*u.hour).to(md_scatter_unit).value, color='orange', linestyle='dotted', label='6 hours')
plt.xlabel('movie duration ({:s})'.format(str(md_scatter_unit)))
plt.ylabel('time difference ({:s})'.format(str(td_scatter_unit)))
plt.legend()
plt.title(data_type)
plt.show()


# Figure 6
# Do some analysis on the choice of data sources.


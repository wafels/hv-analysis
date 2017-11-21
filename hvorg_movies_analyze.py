#
# Analysis of the hvorg_movies
#

import os
import pickle
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import astropy.units as u
import hvorg_style as hvos
plt.rc('text', usetex=True)
plt.rc('font', size=14)

restriction = 'observable'
#restriction = 'positive requested duration'

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output location
img = hvos.img

# Type of data we are looking at
data_type = 'helioviewer.org movies ({:s})'.format(restriction)

# How much time did the movie cover?
f = os.path.join(directory, "movie_durations.npy")
movie_durations = np.load(f)
durations_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmduration'][0], hvos.dates['Tmend'], hvos.dates['Tmstart'])

# Movie start times
f = os.path.join(directory, "movie_start_time.pkl")
movie_start_time = pickle.load(open(f, 'rb'))
movie_start_time_date = hvos.dates['Tmstart']

# Movie start times
f = os.path.join(directory, "movie_mid_point.pkl")
movie_mid_point = pickle.load(open(f, 'rb'))
movie_mid_point_date = hvos.dates['Tmmidpoint']

# Movie end times
f = os.path.join(directory, "movie_end_time.pkl")
movie_end_time = pickle.load(open(f, 'rb'))
movie_end_time_date = hvos.dates['Tmend']

# The time the movie was requested
f = os.path.join(directory, "request_time.pkl")
request_time = pickle.load(open(f, 'rb'))

# Number of movies
nmovies = len(movie_start_time)

# Topicality - calculate the time difference between the time of the request and the
# movie start time.
topicality = np.asarray([(request_time[i] - movie_start_time[i]).total_seconds() for i in range(0, nmovies)])
topicality_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmtopicality'][0], hvos.dates['Tmrequest'], movie_start_time_date)

# near_real_time - calculate the time difference between the time of the request and the
# movie end time.
near_real_time = np.asarray([(request_time[i] - movie_end_time[i]).total_seconds() for i in range(0, nmovies)])

# The movie has a non-zero duration
positive_duration = movie_durations > 0

# It was physically possible that we had data for the entire request
physically_possible = near_real_time >= 0

# What kind of restrictions can we put on the times
if restriction == 'observable':
    data_observable = np.logical_and(positive_duration, physically_possible)

if restriction == 'positive requested duration':
    data_observable = deepcopy(positive_duration)

# Restrict the movies we will look at.
td = topicality[data_observable]
md = movie_durations[data_observable]

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

# Figure 1 : topicality
topicality_unit = u.year
overall_td_bins = 100
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td.to(topicality_unit).value, bins=overall_td_bins)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(topicality_unit)))
plt.ylabel(hvos.mlabel(len(td)))
plt.title('{{{:s}}}\n{{{:s}}}'.format(data_type, topicality_subtitle))
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'topicality'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 2: topicality < 30 days
td_short_limit = 30*u.day
td_short = td[td <= td_short_limit]
td_short_unit = u.day
td_short_fraction = 24
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td_short.to(td_short_unit).value, bins=int(td_short_limit.to(td_short_unit).value*td_short_fraction))
ax.grid(True, linestyle='dotted')
rl = hvos.relevant_lines(hvos.lines, tr=[0, 30]*u.day)
for key in list(rl.keys()):
    kwargs = rl[key]
    kwargs['label'] = str(key)
    plt.axvline(key.to(td_short_unit).value, **kwargs)
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(td_short_unit)))
plt.ylabel(hvos.mlabel(len(td_short)))
plt.title('{{{:s}}}\n{{{:s}}} {{{:s}}} {{{:s}}}'.format(data_type, topicality_subtitle, "$\le$", td_short_limit))
plt.legend()
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'topicality_{:s}'.format(str(td_short_limit))))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 3
# Plot a histogram of movie durations
md_unit = u.year
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(md.to(md_unit).value, bins=100)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmduration'][1], hvos.durations['tmduration'][0], str(md_unit)))
plt.ylabel(hvos.mlabel(len(md)))
plt.title('{{{:s}}}\n {{{:s}}}'.format(data_type, durations_subtitle))
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'duration'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

# Figure 4
# Plot a histogram of movie durations
md_short_fraction = 2
for fhist in ((2*u.day, u.hour), (30*u.day, u.day)):
    md_short_limit = fhist[0]
    md_short_unit = fhist[1]
    md_short = md[md < md_short_limit]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.hist(md_short.to(md_short_unit).value, bins=int(md_short_limit.to(md_short_unit).value*md_short_fraction))
    ax.grid(True, linestyle='dotted')
    rl = hvos.relevant_lines(hvos.lines, tr=[0, md_short_limit.to(u.day).value]*u.day)
    for key in list(rl.keys()):
        kwargs = rl[key]
        kwargs['label'] = str(key)
        plt.axvline(key.to(md_short_unit).value, **kwargs)
    plt.yscale('log')
    plt.xlabel(hvos.qlabel(hvos.durations['tmduration'][1], hvos.durations['tmduration'][0], str(md_short_unit)))
    plt.ylabel(hvos.mlabel(len(md_short)))
    plt.title('{{{:s}}}\n{{{:s}}} {{{:s}}} {{{:s}}}'.format(data_type, durations_subtitle, "$\le$", md_short_limit))
    plt.legend()
    plt.tight_layout()
    filename = hvos.overleaf(os.path.join(data_type, 'duration_{:s}'.format(str(md_short_limit))))
    filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
    filepath = os.path.join(img, filename)
    plt.savefig(filepath)


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

for line in list(hvos.lines.keys()):
    kwargs = hvos.lines[line]
    plt.axvline(line.to(md_scatter_unit).value, **kwargs)
    kwargs['label'] = str(line)
    plt.axhline(line.to(md_scatter_unit).value, **kwargs)

plt.xlabel(hvos.qlabel(hvos.durations['tmduration'][1], hvos.durations['tmduration'][0], str(md_scatter_unit)))
plt.ylabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(td_scatter_unit)))
plt.legend()
plt.title(data_type + '\n' + '{{{:s}}} total'.format(str(len(md))))
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'scatter_duration_vs_topicality'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 6
# Number of requests as a function of time
df = pd.DataFrame(request_time, columns=['date'])
# Setting the date as the index since the TimeGrouper works on Index, the date column is not dropped to be able to count
df.set_index('date', drop=False, inplace=True)

plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='Q')).count()
h.rename(columns={'date': 'movies'}, inplace=True)
h.plot(kind='bar', ax=ax)
ax.xaxis_date()
ax.xaxis.set_major_formatter(dates.AutoDateFormatter(dates.AutoDateLocator))
ax.set_title('movies per quarter')
ax.set_ylabel(hvos.mlabel(len(request_time)))
ax.set_xlabel('date')
ax.grid(True, linestyle='dotted')
plt.tight_layout()
plt.show()


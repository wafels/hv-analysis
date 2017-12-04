#
# Analysis of the hvorg_movies
#

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
from sunpy.time import parse_time

import hvorg_style as hvos
plt.rc('text', usetex=True)
plt.rc('font', size=14)
figsize = (10, 5)

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output location
img = hvos.img

# application
application = 'helioviewer.org'

# data product
data_product = 'screenshots'

# Type of data we are looking at
data_analyzed = '{:s} {:s}'.format(application, data_product)
data_type = '{:s}'.format(data_analyzed)

# Time difference
f = os.path.join(directory, 'hvorg_screenshot_time_difference_seconds.npy')
td = np.load(f) * u.s
topicality_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmtopicality'][0], hvos.dates['Tmrequest'], hvos.dates['Tsdate'])

# Screenshot request times
f = os.path.join(directory, "hvorg_screenshot_request_time.pkl")
screenshot_request_time = pickle.load(open(f, 'rb'))

# Number of screenshots
nmovies = len(td)

# Figure 1 : topicality
# Scale size we are interested in
topicality_unit = u.year

# Define the topicality on the scale size
topicality = td.to(topicality_unit).value

# Histogram bins
topicality_bins = 100

# make the plot
plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(topicality, bins=topicality_bins)
ax.grid(True, linestyle='dotted')
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(topicality_unit)))
plt.ylabel(hvos.mlabel(len(td), data_type=data_product))
plt.title('{{{:s}}}\n{{{:s}}}'.format(data_type, topicality_subtitle))
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'topicality'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 2: topicality < 30 days
# Scale size we are interested in
td_short_unit = u.day

# Longest possible topicality
td_short_limit = 30*u.day

# Find the topicalities less than the longest possible
topicality = td.to(td_short_unit)
these = np.abs(topicality) < td_short_limit
topicality = topicality[these].value

# Histogram bins
topicality_bins = int(td_short_limit.to(td_short_unit).value*24)

# Fix the bin size
td_short_fraction = 24
plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(topicality, bins=topicality_bins)
ax.grid(True, linestyle='dotted')
rl = hvos.relevant_lines(hvos.lines, tr=[0, 30]*u.day)
for key in list(rl.keys()):
    kwargs = rl[key]
    kwargs['label'] = str(key)
    plt.axvline(key.to(td_short_unit).value, **kwargs)
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(td_short_unit)))
plt.ylabel(hvos.mlabel(len(topicality), data_type=data_product))
plt.title('{{{:s}}}\n{{{:s}}} {{{:s}}} {{{:s}}}'.format(data_type, topicality_subtitle, "$\le$", td_short_limit))
plt.legend()
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'topicality_{:s}'.format(str(td_short_limit))))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 6
# Number of requests as a function of time
title = 'screenshots per quarter'
df = pd.DataFrame(screenshot_request_time, columns=['date'])
# Setting the date as the index since the TimeGrouper works on Index, the date column is not dropped to be able to count
df.set_index('date', drop=False, inplace=True)

plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='Q')).count()
h.rename(columns={'date': 'movies'}, inplace=True)
h.plot(kind='bar', ax=ax)
new_ticks = []
for dt in h.index:
    new_ticks.append(dt.to_datetime())
ax.set_xticklabels([dt.strftime('%Y-%m-%d') for dt in new_ticks])
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(screenshot_request_time)))
ax.set_xlabel('date')
ax.xaxis.set_tick_params(labelsize=10)
ax.grid(linestyle='dotted')
fig.autofmt_xdate(rotation=65)
plt.legend()
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, title))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

# Figure 7
# Daily numbers as a plot
title = 'daily screenshots requested'
plt.close('all')
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='D')).count()
h.rename(columns={'date': 'movies'}, inplace=True)

movies_per_day = np.asarray(list(h["movies"]))
mean = np.int(np.rint(np.mean(movies_per_day)))
median = np.int(np.rint(np.median(movies_per_day)))
h.plot(kind='line', ax=ax)
ax.axhline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
ax.axhline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(screenshot_request_time)))
ax.set_xlabel('date')
ylim_max = 1.1*np.max(movies_per_day)
ax.set_ylim(0, ylim_max)
# Project events
for event in ('repair', 'bigbreak'):
    ax.fill_betweenx((0, ylim_max),
                     parse_time(hvos.hv_project_dates[event]["date_start"]),
                     parse_time(hvos.hv_project_dates[event]["date_end"]),
                     **hvos.hv_project_dates[event]["kwargs"])

# Solar physics events
for event in ("june7_event", "comet_ison", "flare_flurry2017"):
    ax.axvline(parse_time(hvos.solar_physics_events[event]["date"]),
               **hvos.solar_physics_events[event]["kwargs"])
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.2, facecolor='y')
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, title))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 8
# Distribution of the number of screenshots made per day
title = 'distribution of number of {{{:s}}} per day'.format(data_analyzed)
plt.close('all')
plt.hist(movies_per_day, bins=60, label='movies')
plt.axvline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
plt.axvline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
plt.yscale('log')
plt.xlabel('number of movies per day')
plt.ylabel('number of days\n[{{{:n}}} total]'.format(len(movies_per_day)))
plt.title('{{{:s}}}\n[{{{:n}}} total]'.format(title, np.sum(movies_per_day)))
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.2)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'histogram_number_of_movies_per_day'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

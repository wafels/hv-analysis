#
# Analysis of the hvorg_movies
#

import os
import pickle
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import astropy.units as u
from sunpy.time import parse_time

import hvorg_style as hvos
plt.rc('text', usetex=True)
plt.rc('font', size=14)
figsize = (10, 5)

topicality_calculated_using = 'movie_end_time'

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Event annotation style
edit = 1

# application
application = 'JHelioviewer'
application_short = 'jhv'

# data product
data_product = 'movies'

# Image output location
img = os.path.join(os.path.expanduser(hvos.img), application)

# Type of data we are looking at
data_analyzed = '{:s} {:s}'.format(application, data_product)
data_type = '{:s}'.format(data_analyzed)

# Movie request times
f = os.path.join(directory, "jhv_movie_request_timestamps_only.pkl")
movie_request_time = pickle.load(open(f, 'rb'))

# Number of movies
nmovies = len(movie_request_time)


# Figure 6
# Number of requests as a function of time
title = '{:s} movies per quarter'.format(application)
df = pd.DataFrame(movie_request_time, columns=['date'])
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
ax.set_ylabel(hvos.mlabel(len(movie_request_time)))
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
title = '{:s} daily movies requested ({{{:s}}})'.format(application, hvos.quantity['jhvm'])
plt.close('all')
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='D')).count()
h.rename(columns={'date': 'movies'}, inplace=True)
subtitle = '({{{:s}}} - {{{:s}}})'.format(str(h.index.min().to_pydatetime().date()), str(h.index.max().to_pydatetime().date()))
movies_per_day = np.asarray(list(h["movies"]))
mean = np.int(np.rint(np.mean(movies_per_day)))
median = np.int(np.rint(np.median(movies_per_day)))
h.plot(kind='line', ax=ax)
ax.axhline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
ax.axhline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(movie_request_time)))
ax.set_xlabel('date\n{{{:s}}}'.format(subtitle))
ylim_max = 1.1*np.max(movies_per_day)
ax.set_ylim(0, ylim_max)
# Project events
for event in ('repair', 'bigbreak', 'shutdown2013'):
    ax.fill_betweenx((0, ylim_max),
                     parse_time(hvos.hv_project_dates[event]["date_start"]),
                     parse_time(hvos.hv_project_dates[event]["date_end"]),
                     **hvos.hv_project_dates[event]["kwargs"])

for i, event in enumerate(("newjhv",)):
    this_event = hvos.hv_project_dates[event]
    if edit == 0:
        ax.axvline(parse_time(this_event["date"]), **this_event["kwargs"])
    elif edit == 1:
        t = parse_time(this_event["date"])
        t_pd = str(t.date())
        y = h.loc[t_pd, data_product]
        if y <= 0.1 * max(h[data_product]):
            y = (0.2 + i*0.2) * max(h[data_product])
        plt.axvline(t, color='r', linestyle=":", linewidth=0.5)
        plt.text(t, y, this_event["label"], **this_event["kwargs_text"])

# Solar physics events
for i, event in enumerate(("june7_event", "comet_ison", "flare_flurry2017")):
    this_event = hvos.solar_physics_events[event]
    if edit == 0:
        ax.axvline(parse_time(this_event["date"]), **this_event["kwargs"])
    elif edit == 1:
        t = parse_time(this_event["date"])
        t_pd = str(t.date())
        y = h.loc[t_pd, data_product]
        if y <= 0.1 * max(h[data_product]):
            y = (0.2 + i*0.2) * max(h[data_product])
        plt.axvline(t, color='r', linestyle=":", linewidth=0.5)
        plt.text(t, y, this_event["label"], **this_event["kwargs_text"])


plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.4, facecolor='y', fontsize=9)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, title))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 8
# Distribution of the number of movies made per day
title = 'distribution of number of {{{:s}}} per day'.format(data_analyzed)
plt.close('all')
plt.hist(movies_per_day, bins=60, label='movies')
plt.axvline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
plt.axvline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
plt.yscale('log')
plt.xlabel('number of movies per day ({{{:s}}})'.format(hvos.quantity['jhvm']))
plt.ylabel('number of days\n[{{{:n}}} total]'.format(len(movies_per_day)))
plt.title('{{{:s}}}\n[{{{:n}}} total]'.format(title, np.sum(movies_per_day)))
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.2)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'histogram_number_of_movies_per_day'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

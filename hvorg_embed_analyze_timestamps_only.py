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


# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# application
application = 'helioviewer.org'
application_short = 'hvorg'

# data product
data_product = 'embeds'

# Image output location
img = os.path.join(os.path.expanduser(hvos.img), application)


# Type of data we are looking at
data_analyzed = '{:s} {:s}'.format(application, data_product)
data_type = '{:s}'.format(data_analyzed)

# Movie request times
f = os.path.join(directory, "hvorg_embed_request_timestamps_only.pkl")
movie_request_time = pickle.load(open(f, 'rb'))

# Number of embeds
n = len(movie_request_time)


# Figure 6
# Number of requests as a function of time
title = '{:s} embeds per quarter'.format(application)
df = pd.DataFrame(movie_request_time, columns=['date'])
# Setting the date as the index since the TimeGrouper works on Index, the date column is not dropped to be able to count
df.set_index('date', drop=False, inplace=True)

plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='Q')).count()
h.rename(columns={'date': 'embeds'}, inplace=True)
h.plot(kind='bar', ax=ax)
new_ticks = []
for dt in h.index:
    new_ticks.append(dt.to_datetime())
ax.set_xticklabels([dt.strftime('%Y-%m-%d') for dt in new_ticks])
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(movie_request_time), data_type=data_product))
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
title = '{:s} daily embeds requested'.format(application)
plt.close('all')
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='D')).count()
h.rename(columns={'date': 'embeds'}, inplace=True)

movies_per_day = np.asarray(list(h["embeds"]))
mean = np.int(np.rint(np.mean(movies_per_day)))
median = np.int(np.rint(np.median(movies_per_day)))
h.plot(kind='line', ax=ax)
ax.axhline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
ax.axhline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(movie_request_time), data_type=data_product))
ax.set_xlabel('date')
ylim_max = 1.1*np.max(movies_per_day)
ax.set_ylim(0, ylim_max)
# Project events
for event in ('bigbreak',):
    ax.fill_betweenx((0, ylim_max),
                     parse_time(hvos.hv_project_dates[event]["date_start"]),
                     parse_time(hvos.hv_project_dates[event]["date_end"]),
                     **hvos.hv_project_dates[event]["kwargs"])

# Solar physics events
for event in ("comet_ison", "flare_flurry2017"):
    ax.axvline(parse_time(hvos.solar_physics_events[event]["date"]),
               **hvos.solar_physics_events[event]["kwargs"])
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.9, facecolor='y')
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, title))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 8
# Distribution of the number of embeds made per day
title = 'distribution of number of {{{:s}}} per day'.format(data_analyzed)
plt.close('all')
plt.hist(movies_per_day, bins=60, label='embeds')
plt.axvline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
plt.axvline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
plt.yscale('log')
plt.xlabel('number of embeds per day')
plt.ylabel(hvos.mlabel(len(movies_per_day), data_type='days'))
#plt.ylabel('number of days\n[{{{:n}}} total]'.format(len(movies_per_day)))
plt.title('{{{:s}}}\n[{{{:n}}} total]'.format(title, np.sum(movies_per_day)))
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.2)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'histogram_per_day'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

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

# application
application = 'helioviewer.org'
# application = 'JHelioviewer'

if application == 'helioviewer.org':
    application_short = 'hvorg'
if application == 'JHelioviewer':
    application_short = 'jhv'

# data product
data_product = 'movies'

# Event annotation style
edit = 1

# restriction = 'positive requested duration'
restriction = 'observable'

# How to calculate the topicality
topicality_calculated_using = 'movie_end_time'

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output location
img = os.path.join(os.path.expanduser(hvos.img), application)

# Type of data we are looking at
data_analyzed = '{:s} {:s}'.format(application, data_product)
data_type = '{:s} ({:s})'.format(data_analyzed, restriction)

# How much time did the movie cover?
f = os.path.join(directory, "hvorg_movie_durations_seconds.npy")
movie_durations = np.load(f)
durations_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmduration'][0], hvos.dates['Tmend'], hvos.dates['Tmstart'])

# Save the time information
f = os.path.join(directory, 'hvorg_movie_mid_point_seconds.npy')
movie_mid_point = np.load(f)

# Time difference
f = os.path.join(directory, 'hvorg_movie_time_difference_seconds.npy')
time_difference = np.load(f)

# Movie start times
f = os.path.join(directory, "hvorg_movie_start_time.pkl")
movie_start_time = pickle.load(open(f, 'rb'))
movie_start_time_date = hvos.dates['Tmstart']

# Movie end times
f = os.path.join(directory, "hvorg_movie_end_time.pkl")
movie_end_time = pickle.load(open(f, 'rb'))
movie_end_time_date = hvos.dates['Tmend']

# Movie request times
f = os.path.join(directory, "hvorg_movie_request_time.pkl")
movie_request_time = pickle.load(open(f, 'rb'))

# Number of movies
nmovies = len(movie_start_time)

# Topicality - calculate the time difference between the time of the request and the movie start time.
if topicality_calculated_using == 'movie_end_time':
    topicality = np.asarray([(movie_request_time[i] - movie_end_time[i]).total_seconds() for i in range(0, nmovies)])
    topicality_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmtopicality'][0], hvos.dates['Tmrequest'], movie_end_time_date)

if topicality_calculated_using == 'movie_start_time':
    topicality = np.asarray([(movie_request_time[i] - movie_start_time[i]).total_seconds() for i in range(0, nmovies)])
    topicality_subtitle = "{:s} = {:s} - {:s}".format(hvos.durations['tmtopicality'][0], hvos.dates['Tmrequest'], movie_start_time_date)

# Calculate the time difference between the time of the request and the movie end time.  Positive values
# indicate that the time the request was made was definitely after the movie end time.
proximity_to_real_time = np.asarray([(movie_request_time[i] - movie_end_time[i]).total_seconds() for i in range(0, nmovies)])


# Estimated maximum movie durations
estimated_maximum_duration = []
for i in range(0, nmovies):
    if movie_request_time[i] < movie_end_time[i]:
        estimated_maximum_duration.append((movie_request_time[i] - movie_start_time[i]).total_seconds())
    else:
        estimated_maximum_duration.append((movie_end_time[i] - movie_start_time[i]).total_seconds())
estimated_maximum_duration = np.asarray(estimated_maximum_duration)

# The movie has a non-zero duration
positive_duration = movie_durations > 0

# It was physically possible that we had data for the entire request?
physically_possible = proximity_to_real_time > 0

# What kind of restrictions can we put on the times
if restriction == 'observable':
    data_observable = np.logical_and(positive_duration, physically_possible)

if restriction == 'positive requested duration':
    data_observable = deepcopy(positive_duration)

# Positive and negative topicality needs its own exploration.
# Figure 2a: positive and negative topicality
td = topicality * u.s
td_short_unit = u.day
td_short_fraction = 24*4
td_short_limit = 8 * u.day
td_short = td[np.abs(td) < td_short_limit]
topicality_subtitle = "{:s} = {:s} - {:s}, $\mid${:s}$\mid$".format(hvos.durations['tmtopicality'][0], hvos.dates['Tmrequest'], movie_end_time_date,hvos.durations['tmtopicality'][0])
plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
plt.hist(td_short.to(td_short_unit).value, bins=int(td_short_limit.to(td_short_unit).value*td_short_fraction))
ax.grid(True, linestyle='dotted')
rl = hvos.relevant_lines(hvos.lines, tr=[0, td_short_limit.to(u.day).value]*u.day)
for key in list(rl.keys()):
    kwargs = rl[key]
    kwargs['label'] = str(key)
    plt.axvline(key.to(td_short_unit).value, **kwargs)
plt.yscale('log')
plt.xlabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(td_short_unit)))
plt.ylabel(hvos.mlabel(len(td_short)))
plt.title('{{{:s}}}\n{{{:s}}} {{{:s}}} {{{:s}}}'.format(data_analyzed, topicality_subtitle, "$\le$", td_short_limit))
plt.xlim(-td_short_limit.to(u.day).value, td_short_limit.to(u.day).value)
plt.legend()
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'topicality_positive_negative'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

# Restrict the movies we will look at.
td = topicality[data_observable]
md = movie_durations[data_observable]

# How many good movies?
ngood = len(td)

# Apply units - makes handling time durations much easier.
td = td * u.s
md = md * u.s


# Scatter plot of time difference versus movie duration
md_scatter_unit = u.day
td_scatter_unit = u.day
plt.close('all')
fig = plt.figure()
ax = fig.add_subplot(111)
md_value = md.to(md_scatter_unit).value
td_value = td.to(td_scatter_unit).value
plt.scatter(md_value, td_value, s=1)
plt.yscale('log')
plt.xscale('log')
mtd_min = np.min([md.to(md_scatter_unit).min().value, md.to(md_scatter_unit).min().value])
mtd_max = np.max([md.to(md_scatter_unit).max().value, md.to(md_scatter_unit).max().value])
plt.plot([mtd_min, mtd_max], [mtd_min, mtd_max], color='k', label='equality')

for line in list(hvos.lines.keys()):
    kwargs = hvos.lines[line]
    plt.axvline(line.to(md_scatter_unit).value, **kwargs)
for line in list(hvos.lines.keys()):
    kwargs = hvos.lines[line]
    plt.axhline(line.to(md_scatter_unit).value, label=str(line), **kwargs)

plt.xlabel(hvos.qlabel(hvos.durations['tmduration'][1], hvos.durations['tmduration'][0], str(md_scatter_unit)))
plt.ylabel(hvos.qlabel(hvos.durations['tmtopicality'][1], hvos.durations['tmtopicality'][0], str(td_scatter_unit)))
plt.legend()
plt.title(data_type + '\n' + '{{{:s}}} total'.format(str(len(md))))
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'scatter_duration_vs_topicality'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 1 : topicality
topicality_unit = u.year
overall_td_bins = 100
plt.close('all')
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
plt.close('all')
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
plt.close('all')
fig = plt.figure(figsize=figsize)
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
    plt.close('all')
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


# Figure 6
# Number of requests as a function of time
title = 'movies per quarter'
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
title = 'daily movies requested ({{{:s}}})'.format(hvos.quantity['hvm'])
plt.close('all')
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot(111)
h = df.groupby(pd.TimeGrouper(freq='D')).count()
h.rename(columns={'date': 'movies'}, inplace=True)

movies_per_day = np.asarray(list(h["movies"]))
mean = np.int(np.rint(np.mean(movies_per_day)))
median = np.int(np.rint(np.median(movies_per_day)))
h.plot(kind='line', ax=ax)
subtitle = '({{{:s}}} - {{{:s}}})'.format(str(h.index.min().to_pydatetime().date()), str(h.index.max().to_pydatetime().date()))
ax.axhline(mean, color='r', linestyle='dashed', label='mean ({{{:n}}})'.format(mean))
ax.axhline(median, color='k', linestyle='dashed', label='median ({{{:n}}})'.format(median))
ax.set_title(title)
ax.set_ylabel(hvos.mlabel(len(movie_request_time)))
ax.set_xlabel('date\n{{{:s}}}'.format(subtitle))
ylim_max = 1.1*np.max(movies_per_day)
ax.set_ylim(0, ylim_max)
# Project events
for event in ('repair', 'bigbreak', "shutdown2013"):
    ax.fill_betweenx((0, ylim_max),
                     parse_time(hvos.hv_project_dates[event]["date_start"]),
                     parse_time(hvos.hv_project_dates[event]["date_end"]),
                     **hvos.hv_project_dates[event]["kwargs"])


for i, event in enumerate(("hvorg3",)):
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
        if event == "june7_event":
            y = 1.25*y
        if y <= 0.1 * max(h[data_product]):
            y = (0.2 + i*0.2) * max(h[data_product])
        plt.axvline(t, color='r', linestyle=":", linewidth=0.5)
        plt.text(t, y, this_event["label"], **this_event["kwargs_text"])




plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.8, facecolor='y', fontsize=9)
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
plt.xlabel('number of movies per day ({{{:s}}})'.format(hvos.quantity['hvm']))
plt.ylabel('number of days\n[{{{:n}}} total]'.format(len(movies_per_day)))
plt.title('{{{:s}}}\n[{{{:n}}} total]'.format(title, np.sum(movies_per_day)))
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.2)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'histogram_number_of_movies_per_day'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

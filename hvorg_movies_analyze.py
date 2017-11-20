#
# Analysis of the hvorg_movies
#

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import hvorg_style as hvos
plt.rc('text', usetex=True)
plt.rc('font', size=14)

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output
img = hvos.img

data_type = 'helioviewer.org movies'

# How much time did the movie cover?
f = os.path.join(directory, "movie_durations.npy")
movie_durations = np.load(f)
durations_subtitle = "{:s}={:s}-{:s}".format(hvos.durations['tmduration'], hvos.dates['Tmend'], hvos.dates['Tmstart'])

# Movie start times
f = os.path.join(directory, "movie_start_time.pkl")
movie_start_time = pickle.load(open(f, 'rb'))
movie_start_time_date = hvos.dates['Tmstart']

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
topicality_subtitle = "{:s}={:s}-{:s}".format(hvos.durations['tmtopicality'], hvos.dates['Tmrequest'], movie_start_time_date)

# near_real_time - calculate the time difference between the time of the request and the
# movie end time.
near_real_time = np.asarray([(request_time[i] - movie_end_time[i]).total_seconds() for i in range(0, nmovies)])

# The movie has a non-zero duration
positive_duration = topicality > 0

# It was physically possible that we had data for the entire request
physically_possible = near_real_time >= 0

# These movies had data which we could have had
data_observable = np.logical_and(positive_duration, physically_possible)

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
plt.xlabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmtopicality'], str(topicality_unit)))
plt.ylabel('number of movies\n({{{:s}}} total)'.format(str(len(td))))
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
plt.xlabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmtopicality'], str(td_short_unit)))
plt.ylabel('number of movies\n({{{:s}}} total)'.format(str(len(td_short))))
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
plt.xlabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmduration'], str(md_unit)))
plt.ylabel('number of movies\n({{{:s}}} total)'.format(str(len(md))))
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
    plt.xlabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmduration'], str(md_short_unit)))
    plt.ylabel('number of movies\n({{{:s}}} total)'.format(str(len(md_short))))
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
"""
plt.axvline((1*u.hour).to(md_scatter_unit).value, color='r', linestyle='dotted', label='1 hour')
plt.axvline((3*u.hour).to(md_scatter_unit).value, color='k', linestyle='dotted', label='3 hours')
plt.axvline((6*u.hour).to(md_scatter_unit).value, color='orange', linestyle='dotted', label='6 hours')
plt.axvline((1*u.day).to(md_scatter_unit).value, color='r', linestyle='dashed', label='1 day')
plt.axvline((7*u.day).to(md_scatter_unit).value, color='k', linestyle='dashed', label='1 week')
plt.axvline((28*u.day).to(md_scatter_unit).value, color='orange', linestyle='dashed', label='28 days')
plt.axvline((365*u.day).to(md_scatter_unit).value, color='orange', linestyle='solid', label='365 days')

plt.axhline((1*u.hour).to(md_scatter_unit).value, color='r', linestyle='dotted')
plt.axhline((3*u.hour).to(md_scatter_unit).value, color='k', linestyle='dotted')
plt.axhline((6*u.hour).to(md_scatter_unit).value, color='orange', linestyle='dotted')
plt.axhline((1*u.day).to(md_scatter_unit).value, color='r', linestyle='dashed')
plt.axhline((7*u.day).to(md_scatter_unit).value, color='k', linestyle='dashed')
plt.axhline((28*u.day).to(md_scatter_unit).value, color='orange', linestyle='dashed')
plt.axhline((365*u.day).to(md_scatter_unit).value, color='orange', linestyle='solid')
"""
plt.xlabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmduration'], str(md_scatter_unit)))
plt.ylabel('{{{:s}}} ({{{:s}}})'.format(hvos.durations['tmtopicality'], str(td_scatter_unit)))
plt.legend()
plt.title(data_type)
plt.tight_layout()
filename = hvos.overleaf(os.path.join(data_type, 'scatter_duration_vs_topicality'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Figure 6
# Do some analysis on the choice of data sources.


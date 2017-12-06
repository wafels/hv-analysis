#
# Analysis of the timestamps of all service requests
#

import os
import pickle
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sunpy.time import parse_time
from scipy.stats import spearmanr

import hvorg_style as hvos
plt.rc('text', usetex=True)
plt.rc('font', size=14)
figsize = (10, 5)

# application
application = 'service_comparison'
# application = 'JHelioviewer'

if application == 'helioviewer.org':
    application_short = 'hvorg'
if application == 'JHelioviewer':
    application_short = 'jhv'

# services
services = ["helioviewer.org movie", "helioviewer.org embed", "JHelioviewer movie"]

filenames = {"helioviewer.org movie": "hvorg_movie_request_time.pkl",
             "helioviewer.org embed": "hvorg_embed_request_timestamps_only.pkl",
             "JHelioviewer movie": "jhv_movie_request_timestamps_only.pkl"}

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output location
img = os.path.join(os.path.expanduser(hvos.img), application)

# Service request times
service_request_time = dict()
for service in services:
    f = os.path.join(directory, filenames[service])
    service_request_time[service] = sorted(pickle.load(open(f, 'rb')))

# Find the start and end times within which all services exist
start_time = parse_time('1976-01-02')
end_time = parse_time('2976-01-02')
for service in services:
    if service_request_time[service][0] > start_time:
        start_time = service_request_time[service][0]
    if service_request_time[service][-1] < end_time:
        end_time = service_request_time[service][-1]

# Figure 7
# Daily numbers as a plot
for i, service in enumerate(services):
    these_times = service_request_time[service]
    df = pd.DataFrame(these_times, columns=['date'])

    # Setting the date as the index since the TimeGrouper works on Index, the date column is not dropped to be able to
    # count
    df.set_index('date', drop=False, inplace=True)

    h = df[(df.index >= start_time) & (df.index <= end_time)].groupby(pd.TimeGrouper(freq='D')).count()
    h.rename(columns={'date': service}, inplace=True)

    if i == 0:
        dfz = deepcopy(h)
    else:
        dfz[service] = pd.Series(h[service].values, index=dfz.index)

total_daily_service_requests = dfz.sum(axis=1)

s0 = np.zeros(len(total_daily_service_requests))
s1 = dfz["helioviewer.org movie"].values / total_daily_service_requests.values
s2 = (dfz["helioviewer.org movie"].values + dfz["helioviewer.org embed"].values) / total_daily_service_requests.values
s3 = np.ones(len(total_daily_service_requests))
x = total_daily_service_requests.index.to_pydatetime()

f_denominator = '{{{:s}}}+{{{:s}}}+{{{:s}}}'.format(hvos.quantity["hvm"], hvos.quantity["hve"], hvos.quantity["jhvm"])
f_hvm = '{{{:s}}}/({{{:s}}})'.format(hvos.quantity["hvm"], f_denominator)
f_jhvm = '{{{:s}}}/({{{:s}}})'.format(hvos.quantity["jhvm"], f_denominator)
f_hve = '{{{:s}}}/({{{:s}}})'.format(hvos.quantity["hve"], f_denominator)


plt.close('all')
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.fill_between(x, s0, s1, label='helioviewer.org movie requests\n{{{:s}}}'.format(f_hvm))
ax.fill_between(x, s1, s2, label='helioviewer.org embed requests\n{{{:s}}}'.format(f_hve))
ax.fill_between(x, s2, s3, label='JHelioviewer movie requests\n{{{:s}}}'.format(f_jhvm))
ax.set_title("service usage expressed as fraction of total daily usage")
ax.set_ylabel("fractional use")
subtitle = '{{{:s}}} - {{{:s}}}'.format(str(start_time.date()), str(end_time.date()))
ax.set_xlabel('date\n({{{:s}}})'.format(subtitle))
ax.set_ylim(0, 1.1)
# Project events
for event in ('bigbreak', 'shutdown2013'):
    ax.fill_betweenx((0, 1.1),
                     parse_time(hvos.hv_project_dates[event]["date_start"]),
                     parse_time(hvos.hv_project_dates[event]["date_end"]),
                     **hvos.hv_project_dates[event]["kwargs"])

for event in ("hvorg3", "newjhv"):
    ax.axvline(parse_time(hvos.hv_project_dates[event]["date"]),
               **hvos.hv_project_dates[event]["kwargs"])

# Solar physics events
for event in ("comet_ison", "flare_flurry2017"):
    ax.axvline(parse_time(hvos.solar_physics_events[event]["date"]),
               **hvos.solar_physics_events[event]["kwargs"])
plt.grid('on', linestyle='dotted')
plt.legend(fontsize=8, framealpha=0.4, facecolor='y', loc='upper left')
plt.tight_layout()
filename = hvos.overleaf(os.path.join('fractional_service_usage'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Cross correlation - movies
plt.close('all')

down_time = '2015-07-01'

dfz_before_down_time = dfz[(dfz.index < down_time)]
xb = dfz_before_down_time["helioviewer.org movie"].values
yb = dfz_before_down_time["JHelioviewer movie"].values

ge1 = np.logical_and(xb >= 1, yb >= 1)

polyfit_xb = np.log10(xb[ge1])
polyfit_yb = np.log10(yb[ge1])
polyfit = np.polyfit(polyfit_xb, polyfit_yb, 1)
xbp = np.arange(0, 4.0, 0.001)
ybp = 10.0**np.polyval(polyfit, xbp)
fit_string = '{{{:s}}}$=$ {{{:.2f}}} {{{:s}}}$^{{{:.2f}}}$'.format(hvos.quantity["jhvm"], 10.0**polyfit[1], hvos.quantity["hvm"], polyfit[0])

cc = spearmanr(polyfit_xb, polyfit_yb)
ss_string = '{:.2f}'.format(cc.correlation)
pv_string = '{:.2f}'.format(cc.pvalue)
spearman_string = 'Spearman $\\rho$={{{:s}}} ({{{:s}}})'.format(ss_string, pv_string)

dfz_after_down_time = dfz[(dfz.index >= down_time)]
xa = dfz_after_down_time["helioviewer.org movie"].values
ya = dfz_after_down_time["JHelioviewer movie"].values

scatter_size = 1.5
after_scatter_color = 'm'
after_scatter_marker = 's'

label = 'before {{{:s}}} '.format(down_time) + hvos.tlabel(len(xb), suffix='days')
plt.scatter(xb, yb, s=scatter_size, label=label)
label = 'after {{{:s}}} '.format(down_time) + hvos.tlabel(len(xa), suffix='days')
plt.scatter(xa, ya, s=scatter_size, color=after_scatter_color,  marker=after_scatter_marker, label=label)
plt.plot(10**xbp, ybp, color='k', label='best fit (before {{{:s}}})\n{{{:s}}}\n{{{:s}}}'.format(down_time, spearman_string, fit_string))
plt.plot([1, 10000], [1, 10000], linestyle=':', color='k', label='equality')
plt.yscale('log')
plt.xscale('log')
plt.xlim(1, 10000)
plt.ylim(1, 10000)
xlabel = 'helioviewer.org movies, daily usage ({{{:s}}})'.format(hvos.quantity["hvm"])
plt.xlabel(xlabel)
ylabel = 'JHelioviewer movies, daily usage ({{{:s}}})'.format(hvos.quantity["jhvm"])
plt.ylabel(ylabel)
title = 'service usage correlation\n{{{:s}}}\nhelioviewer.org movies vs JHelioviewer movies'.format(subtitle)
plt.title(title)
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.3, fontsize=10, facecolor='y')
plt.tight_layout()
filename = hvos.overleaf(os.path.join('scatter_hvorg_movies_vs_jhv_movies'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)


# Cross correlation - movies
plt.close('all')

down_time = '2015-07-01'

dfz_before_down_time = dfz[(dfz.index < down_time)]
xb = dfz_before_down_time["helioviewer.org movie"].values
yb = dfz_before_down_time["helioviewer.org embed"].values

label = 'before {{{:s}}} '.format(down_time) + hvos.tlabel(len(xb), suffix='days')
plt.scatter(xb, yb, s=scatter_size, label=label)

dfz_after_down_time = dfz[(dfz.index >= down_time)]
xa = dfz_after_down_time["helioviewer.org movie"].values
ya = dfz_after_down_time["helioviewer.org embed"].values
label = 'after {{{:s}}} '.format(down_time) + hvos.tlabel(len(xa), suffix='days')
plt.scatter(xa, ya, s=scatter_size, color=after_scatter_color, marker=after_scatter_marker, label=label)


plt.yscale('log')
plt.xscale('log')
plt.xlim(1, 10000)
plt.ylim(1, 10000)
xlabel = 'helioviewer.org movies, daily usage ({{{:s}}})'.format(hvos.quantity["hvm"])
plt.xlabel(xlabel)
ylabel = 'helioviewer embeds, daily usage ({{{:s}}})'.format(hvos.quantity["hve"])
plt.ylabel(ylabel)
title = 'service usage correlation\n{{{:s}}}\nhelioviewer.org movies vs helioviewer.org embeds'.format(subtitle)
plt.title(title)
plt.grid('on', linestyle='dotted')
plt.legend(framealpha=0.3, facecolor='y', fontsize=10)
plt.tight_layout()
filename = hvos.overleaf(os.path.join('scatter_hvorg_movies_vs_hvorg_embeds'))
filename = '{:s}.{:s}'.format(filename, hvos.imgfiletype)
filepath = os.path.join(img, filename)
plt.savefig(filepath)

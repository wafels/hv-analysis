#
# Styles and constants used in the HV analysis
#
import re
import os
from copy import deepcopy
from collections import OrderedDict
import astropy.units as u

# Where to save the images
img = os.path.expanduser('~/hvp/hv-analysis/img')
imgfiletype = 'png'

# Times we are interested in
d = {1*u.hour: {"linestyle": "dotted", "color": "r"},
     3*u.hour: {"linestyle": "dotted", "color": "k"},
     6*u.hour: {"linestyle": "dotted", "color": "orange"},
     1*u.day: {"linestyle": "dashed", "color": "r"},
     7*u.day: {"linestyle": "dashed", "color": "k"},
     28*u.day: {"linestyle": "dashed", "color": "orange"},
     365*u.day: {"linestyle": "solid", "color": "orange"}
     }

# LaTeX description of dates and durations
dates = {"Tmrequest": "$T_{request}$",
         "Tmstart": "$T_{start}$",
         "Tmend": "$T_{end}$",
         "Tmmidpoint": "$T_{midpoint}$"}

durations = {"tmduration": ["$t_{duration}$", "requested duration"],
             "tmtopicality": ["$t_{topicality}$", "requested topicality"]}


# Helioviewer Project Dates
hv_project_dates = {"hv_bigbreak_start": {"date": "2015-07-09 00:00:00", "kwargs": {"linestyle": "solid", "color": "k"}},
                    "hv_bigbreak_end": {"date": "2015-10-01 00:00:00", "kwargs": {"linestyle": "dashed", "color": "k"}},
                    "hv_version3_launch": {"date": "2016-03-29 00:00:00", "kwargs": {"linestyle": "dotted", "color": "k"}},
                    "hv_smallbreak_start": {"date": "2015-07-09 00:00:00", "kwargs": {"linestyle": "solid", "color": "k"}},
                    "hv_smallbreak_end": {"date": "2015-10-01 00:00:00", "kwargs": {"linestyle": "dashed", "color": "k"}},
                    }

# Solar physics events
solar_physics_events = {"june7_event": {"date": "2011-06-07 06:30:00",
                                        "kwargs": {"label": "June 7 2011 failed eruption", "linestyle": "solid", "color": "r"}},
                        "tse2017": {"date": "2017-08-21 00:00:00",
                                    "kwargs": {"label": "total solar eclipse", "linestyle": "dashed", "color": "r"}},
                        "transit_of_venus": {"date": "2012-06-06 00:00:00",
                                             "kwargs": {"label": "transit of Venus", "linestyle": "dot-dashed", "color": "r"}},
                        "comet_ison": {"date": "2013-11-28 00:00:00",
                                       "kwargs": {"label": "Comet ISON", "linestyle": "dot-dashed", "color": "g"}}
                        }



# Order the dictionary according to the keys
def order_dictionary(this_d):
    return OrderedDict(sorted(this_d.items(), key=lambda t: t[0]))


# Find the relevant lines with the range tr
def relevant_lines(this_d, tr=[0.0, 1.0]*u.day):
    rl = {}
    keys = list(this_d.keys())
    for key in keys:
        if tr[0] <= key <= tr[1]:
            rl[key] = deepcopy(this_d[key])
    return order_dictionary(rl)


# Number of movies label
def mlabel(n, brackets='[]'):
    return "number of movies\n{{{:s}}}{{{:s}}} total{{{:s}}}".format(brackets[0], str(n), brackets[1])


# Quantity label
def qlabel(a, b, c):
    return '{{{:s}}} ({{{:s}}}) [{{{:s}}}]'.format(a, b, c)


# Clean a filename for use with Overleaf
def overleaf(s, rule='\W+', rep='_'):
    return re.sub(rule, rep, s)


lines = order_dictionary(d)

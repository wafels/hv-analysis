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
         "Tmmidpoint": "$T_{midpoint}$",
         "Tsdate": "$T_{obs}$"}

durations = {"tmduration": ["$t_{duration}$", "requested duration"],
             "tmtopicality": ["$t_{topicality}$", "requested topicality"]}

# Quantities
quantity = {"hvm": "$n_{hv}$", "jhvm": "$n_{jhv}$",
            "hve": "$m_{hv}$"}


# Helioviewer Project Dates
hv_project_dates = {"bigbreak": {"date_start": "2015-02-04 00:00:00",
                                 "date_end": "2015-09-23 00:00:00",
                                 "kwargs": {"facecolor": 'r',
                                            "label": 'GSFC server down',
                                            "alpha": 0.2
                                            }
                                 },
                    "repair": {"date_start": "2011-08-11 00:00:00",
                               "date_end": "2011-09-18 00:00:00",
                               "kwargs": {"facecolor": 'k',
                                          "label": 'GSFC server repair',
                                          "alpha": 0.2
                                          }
                               },
                    "hvorg3": {"date": "2016-03-29 00:00:00",
                               "kwargs": {"color": 'k',
                                          "label": 'helioviewer.org 3.0 released'
                                          }
                               },
                    "newjhv": {"date": "2016-03-31 00:00:00",
                               "kwargs": {"color": 'k',
                                          "linestyle": "-.",
                                          "label": 'JHelioviewer 2.10 released'
                                          }
                               }
                    }


# Solar physics events
solar_physics_events = {"june7_event": {"date": "2011-06-07 06:30:00",
                                        "kwargs": {"label": "failed eruption (2011/06/07)", "linestyle": "solid", "color": "r"}},
                        "tse2017": {"date": "2017-08-21 00:00:00",
                                    "kwargs": {"label": "total solar eclipse", "linestyle": "--", "color": "r"}},
                        "transit_of_venus": {"date": "2012-06-06 00:00:00",
                                             "kwargs": {"label": "transit of Venus", "linestyle": "-.", "color": "r"}},
                        "comet_ison": {"date": "2013-11-28 00:00:00",
                                       "kwargs": {"label": "Comet ISON (2013/11/28)", "linestyle": "-.", "color": "m"}},
                        "flare_flurry2017": {"date": "2017-09-08 00:00:00",
                                             "kwargs": {"label": "large flares (2017/09/6-10)", "linestyle": "--", "color": "m"}}
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
def mlabel(n, data_type='movies', brackets='[]'):
    return "number of {{{:s}}}\n{{{:s}}}{{{:s}}} total{{{:s}}}".format(data_type, brackets[0], str(n), brackets[1])


def tlabel(n, brackets='[]', suffix='total'):
    return "{{{:s}}}{{{:s}}} {{{:s}}}{{{:s}}}".format(brackets[0], str(n), suffix, brackets[1])


# Quantity label
def qlabel(a, b, c):
    return '{{{:s}}} ({{{:s}}}) [{{{:s}}}]'.format(a, b, c)


# Clean a filename for use with Overleaf
def overleaf(s, rule='\W+', rep='_'):
    return re.sub(rule, rep, s)


lines = order_dictionary(d)

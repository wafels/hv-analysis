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
                                            "label": 'GSFC server down (2015/02/04 - 2015/09/23)',
                                            "alpha": 0.2
                                            }
                                 },
                    "repair": {"date_start": "2011-08-11 00:00:00",
                               "date_end": "2011-09-18 00:00:00",
                               "kwargs": {"facecolor": 'k',
                                          "label": 'GSFC server repair (2011/08/11 - 2011/09/18)',
                                          "alpha": 0.2
                                          }
                               },
                    "shutdown2013": {"date_start": "2013-10-01 00:00:00",
                                     "date_end": "2013-10-16 00:00:00",
                                     "kwargs": {"facecolor": 'g',
                                                "label": 'U.S. Fed. Gov. shutdown (2013/10/01 - 2013/10/16)',
                                                "alpha": 0.4
                                                }
                               },
                    "hvorg3": {"date": "2016-03-29 00:00:00",
                               "label": 'HV.org 3.0 released\n(2016-03-29)',
                               "kwargs": {"color": 'k',
                                          "linewidth": 0.5
                                          },
                               "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                               "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                               }
                               },
                    "newjhv": {"date": "2016-03-31 00:00:00",
                               "label": 'JHV 2.10 released\n(2016-03-31)',
                               "kwargs": {"color": 'k',
                                          "linestyle": "-.",
                                          "linewidth": 0.5
                                          },
                               "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                               "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                               }
                               }
                    }


# Solar physics events
solar_physics_events = {"june7_event": {"date": "2011-06-07 06:30:00",
                                        "label": "failed eruption\n(2011/06/07)",
                                        "kwargs": {"linestyle": "solid",
                                                   "color": "r",
                                                   "linewidth": 0.5},
                                        "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                                        "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                                        }
                                        },
                        "tse2017": {"date": "2017-08-21 00:00:00",
                                    "label": "total solar eclipse",
                                    "kwargs": {"linestyle": "--",
                                               "color": "r",
                                               "linewidth": 0.5},
                                    "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                                    "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                                    }
                                    },
                        "transit_of_venus": {"date": "2012-06-06 00:00:00",
                                             "label": "transit of Venus",
                                             "kwargs": {"linestyle": "-.",
                                                        "color": "r",
                                                        "linewidth": 0.5},
                                             "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                                             "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                                             }
                                             },
                        "comet_ison": {"date": "2013-11-28 00:00:00",
                                       "label": "Comet ISON\n(2013/11/28)",
                                       "kwargs": {"linestyle": "-.",
                                                  "color": "m",
                                                  "linewidth": 0.5},
                                       "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                                       "fontsize": 9,
                                                       "horizontalalignment": 'center',
                                                       "zorder": 1000
                                                      }
                                       },
                        "flare_flurry2017": {"date": "2017-09-08 00:00:00",
                                             "label": "large flares\n(2017/09/6-10)",
                                             "kwargs": {"linestyle": "--",
                                                        "color": "m",
                                                        "linewidth": 0.5},
                                             "kwargs_text": {"bbox": dict(facecolor='yellow', alpha=0.5),
                                                             "fontsize": 9,
                                                        "horizontalalignment": 'center'
                                                             }
                                             }
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

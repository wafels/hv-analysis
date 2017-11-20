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
d = {1*u.hour: {"color": "k", "linestyle": "dotted", "color": "r"},
     3*u.hour: {"color": "k", "linestyle": "dotted", "color": "k"},
     6*u.hour: {"color": "k", "linestyle": "dotted", "color": "orange"},
     1*u.day: {"color": "k", "linestyle": "dashed", "color": "r"},
     7*u.day: {"color": "k", "linestyle": "dashed", "color": "k"},
     28*u.day: {"color": "k", "linestyle": "dashed", "color": "orange"},
     365*u.day: {"color": "k", "linestyle": "solid", "color": "orange"}
     }

# LaTeX description of dates and durations
dates = {"Tmrequest": "$T_{request}$",
         "Tmstart": "$T_{start}$",
         "Tmend": "$T_{end}$",
         "Tmidpoint": "$T_{midpoint}$"}

durations = {"tmduration": "$t_{duration}$",
             "tmtopicality": "$t_{topicality}$"}


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


# Clean a filename for use with Overleaf
def overleaf(s, rule='\W+', rep='_'):
    return re.sub(rule, rep, s)


lines = order_dictionary(d)

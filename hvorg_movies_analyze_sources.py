#
# Analysis of the hvorg_movies sources
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

restriction = 'observable'
#restriction = 'positive requested duration'

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Image output location
img = hvos.img

# application
application = 'helioviewer.org'

# data product
data_product = 'movies'

# Type of data we are looking at
data_analyzed = '{:s} {:s}'.format(application, data_product)
data_type = '{:s} ({:s})'.format(data_analyzed, restriction)

# Load in the sources file
f = os.path.join(directory, "hvorg_data_source_ids.csv")
sources_used = pd.read_csv(f)

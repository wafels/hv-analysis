#
# Analysis of the embed requests
#

import os
import pickle
import pandas as pd
from sunpy.time import parse_time


# Save the data
save_directory = os.path.expanduser('~/Data/hvanalysis/derived')

# Read in the data
directory = os.path.expanduser('~/Data/hvanalysis/source')
jhv_movies = 'embed.csv'
path = os.path.expanduser(os.path.join(directory, jhv_movies))
df = pd.read_csv(path)

data_type = 'Helioviewer.org embed'

# Get some figures of merit for the movies
# When was the movie requested?
print('Parsing embed times')
request_time = [parse_time(x) for x in df.timestamp.tolist()]

# Save the time information
f = os.path.join(save_directory, 'hvorg_embed_request_timestamps_only.pkl')
pickle.dump(request_time, open(f, 'wb'))

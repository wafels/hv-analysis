
# Make an UpSet plot of the data

# Load in the library
library(UpSetR)

# Where is the data?
filepath = "/home/ireland/Data/hvanalysis/derived/jhv_data_source_ids.csv"

# Read in the CSV file
sourcesused <- read.csv(file=filepath, header=TRUE, sep=",")

# Save the output as a TIFF image
png(filename="/home/ireland/hvp/hv-analysis/img/jhv_movies_data_sources.png", width=1500, height=750)

# Create the UpSet plot
upset(sourcesused, text.scale=2, nsets=10, order.by="freq", number.angle=10, scale.intersections='log10')

# Close the output device
dev.off()

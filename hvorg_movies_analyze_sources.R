
# Make an UpSet plot of the data

# Load in the library
library(UpSetR)

# Where is the data?
filepath = "/home/ireland/Data/hvanalysis/derived/hvorg_data_source_ids.csv"

# Read in the CSV file
sourcesused <- read.csv(file=filepath, header=TRUE, sep=",")

# Save the output as a TIFF image
tiff(filename="/home/ireland/Desktop/nnn.tiff", width=1500, height=500)

# Create the UpSet plot
upset(sourcesused, text.scale=2, nsets=10, order.by="freq", number.angle=10, scale.intersections='log10')

# Close the output device
dev.off()

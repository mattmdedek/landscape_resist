# TO-DO: figure out how to recover from missing vegan gracefully...
# These commands install it:
# Install/update dependancy lattice
# install.package("lattice")
# Install the vegan package
# install.packages("vegan")

# vegan... we has it
library(vegan)

# We have three input files for a partial mantel test:
# 1 - genetic distance, loaded as geneDistTxt etc
# 2 - geometric (euclidean) distance loaded as physDistTxt etc
# 3 - resistance 'distance' loaded as resistTxt etc

# get the input files from the command line
args <- commandArgs(trailingOnly = T)

if (length(args) < 3) {
  stop('Provide three files: genetic distance, geometric distance, resistance matrix, and number of permutations')
} else {
  geneDistPath <- args[1]
  physDistPath <- args[2]
  resistPath   <- args[3]
  perms        <- args[4]
}

# read files into strings
# size is the number of characters in the file
geneDistTxt <- readChar(geneDistPath, file.info(geneDistPath)$size)
physDistTxt <- readChar(physDistPath, file.info(physDistPath)$size)
resistTxt <- readChar(resistPath, file.info(resistPath)$size)

# read strings into matrices
# strings contained in files should already be symetric matrices with the same 
# number of rows and columns and with the rows and columns representing the same
# individuals
slopedmat <- data.matrix(read.table(text=slopetxt, fill=T, sep="\t", header=F))

mantel(as.dist(eucdmat), as.dist(rousdmat), method="pearson", permutations=99)

mantel.partial(as.dist(rousdmat), as.dist(slopedmat), as.dist(eucdmat), method="pearson", permutations=9999)


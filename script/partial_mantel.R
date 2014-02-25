# TO-DO: figure out how to recover from missing vegan gracefully...
# These commands install it:
# Install/update dependancy lattice
# install.package("lattice")
# Install the vegan package
# install.packages("vegan")

# vegan... we has it
library(vegan)

# We have three input files for a partial mantel test:
# 1 - genetic distance, loaded as gen_dist_fp etc
# 2 - geometric (euclidean) distance loaded as euc_dist_fp etc
# 3 - resistance 'distance' loaded as res_dist_fp etc
# All of these files are already tab-delimited symetric diagonal matrices
# the sample represented by the nth column is the same as the sample
# represented by the nth row.

# get the input files from the command line
args <- commandArgs(trailingOnly = T)

if (length(args) < 3) {
  stop('Provide three files: genetic distance, geometric distance, resistance matrix, and number of permutations')
} else {
  gen_dist_fp <- args[1]
  euc_dist_fp <- args[2]
  res_fp      <- args[3]
  perms       <- args[4]
}

# read files into strings
# size is the number of characters in the file
gen_dist_ft <- readChar(gen_dist_fp, file.info(gen_dist_fp)$size)
euc_dist_ft <- readChar(euc_dist_fp, file.info(euc_dist_fp)$size)
res_ft <- readChar(res_fp, file.info(res_fp)$size)

# read strings into matrices
gen_mat <- data.matrix(read.table(text=gen_dist_ft, fill=F, sep="\t", header=F))
euc_mat <- data.matrix(read.table(text=euc_dist_ft, fill=F, sep="\t", header=F))
res_mat <- data.matrix(read.table(text=res_ft, fill=F, sep="\t", header=F))

mantel.partial(as.dist(gen_mat), as.dist(res_mat), as.dist(euc_mat), method="pearson", permutations=perms)


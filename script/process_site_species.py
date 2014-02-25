#!/usr/bin/python

import ls_transforms
import glob
import os
import sys
import re

# take a species and a directory and run the mantel analyses

# get the site and species to process from the arguments
site = ''
species = ''
if len(sys.argv) < 3:
    print "Usage: site, species"
else:
    site = sys.argv[1].upper()
    species = sys.argv[2]upper()

# set up data locations
out_dir = '../results/' + site + '/' + species + '/'
in_dir = '../data/sites/' + site + '/' + species + '/'
sample_map = '../data/samples/sample_array.txt'
array_map = in_dir + 'Array_ID_' + site + '.txt'

# create the file tranforming object
try:
    sm = ls_transformers.sample_mapper(sample_map, array_map)
except Exception e:
    print e
    exit()

# find genetic and euclidean distance files
gen_fp = in_dir + site.lower() + '_' + species.lower() + '_rousset.txt'
euc_fp = in_dir + 'PairwiseEuclideanDistance_' + species.lower() + '.txt'

# glob for a list of resistance files
res_fps = glob.glob(in_dir + site.lower() + '*resistances_3columns')

# build the output directory tree
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# clean the output directory
for f in os.listdir(out_dir):
    fp = os.path.join(out_dir, f)
    try:
        if os.path.isfile(fp):
             os.unlink(fp)
    except Exception, e:
        print e

# start analyzing
compiled_mantel = []
compiled_partial = []

# process euclidean and genetic distances
gen_matrix_fp = out_dir + site.lower() + '_' + species.lower() + '_rousset.txt'
sample_list = lt.genetic_to_matrix_file(gen_fp, gen_matrix_fp)
print "Loaded genetic distance file: " + gen_fp

euc_matrix_fp = out_dir + 'PairwiseEuclideanDistance_' + species.lower() + '.txt'
lt.euclid_to_matrix_file(euc_fp, euc_matrix_fp, sample_list)
print "Loaded Euclidean distance file: " + gen_fp

for res_fp in res_fps:
    res_fn = os.path.basename(res_fp)
    res_matrix_fp = out_dir + res_fn
    fn_toks = res_fn.split('_')
    print "Processing resistance file: " + res_fp
    mantel_out_fp = out_dir + res_fn + "_mantel"
    partial_out_fp = out_dir + res_fn + "_partial"
    lt.resist_to_matrix_file(res_fn, res_matrix_fp, sample_list) 


import glob
import os

# For all of the data file lookup functions, the data_dir
# will default to the spec, but can be set to an alternate
# location for testing.
# This feature is provided for testing, where the data_dir
# directory is configured to mirror the ../data directory

def get_dist_metric_path(site, metric, spec, cost, data_dir = '../data/'):
    base_path = ( data_dir.rstrip('/\\') + '/sites/' + site + '/' +
                  '_'.join([site, metric, spec, cost]) )
    try:
        return 'columnar', _safe_data_path(base_path + '_resistances_3columns')
    except ConfigFileMissingError:
        return 'matrix', _safe_data_path(base_path + '_resistances')

def get_dist_path(site, metric = "euclidean", data_dir = '../data/'):
    return 'matrix', _safe_data_path(data_dir.rstrip('/\\') + '/sites/' + metric + '.txt')

def get_gdist_path(site, species, metric = "rousset", data_dir = '../data/'):
    return 'matrix', ( _safe_data_path(
                         data_dir.rstrip('/\\') + 
                         '/samples/genetic_dist/' +
                         '_'.join([site, species, metric]) + '.txt'
                     ) )

def _safe_data_path(fname):
    if os.path.isfile(fname):
        return fname       
    else:
        raise ConfigFileMissingError, ( fname + ' not found' )

def sample_arrays_to_dict(map_path = "../data/samples/sample_arrays.txt"):
    """
    Read the sample mapping file to map samples to collection sites.

    Input file format: Tab-delimited, columns SampleID, FieldSiteID, ArrayID
    Header line optional.

    Function returns a dictionary of dictionaries.
    Top level key is the SampleID.
    Second level keys are SampleID, FieldSiteID and ArrayID
    """
    if not os.path.isfile(map_path):
        raise ConfigFileMissingError, map_path + " not found"
    
    mapping_dict = {}
    expected_header = "sampleid\tfieldsiteid\tarrayid"
    line_no = 0

    with open(map_path, 'r') as map_file:
        for line in map_file:
            line_no += 1
            if line_no == 1 and line.strip().lower() == expected_header:
                continue
            else:
                ltoks = line.strip().split("\t")
                if len(ltoks) >= 3:
                    this_dict = {"SampleID": ltoks[0], "FieldSiteID": ltoks[1], "ArrayID": ltoks[2]}
                    if ltoks[0] in mapping_dict:
                        raise DuplicateConfigKeyError, (
                              "Sample " + ltoks[0] + " specified for two sites: " +
                              str(mapping_dict[ltoks[0]]) + " and " + str(this_dict) )
                    else:
                        mapping_dict[ltoks[0]] = this_dict

    map_file.close()
    return mapping_dict

class ConfigFileMissingError(RuntimeError):
    """A data file is missing"""
    pass

class DuplicateConfigKeyError(RuntimeError):
    """A key which was expected to be unique was specified twice"""
    pass


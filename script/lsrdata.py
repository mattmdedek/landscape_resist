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

class ConfigFileMissingError(RuntimeError):
    """A data file is missing"""
    pass


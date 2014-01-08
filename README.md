landscape_resist
================

Purpose:
--------

To automate distance models for landscape genetic studies.

We will start this project with support for Mantel and Partial Mantel
tests using the Vegan R package with distance matrices computed by 
Circuitscape.

Configuration Files:
--------------------

1.  Raw data is stored in the data directory with one sub directory 
    per field site.
2.  A mapping file is required to map collections to collection arrays and
    field sites. This mapping file is stored in data/sample_arrays.txt.
    data/sample_arrays.txt is tab-delimited with three columns:
    * Column 1: SampleID - The sample identifier
    * Column 2: FieldSiteID - The field site identifier, matches sub-
      directories of data/sites
    * Column 3: ArrayID - The collection array identifier
3. When generating Circuitscape data, each position (corresponding to a 
   collection array in this context) is assigned a numeric ID. We need to
   map the numeric ID to the FieldSiteID.

   Therefore, each field site's sub-directory of data/sites must contain 
   a mapping file array_ids.txt that maps this numeric ID to a collection
   array ID string. The file is tab-delimited with two columns:
   * Column 1: NumericID
   * Column 2: FieldSiteID

Array Distance Files:
----------------

1.  The array distance files are saved in the field site sub-directories
    of data/sites.
2.  Each field site sub-directory is named by the field site identifier.
    This identifier must match the FieldSiteID listed in the
    configuration files.
3.  The individual distance files conform to the following naming
    convention:
    * *FieldSiteID*_*metric*_*type*_*cost*[_resistances_3columns].txt




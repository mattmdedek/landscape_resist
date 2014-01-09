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

1.  Site distance data is stored in the data directory with one sub
    directory per field site.

2.  Genetic distance data is stored by species

3.  A mapping file is required to map collections to collection arrays and
    field sites. This mapping file is stored in data/sample_arrays.txt.
    data/sample_arrays.txt is tab-delimited with three columns:

    * Column 1: SampleID - The sample identifier
    * Column 2: FieldSiteID - The field site identifier, matches sub-
      directories of data/sites
    * Column 3: ArrayID - The collection array identifier

4. When generating Circuitscape data, each position (corresponding to a 
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

      FieldSiteID_Metric_MetricSpec_Cost[_resistances_3columns].txt

    * Underscores are not not allowed in any of the name tokens
    * the resistances_3columns substring is automatically appended by
      Circuitscape and is allowed as a convenience.
    * Numeric ranges (perhaps in the Cost token) may be specified 
      by 0.001-0.01 or by 0p001-0p01, replacing the period with a p.

4.  These file names will be used to find inputs for batch tests and
    to generate reports, so please adhere to the standard.


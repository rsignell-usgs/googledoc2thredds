googledoc2thredds
=================

Use information in a Google Doc spreadsheet to create a THREDDS catalog.  This technique was used by the IOOS Modeling Testbed to allow modelers to "register" their new datasets in the catalog.  The procedure was this:

Modelers would upload their data to the testbed server, which usually consisted of a collection of non-standards-compliant NetCDF files.  They would also supply a NcML file (NetCDF Markup Language) which both aggregated data data and made the resulting aggregation CF-Compliant.   This NcML was usually based only on the conventions used by each modeling group for their output files, and thus could often be used simply as a template that was copied from one run to the next.   

The modeler would edit the Google Doc, adding a line to specify the unique characteristics of the run, as well as to specify the location of the NcML file.  Often this also could just be copied from the preceding line and a few items change. 

The googledoc2catalog.py script would run each hour in a cronjob, generating new thredds catalogs.  Changes in conventions could also be handled by modifying this script.

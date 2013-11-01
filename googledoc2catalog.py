#!/usr/bin/env python
import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import re, os
import datasetXML
import string

# Connect to Google
gd_client = gdata.spreadsheet.service.SpreadsheetsService() # acrosy
#ourkey = "0AnjRO6UoIcT5dFRtdXh1ejRQNkdMSG5EeVFNZ1ZYNVE" # acrosby
gd_client.email = 'rsignell@yahoo.com'
gd_client.password = 'sura_ftp'
gd_client.source = 'SURA Model Extractor'
gd_client.ProgrammaticLogin()

#Now that we're connected, we query the spreadsheet by name, and extract the unique spreadsheet and worksheet IDs.
q = gdata.spreadsheet.service.DocumentQuery()
q['title'] = "NOAA IOOS Testbed - Inundation Inventory"
q['title-exact'] = 'true'
feed = gd_client.GetSpreadsheetsFeed(query=q)

# Make sure we got a single match on the spreadsheet name
if len(feed.entry) > 0:
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    
    # Models (Worksheet 0)
    # worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    
    # Runs (Worksheet 1)
    worksheet_id = feed.entry[1].id.text.rsplit('/',1)[1]
    
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    
    # we now have a row iterator which will yield rows for the Google spreadsheet. 
    
    # read header for Inundation THREDDS Catalog
    f = open('/home/tomcat/python/inundation_header.xml','r')
    header = f.read()
    f.close() 
    
    # read footer for Inundation THREDDS Catalog
    f = open('/home/tomcat/python/inundation_footer.xml','r')
    footer = f.read()
    f.close()
    
    # read imeds obs xml and add to catalog
    f = open('/var/www/tomcat-threddsdev/content/thredds/inundation_imeds.xml', 'r')
    obs = f.read()
    f.close()

    catalog = header + obs
    
    # Loop through rows of Google Doc, pulling the NcML location, 
    # the unique dataset identifier, and the descriptive dataset name
    
    for row in rows:
        dir = row.custom['locationofncmlonsuraserver'].text
        #print dir
        if dir is not None:
            id = row.custom['uniquerunidentifier'].text
            #ncmlFile = dir + '/00_dir.ncml'
            ncmlFile = dir 
            print ncmlFile
            urlPath = string.replace(id,'.','/')
            datasetName = row.custom['runtitle'].text
            runSummary = row.custom['runsummary'].text
            #print row.customdocs
            coveragetype = row.custom['coveragecontenttype'].text
            coveragevars = row.custom['variablesofinterestforcoveragetype'].text
            cdmdatatype = row.custom['cdmtype'].text
            xml = datasetXML.datasetXML(ncmlFile, datasetName, runSummary, urlPath, id,
                                        coveragetype, coveragevars, cdmdatatype)
            catalog = catalog + xml
        
    catalog = (catalog + footer).encode('utf-8')
    f = open('/var/www/tomcat-threddsdev/content/thredds/inundation_googledoc.xml','w')
    f.write(catalog)
    f.close()
    os.system('touch /var/www/tomcat-threddsdev/webapps/thredds/WEB-INF/web.xml')
else:
    print '0 spreadsheets found for user ' + gd_client.email
    print 'Using query:'
    print q

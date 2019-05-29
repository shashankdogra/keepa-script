import os
import logging
import inspect
logging.basicConfig()
import requests
import numpy as np
import csv
import io
import ftplib
import glob
import pandas, sys
import pandas as pd
a = pd.read_csv("output1.csv")
b = pd.read_csv("output2.csv")
merged = pd.concat([a,b])
print '\nMerging Files\n'
print '....'
merged.to_csv("output.csv", index=False)
print 'Merge Successful'
#File transfer to the ftp initiated
print '\n\nNow uploading Files to the FTP'
print '...'
print '..'
print '.'

ftp = ftplib.FTP('ftp.altatac2.com', 'keepa@altatac2.com' , 'Keepa532')
ftp.cwd('/keepaoutput')
ftp.dir()
fp = open("output.csv", 'rb')
ftp.storbinary('STOR %s' % os.path.basename("output.csv"), fp, 1024)
fp.close()
print '\n\n ---------------------All Done. ------------------------'
import keepa
import logging
import inspect
logging.basicConfig()
import datetime
import requests
import numpy as np
import csv
import pandas
import io
import os
import ftplib
#Open ftp connection
ftp = ftplib.FTP('ftp.altatac2.com', 'keepa@altatac2.com' , 'Keepa532')
files = ftp.dir()
print files
ftp.cwd("/inputupcs")
gFile = open("upcs.csv", "wb")
ftp.retrbinary('RETR upcs.csv', gFile.write)
gFile.close()
ftp.quit()

#Print the readme file contents
print "\nFile Output:"
gFile = open("upcs.csv", "r")
buff = gFile.read()
print buff
gFile.close()
#Taking data from csv and turning into arrays of sku and upcs
data = csv.reader(open('upcs.csv', 'rb'), delimiter=",", quotechar='|')
sku, upc = [], []
for row in data:
    sku.append(row[0])
    upc.append(row[1])
print sku
print upc
# taking upc output and putting it into upcs without the column header
upcs = upc[1:]
skus = sku[1:]
print 'final list of upcs being sent to Keepa'
print upcs
for x in range(len(upcs)):
    print upcs[x]
# starting Keepa and passing UPC array into api query
accesskey = 'b9pms3n5aile7ihpmgvigtigf1cs2eu04ms13ikvbn92l9q559neucdidho9511f' # enter real access key here
api = keepa.Keepa(accesskey)
import os
if os.path.exists("output.csv"):
  os.remove("output.csv")
else:
  print("The file does not exist")
with open('output.csv', "w") as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(['SKU','UPC','ASIN','Title','No. of Offers','Current Sales Rank','Current Price'])
print 'Keepa Pull Initiated ...'
for x in range(len(upcs)):
    try:
        print '========================================================================================'
        print 'product Number:'
        print x
        print 'of'
        print len(upcs)
        print '\n'
        products = api.query(upcs[x], product_code_is_asin=False, offers=100)
        upc_value = upcs[x]
        sku_value = skus[x]
        print upc_value
        print '\n'
        print sku_value
        print '\n'
        product = products[0]
        offers = product['offers']
        offer = offers[0]
        csv = offer['offerCSV']
        # printing the sales rank
        key = 'SALES'
        history = product['data']
        #print key
        sales_dt = history['%s_time' % key]
        sales = history[key]
        #PRINT ASIN
        print('ASIN is ' + products[0]['asin'].encode("utf-8"))
        asin_value = products[0]['asin'].encode("utf-8")
        print asin_value
        #Print Title
        print ('Title is ' + products[0]['title'].encode("utf-8"))
        title_value = products[0]['title'].encode("utf-8")
        #print history[key][-1]
        print ('Sales Rank is: ')
        print sales[-1]
        salesrank_value = sales[-1]
        print ('Number of Offers: ')
        try:
            print len(product['liveOffersOrder'])
            noOfOffers_value = len(product['liveOffersOrder'])
        except:
            print 'No Offers'
            noOfOffers_value = 'No Offers'
        #Current best buy box price
        newprice = product['data']['BUY_BOX_SHIPPING']
        print '\n BuyBox Price is:'
        print  newprice[-1]
        current_price = newprice[-1]
        print '========================================================================================'
    except:
        pass

    del csv
    import csv
    with open('output.csv', "a") as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', lineterminator='\n')
            try:
              output_writer.writerow([sku_value,upc_value,asin_value,title_value,noOfOffers_value,salesrank_value,current_price])
            except:
              pass  
#File transfer to the ftp initiated
ftp = ftplib.FTP('ftp.altatac2.com', 'keepa@altatac2.com' , 'Keepa532')
ftp.cwd('/keepaoutput')
ftp.dir()
fp = open("output.csv", 'rb')
ftp.storbinary('STOR %s' % os.path.basename("output.csv"), fp, 1024)
fp.close()

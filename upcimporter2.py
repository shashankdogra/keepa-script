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
print (files)
ftp.cwd("/inputupcs")
gFile = open("upcs.csv", "wb")
ftp.retrbinary('RETR upcs.csv', gFile.write)
gFile.close()
ftp.quit()

#Print the file contents
print ("\nFile Output: ")
gFile = open("upcs.csv", "r")
buff = gFile.read()
#print buff
gFile.close()
#Taking data from csv and turning into arrays of sku and upcs
data = csv.reader(open('upcs.csv', 'rb'), delimiter=",", quotechar='|')
sku, upc = [], []
for row in data:
    sku.append(row[0])
    upc.append(row[1])
# taking upc output and putting it into upcs without the column header
upcs = upc[1:]
upcs1 = upcs[:len(upcs)//2]
upcs2 = upcs[len(upcs)//2:]
skus = sku[1:]
skus1 = skus[:len(skus)//2]
skus2 = skus[len(skus)//2:]

#===========================================================================
# DEBUGGING PRINT STATEMENTS - Remove/ Comment after Finalizing the scripts
print ('Length of UPC segment 1:\t\t' + str(len(upcs1)))
print ('Length of SKU segment 1:\t\t' + str(len(skus1)))
print ('Length of UPC segment 2:\t\t' + str(len(upcs2)))
print ('Length of SKU segment 2:\t\t' + str(len(skus2)))

print "\nFirst Half: \n"

for x in range(len(upcs1)):
    print str(x) + '\t' + str(upcs1[x]) + '\t' + str(skus1[x])
print "\nSecond Half: \n"
for x in range(len(upcs2)):
    print str(x) + '\t' + str(upcs2[x]) + '\t' + str(skus2[x])
# End of DEBUGGING PRINT STATEMENTS for the INPUT LIST
#===========================================================================


# starting Keepa and passing UPC array into api query
accesskey = 'b9pms3n5aile7ihpmgvigtigf1cs2eu04ms13ikvbn92l9q559neucdidho9511f' # enter real access key here
api = keepa.Keepa(accesskey)
if os.path.exists("output2.csv"):
  os.remove("output2.csv")
else:
  print("The file does not exist")
with open('output2.csv', "w") as output_file:
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            output_writer.writerow(['SKU','UPC','ASIN','Title','Description','Bullet Point 1','Bullet Point 2','Bullet Point 3','Bullet Point 4','Bullet Point 5','color','size','Current Sales Rank','Current Price','Average 30','Average 90','Average 180','Category','Category 2','Item Type','FBA Fee Total in $','KeepaCategoryPath'])
print 'Keepa Pull Initiated ...'
asin_value = 'Empty'
title_value = 'Empty'
noOfOffers_value = 'Empty'
salesrank_value = 'Empty'
current_price = 'Empty'
n = len(upcs1)
for x in range(len(upcs2)):
#for x in range(10):

  upc_value = upcs2[x]
  sku_value = skus2[x]
  asin_value = 'Empty'
  title_value = 'Empty'
  noOfOffers_value = 'Not Pulling'
  salesrank_value = 'Empty'
  current_price = 'Empty'
  category_value = 'Empty'
  category2_value = 'Empty'
  itemType_value = 'Empty'
  FBAFeeInDollars = 'Empty'
  BuyBoxPriceCurrent = 'NotAvailable'
  BuyBoxAverage30 = 'NotAvailable'
  BuyBoxAverage90 = 'NotAvailable'
  BuyBoxAverage180 = 'NotAvailable'
  KeepaCategoryPath = 'NotAvailable'
  description = 'NotAvailable'
  bulletpoint1 = 'NotAvailable'
  bulletpoint2 = 'NotAvailable'
  bulletpoint3 = 'NotAvailable'
  bulletpoint4 = 'NotAvailable'
  bulletpoint5 = 'NotAvailable'
  color = ''
  size = ''

  print '====================================== Script 2 ============================================='
  print 'Product Number:\t ' + str(n + x) + " / " + str(n + len(upcs2))
  print '------------------------------'
  print '\n'
  products = api.query(upcs2[x], product_code_is_asin=False, offers=100, stats=90, history=0, rating=1)
  print '\n'
  print ('UPC is: \t' + upc_value)
  print ('SKU is: \t' + sku_value)
  try:
    product = products[0]
    offers = product['offers']
    stats = product['stats']
    categoryTree = product['categoryTree']
    fbafee = product['fbaFees']
    bulletpoints = product['features']
  except:
    product = None
    offers = None
    stats = None
    categoryTree = None
    fbafee = None
    bulletpoints = None
  #PRINT ASIN
  try:
    asin_value = products[0]['asin'].encode("utf-8")
    print('ASIN is: \t' + asin_value)
  except:
    print('No ASIN Value Found')
    asin_value = 'NotAvailable'
      
          
  #Print Title
  try:
    title_value = products[0]['title'].encode("utf-8")
    print ('Title is: \t' + title_value)
  except:
    print 'No Title Found'
    title_value = 'NotAvailable'
    print '\n'

      
  # Printing The Product Description
  try:
    print 'Description:\n'
    description = products[0]['description'].encode("utf-8")
    print description
    print '\n'
  except:
    print 'No Desc Found'
    description = 'NotAvailable'
    print '\n'

  # Print Color and Size
  try:
    color = products[0]['color']
    print 'color:\t' + str(color)
  except:
    print 'No Color Found'
    color = 'NotAvailable'
    print '\n'

  try:
    size = products[0]['size']
    print 'size:\t' + str(size)
  except:
    size = 'NotAvailable'
    print 'No Size Found\n'

    # Print Sales Rank

  try:
    currentRank = stats['current'][3]
  except:
    salesrank_value = 0
    print 'No Sales Rank Found\n'
  else:
      if currentRank == -1:
        salesrank_value = 0
        print salesrank_value
      else:
        print ('Current Rank:\t\t\t' + str(currentRank))
        salesrank_value = str(currentRank)

      
  #print ('Number of Offers: ')
  #try:
  #    print len(product['liveOffersOrder'])
  #    noOfOffers_value = len(product['liveOffersOrder'])
  #except:
  #    print 'No Offers'
  #    noOfOffers_value = 'No Offers'
  #Current best buy box price
  #newprice = product['data']['BUY_BOX_SHIPPING']
  #current_price = newprice[-1]
  #print ('BuyBox Price is:' + str(current_price))

  #Printing Current BuyBox Price
  try:
    currentPrice = stats['current'][18]
    BuyBoxPriceCurrent = str(currentPrice/100.00)
    print ('Current Price:\t\t\t' + BuyBoxPriceCurrent)
    
  except:
    BuyBoxPriceCurrent = ''
    print ('Current Price:\t\t' + 'Not available')
    

  try:    
    average30 = stats['avg30'][18]
    BuyBoxAverage30 = str(average30/100.00)
    print ('Average Price 30 days:\t\t' + BuyBoxAverage30)
    
  except:
    BuyBoxAverage30 = 'NotAvailable'
    print ('Average Price 30 days:\t\t' + 'Not Available')
    
  try:
    average90 = stats['avg90'][18]
    BuyBoxAverage90 = str(average90/100.00)  
    print ('Average Price 90 days:\t\t' + BuyBoxAverage90)
    
  except:
    BuyBoxAverage90 = 'NotAvailable'  
    print ('Average Price 90 days:\t\t' + BuyBoxAverage90)
    

  try:    
    average180 = stats['avg180'][18]
    BuyBoxAverage180 = str(average180/100.00)
    print ('Average Price 180 days:\t\t' + BuyBoxAverage180)
    
  except:
    BuyBoxAverage180 = 'NotAvailable'
    print ('Average Price 180 days:\t\t' + BuyBoxAverage180)

  try:
    # Printing the FBA Fee
    a = fbafee['storageFee']/100.00
    b = fbafee['storageFeeTax']/100.00
    c = fbafee['pickAndPackFee']/100.00
    d = fbafee['pickAndPackFeeTax']/100.00
    FBAFeeSum = a + b + c + d
    FBAFeeInDollars = FBAFeeSum
    print ('FBA Fee in Dollar:\t' + str(FBAFeeInDollars))
    print '\n'
  except:
    FBAFeeInDollars = 'NotAvailable'
    print ('FBA Fee in Dollar:\t' + FBAFeeInDollars)
    print '\n'




  #PRINT Category and Fee

  try:
    category_value = categoryTree[0]['name']
    print ('Category:\t' + category_value)
  except:
    category_value = 'NotAvailable'
    print ('Category:\t' + category_value)
  try: 
    category2_value = categoryTree[1]['name']
    print ('Category 2:\t' + category2_value)
  except:
    category2_value = 'NotAvailable'
    print ('Category:\t' + category2_value)

  try:
    itemType_value = categoryTree[-1]['name']
    print ('Item Type:\t' + itemType_value)
  except:
    itemType_value = 'NotAvailable'
    print ('Item Type:\t' + itemType_value)

  KeepaCategoryPath = category_value + '|' + category2_value + '|' + itemType_value
  print 'Complete Path:\t' + KeepaCategoryPath 




  # Printing out all the Bullet Points
  print 'Bullet Points: \n'
  #for x in range(len(bulletpoints)):
  #    print str(x+1) + '-\t' + bulletpoints[x]
  try:    
    bulletpoint1 = bulletpoints[0].encode("utf-8")
    print ('1:-\t\t' + bulletpoint1)
  except:
    bulletpoint1 = 'NotAvailable'
    print ('1:-\t\t' + 'NotAvailable')
  try:  
    bulletpoint2 = bulletpoints[1].encode("utf-8")
    print ('2:-\t\t' + bulletpoint2)
  except:
    bulletpoint2 = 'NotAvailable'
    print ('2:-\t\t' + 'NotAvailable')
  try:
    bulletpoint3 = bulletpoints[2].encode("utf-8")
    print ('3:-\t\t' + bulletpoint3)
  except:
    bulletpoint3 = 'NotAvailable'
    print ('3:-\t\t' + 'NotAvailable')

  try:
    bulletpoint4 = bulletpoints[3].encode("utf-8")
    print ('4:-\t\t' + bulletpoint4)
  except:
    bulletpoint4 = 'NotAvailable'
    print ('4:-\t\t' + 'NotAvailable')
  try:
    bulletpoint5 = bulletpoints[4].encode("utf-8")
    print ('5:-\t\t' + bulletpoint5)
  except:
    bulletpoint5 = 'NotAvailable'
    print ('5:-\t\t' + 'NotAvailable')
  print '========================================================================================'

  del csv
  import csv
  with open('output2.csv', "a") as output_file:
          output_writer = csv.writer(output_file, delimiter=',', quotechar='"', lineterminator='\n')
          try:
            output_writer.writerow([sku_value,upc_value,asin_value,title_value,description,bulletpoint1,bulletpoint2,bulletpoint3,bulletpoint4,bulletpoint5,color,size,salesrank_value,BuyBoxPriceCurrent, BuyBoxAverage30,BuyBoxAverage90,BuyBoxAverage180,category_value,category2_value,itemType_value,FBAFeeInDollars,KeepaCategoryPath])
          except:
            #pass
            output_writer.writerow([sku_value,upc_value,"No ASIN FOUND","No TITLE FOUND","No Desc","No BP1","No BP2","No BP3","No BP4","No BP5",'','',"No Sales Rank","No Price","No 30 avg Price","No 90 Price","No 180 Price","No Category Found","No Category2 Found","No Item Type Found", "No FBA Fee Found","No Path Found"])  
print '\nEnd of Script 2\n'
import keepa
import logging
import inspect
logging.basicConfig()
import datetime
import requests
import numpy as np
accesskey = 'b9pms3n5aile7ihpmgvigtigf1cs2eu04ms13ikvbn92l9q559neucdidho9511f' # enter real access key here
api = keepa.Keepa(accesskey)
asins = ['B01N5ML1EA', 'B00THPUHPM', 'B01M8IKE7Y', 'B01IQCN744']
asins = np.asarray(['B01N5ML1EA', 'B00THPUHPM', 'B01M8IKE7Y', 'B01IQCN744'])
products = api.query(asins)
product = products[0]

for x in range(len(asins)):
    print('ASIN is ' + products[x]['asin'])
    print ('Title is ' + products[x]['title'])

# printing the sales rank
key = 'SALES'
history = product['data']
#print key
sales_dt = history['%s_time' % key]
sales = history[key]

print history[key][-1]


'''
# Print ASIN and title
print('ASIN is ' + products[0]['asin'])
print('Title is ' + products[0]['title'])

product['stats']
# Access new price history and associated time data
newprice = product['data']['NEW']
newpricetime = product['data']['NEW_time']


# print the first 10 prices
print('%20s   %s' % ('Date', 'Price'))
for i in range(10):
    print('%20s   $%.2f' % (newpricetime[i], newprice[i]))
    '''

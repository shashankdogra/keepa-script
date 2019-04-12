import keepa
import logging
import inspect
logging.basicConfig()
import datetime
import requests
import numpy as np
accesskey = 'xxx' # <-- replace xxx with your keepa api access key
api = keepa.Keepa(accesskey)

'''
You can query using ISBN-10 or ASIN like the above example by default, or by using UPC,
EAN, and ISBN-13 codes by setting product_code_is_asin to False:

products = api.query('978-0786222728', product_code_is_asin=False)

'''

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

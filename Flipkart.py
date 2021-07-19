import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
search=input('Enter product you want to search for : ')
r = requests.get('https://www.flipkart.com/search?q='+search, headers=headers)#, proxies=proxies)
content = r.content
soup = BeautifulSoup(content)
#print(soup)

allproducts = []
for d in soup.findAll('div',attrs={'class':'_1AtVbE'}):
  #print(d)
  product=[]
  pdata=d.find('div',attrs={'data-id':True})
  price=d.find('div',attrs={'class':'_30jeq3'})
  if pdata is not None:
   if price is not None and pdata['data-id'] is not None:
    price=price.text
    plink=pdata.find('a',attrs={'href':True})
    pname=plink['href'].split("/")
    price = price.replace('₹', '')
    price = price.replace(',', '')
    product.append(pname[1])
    product.append(price)
    plink='www.flipkart.com'+plink['href']
    product.append(plink)
    allproducts.append(product)
df = pd.DataFrame(allproducts,columns=(['Title'],['Price'],['link']))#,['price']))
df.to_csv('products.csv', index=False, encoding='utf-8')
for x in range(len(allproducts)):
  print(allproducts[x])

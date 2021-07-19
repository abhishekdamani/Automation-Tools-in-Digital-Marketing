import cgi,cgitb
from bs4 import BeautifulSoup
import requests
form=cgi.FieldStorage()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
#search=input('Enter product you want to search for : ')
#search = search.replace(' ','+')
search=form.getvalue('p_search')
print("<script>console.log('Search received : "+search+"')</script>")
r = requests.get('https://www.amazon.in/s?k='+search, headers=headers)#, proxies=proxies)
content = r.content
soup = BeautifulSoup(content)
#print(soup)
amzn_products=[]
for pdata in soup.findAll('div',attrs={'data-asin':True}) :
    product=[]
    price=pdata.find("span", attrs={"class":'a-price-whole'})
    title=pdata.find("span", attrs={"class": lambda L: L and L.endswith('a-color-base a-text-normal')})
    if(price is not None and title is not None):
     pimg=pdata.find_all('img')
     price_value = price.text
     price_string = price_value.strip()
     title_value = title.text
     title_string = title_value
     link=pdata.find('a',attrs={"class":'a-link-normal a-text-normal'})
     product.append(title_string)
     product.append(price_string)
     product.append("https://amazon.in/"+link['href'])
     product.append(pimg[0]['src'])
     amzn_products.append(product)
if not amzn_products:
      print('''<div class="col-xl-4 col-md-6 col-sm-6 col-xs-12"><div class="card prod-view"><img src="amazon.svg" class="text-center" style="height:50px;width:150px"/><div class="prod-item text-center"><div class="prod-img"><div class="option-hover"></div><img src="" class="hvr-shrink"></img></div><div class="prod-info"><a href="" class="txt-muted">Search is blocked by amazon. Please search again!<h4></h4></a><div class="m-b-10"><label class="label label-success"></label></div><span class="prod-price"><span></div></div></div></div>''')
else:
    print('''<div class="col-xl-4 col-md-6 col-sm-6 col-xs-12"><div class="card prod-view"><img src="amazon.svg" class="text-center" style="height:50px;width:150px"/><div class="prod-item text-center"><div class="prod-img"><div class="option-hover"></div><img src="''',amzn_products[0][3],'''" class="hvr-shrink"></img></div><div class="prod-info"><a href="''',amzn_products[0][2],'''" class="txt-muted"><h4>''',amzn_products[0][0],'''</h4></a><div class="m-b-10"><label class="label label-success"></label></div><span class="prod-price">''',amzn_products[0][1],'''<i class="fa fa-inr"></i><span></div></div></div></div>''')

r = requests.get('https://www.flipkart.com/search?q='+search, headers=headers)#, proxies=proxies)
content = r.content
soup = BeautifulSoup(content)
#print(soup)

fkrt_products = []
for d in soup.findAll('div',attrs={'class':'_1AtVbE'}):
  #print(d)
  product=[]
  pdata=d.find('div',attrs={'data-id':True})
  price=d.find('div',attrs={'class':'_30jeq3'})
  if pdata is not None:
   if price is not None and pdata['data-id'] is not None:
    price=price.text
    pimg=pdata.find_all('img')
    plink=pdata.find('a',attrs={'href':True})
    pname=plink['href'].split("/")
    price = price.replace('₹', '')
    price = price.replace(',', '')

    product.append(pname[1])
    product.append(price)
    plink='www.flipkart.com'+plink['href']
    product.append(plink)
    product.append(pimg[0]['src'])
   fkrt_products.append(product)
print('''<div class="col-xl-4 col-md-6 col-sm-6 col-xs-12"><div class="card prod-view"><img src="flipkart.svg" class="text-center" style="height:50px;width:150px"/><div class="prod-item text-center"><div class="prod-img"><div class="option-hover"></div><img src="''',fkrt_products[0][3],'''" class="hvr-shrink"></img></div><div class="prod-info"><a href="''',fkrt_products[0][2],'''" class="txt-muted"><h4>''',fkrt_products[0][0],'''</h4></a><div class="m-b-10"><label class="label label-success"></label></div><span class="prod-price">''',fkrt_products[0][1],'''<i class="fa fa-inr"></i><span></div></div></div></div>''')

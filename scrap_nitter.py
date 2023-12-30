'''
    MIT LICENSE 
    Application Scrap Nitter
    By Fajrul Iqbal
    
'''
import requests
from bs4 import BeautifulSoup
import csv
import sys

''' 
    Utility :
    Contains red_code and reset_code
    is code ANSI to draw I/O to color red
    
'''
# Code ANSI to draw color res
red_code = '\033[91m'
# The End Teks Have drawed Color
reset_code = '\033[0m'


#  User Input
print(red_code+'\nAPPLICATION SCRAP NITTER\nExample Input That Correct => \nSearch: pelayanan kesehatan\nDate from: 2023-12-01\nDate till: 2023-12-31\n'+reset_code)
user_input_search = input('Search: ')
user_input_search = user_input_search.replace(' ', '+')
user_input_date_from = input('Date from: ')
user_input_date_till = input('Date till: ')
print('\n')

# Pool Request
pool_req= ['nitter.moomoo.me' ,'nitter.unixfox.eu', 
           'nitter.esmailelbob.xyz', 'nitter.poast.org' , 
           'nitter.cz', 'nitter.privacydev.net', 
           'nitter.projectsegfau.lt', 
           'nitter.eu.projectsegfau.lt', 
           'nitter.in.projectsegfau.lt', 
           'nitter.us.projectsegfau.lt', 
           'nitter.rawbit.ninja', 
           'nitter.d420.de', 
           'bird.habedieeh.re', 
           'nitter.tux.pizza', 
           'nitter.x86-64-unknown-linux-gnu.zip', 
           'nitter.woodland.cafe', 
           'nitter.dafriser.be', 
           'nitter.catsarch.com', 
           'nitter.perennialte.ch', 
           'nitter.salastil.com', 
           'n.populas.no', 
           'nt.ggtyler.dev', 
           'nitter.uni-sonia.com', 
           'n.opnxng.com', 
           'nitter.ktachibana.party', 
           'nitter.tinfoil-hat.net', 
           'nitter.jakefrosty.com', 
           'nitter.manasiwibi.com']


#  Scrap Beutiuful Soap
quotes = []  # a list to store quotes
uri ='?f=tweets&q='+user_input_search+'&since='+user_input_date_from+'&until='+user_input_date_till+'&near='
i  = 0
while True :
    r = 0
    try:
        URL = "https://"+pool_req[i]+"/search"+ uri
        r = requests.get(URL)
        while r.status_code != 200 :
            i = i +1
            if  i >= len(pool_req):
              sys.exit()
            URL = "https://"+pool_req[i]+"/search"+ uri
            r = requests.get(URL)
        
        if r.status_code != 200:
            print('This Server Error or Request Error')
            sys.exit()
    except requests.exceptions.RequestException as e:
        if i >= len(pool_req)-1:
          print('Connection Lost')
          sys.exit()
        print('Waitttt ..... ')
        i = i +1
        continue 
    
    soup = BeautifulSoup(r.content, 'html5lib')
    b = soup.findAll('div', class_ = 'show-more')
    
    t = 0 
    for c in b:  
        if "/search" in c.a['href']:
          continue
        else :
          uri= c.a['href']
          print(uri)  # Page 
          t =t+1 
    if t == 0:
        break
          
    timeline = soup.find('div', attrs={'class' : 'timeline'})
    tables = timeline.findAll('div' , attrs= {'class' : 'tweet-body'})

    for row in tables:
        quote = {}
        quote['name']  = row.find('a',attrs ={'class' : 'fullname'}).text
        quote['username']  = row.find('a',attrs ={'class' : 'username'}).text
        quote['image'] = 'https://'+pool_req[i]+row.img['src']
        quote['date'] = row.find('span' , attrs = {'class' : 'tweet-date'}).a['title']
        quote['desc'] = row.find('div' , attrs = {'class' : 'tweet-content media-body'}).text
        quotes.append(quote)
     

if len(quotes)  ==  0:
  print("There's Not Data")
  sys.exit()
# Generate csv
filename = user_input_search+'.csv'
with open(filename, 'w', newline='', encoding="utf-8") as f:
    w = csv.DictWriter(f, ['name','username', 'image', 'date','desc'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)


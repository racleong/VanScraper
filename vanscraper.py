from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import sqlite3

conn = sqlite3.connect('vantest.db')
c = conn.cursor()

#c.execute('''CREATE TABLE vans(title TEXT, price TEXT, spec TEXT, link TEXT)''')
baseurl = 'https://www.autotrader.co.uk'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"
    }


vans = []

def webscrape():
    for page in range(1, 10):
        fuel_type = 'Petrol'
        distance = 40
        r = requests.get(f'https://www.autotrader.co.uk/van-search?sort=relevance&postcode=ig26sl&radius={distance}&include-delivery-option=on&fuel-type={fuel_type}&page={page}', headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        #print(r.status_code)

        vanlist = soup.find_all('li', class_='search-page__result')
        
        for van in vanlist:
            for link in van.find_all('a', class_='js-click-handler listing-fpa-link tracking-standard-link', href=True):
                
                van_title = van.find('h3', class_='product-card-details__title').text.strip()
                van_price = van.find('div', class_='product-card-pricing__price').text.strip()
                van_specs = van.find('p', class_='product-card-details__subtitle').text.strip()
                van_link = baseurl + link['href']
                van = {
                'name': van_title,
                'price': van_price,
                'specs': van_specs,
                'link': van_link
                }
                c.execute('''INSERT INTO vans VALUES(?,?,?,?)''', (van['name'], van['price'], van['specs'], van['link']))

                vans.append(van)
                print('Saving: ', van['name'])
webscrape()                
conn.commit()
print('complete')

#c.execute('''SELECT * FROM vans''')
#results = c.fetchall()
#print(results))

df = pd.read_sql_query("SELECT * FROM vans", conn)
print(df)

conn.close()


import requests
from bs4 import BeautifulSoup
import csv


URL='https://auto.ria.com/car/hyundai/'
HEADERS ={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.228 (Edition Yx 02)', 'accept':'*/*' }
FILE  ='cars.csv'



def get_html(url, params=None):
    r=requests.get(url,headers=HEADERS ,params=params)
    return r



def parse():
    html=get_html(URL)
    if html.status_code==200:
        print(html.text)
        cars = get_content(html.text)
    else:
        print('error ')
    save_file(cars, FILE)

def get_content(html):
    soup=BeautifulSoup(html , 'html.parser')
    items= soup.find_all('div' , class_='content-bar')
    cars=[]

    for i in items:
        uah_price=i.find('span',class_='i-block')
        if uah_price:
            uah_price = uah_price.get_text().replace('\xa0грн','')
        else:
            uah_price = 'Цену уточнняйте'
        cars.append({
            'title': i.find('div' , class_='item ticket-title').get_text(strip=True),
            'link': i.find('a', class_='m-link-ticket').get('href'),
            'usd_price': i.find('span',class_="bold green size22").get_text(),
            'uah_price': uah_price,
            'city': i.find('li', class_='item-char view-location').get_text()
        })
    return cars

def save_file(items,path):
    with open(path ,'w' , newline='') as file:
        writer=csv.writer(file ,delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в долларах', 'цена в гривнах', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['uah_price'], item['city']])




parse()

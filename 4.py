import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text


def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


link = 'https://tabiturient.ru/vuzu/mifi/'
site_name = get_html(link)
site_data = get_head(site_name)
head = site_data.find('div').find_all(style="text-align:justify;", class_='font2')
heads = []
for i in head:
    heads.append(i.string)
heads = [e for e in heads if e is not None]
print(*heads)


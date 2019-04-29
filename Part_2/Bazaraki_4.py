import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd




def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    dvs = soup.find('div', id='listing').find_all('div', class_='list-announcement-block')
    links = []
    # counter = 1

    for div in dvs:
        a = div.find('a').get('href')
        # links.append(str(counter) + ':')
        link = 'https://www.bazaraki.com' + a
        links.append(link)

        # counter += 1

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        client_id = soup.find('div', id='show-post-render-app').find('span', itemprop='sku').text.strip()
    except:
        client_id = ''

    try:
        client_price = soup.find('div', class_='announcement-price__cost _verified').text.strip()
    except:
        client_price = ''

    try:
        client_title = soup.find('div', class_='announcement-content-header').find('h1', class_="title-announcement").text.strip()
    except:
        client_title = ''

    data = {
        'client_id': client_id,
        'client_price': client_price,
        'client_title': client_title,
    }

    return data


def write_csv(data):
    with open('bazaraki.csv', 'a') as f:  # создание и запись в файл f
        writer = csv.writer(f)  # j

        writer.writerow((data['client_id'],
                         data['client_title'],
                         data['client_price']
                         ))

        print(data['client_id'], 'parsed')


def write_data_base(data):

        b = pd.Series(data)
        return b



def main():
    start = datetime.now()

    url = 'https://www.bazaraki.com/real-estate/houses-and-villas-sale/'
    all_links = get_all_links(get_html(url))
    from pprint import pprint
    pprint(all_links)

    print('start')

    i = 0
    while i < len(all_links)-1:  # пробегаю по всем полученным ссылкам

        link = all_links[i]  # получаю каждую отдельную ссылку из списка
        html = get_html(link)  # первожу этот тип данных в текст
        data = get_page_data(html)  # вытаскиваю данные
        #write_csv(data)  # пишу в файл
        print(i)
        print(write_data_base(data))
        i += 1


    end = datetime.now()

    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()

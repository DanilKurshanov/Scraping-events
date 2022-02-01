#pip install beautifulsoup4 lxml re
from bs4 import BeautifulSoup
import requests
import re
import datetime

def ticketscloud_place(url):

    events_list = []

    link = requests.get(url).text
    soup = BeautifulSoup(link, 'lxml')

    # scraping all events on web link
    all_events = soup.find('div', class_='u-flex u-flex--wrap').find_all('div', class_='ticketscloud-event-item col-md-4')

    # create dictionary for each event
    for item in all_events:

        title = item.find(class_='ticketscloud-event-item__title')
        href = url.split('?')[0][:-1] + item.find('a').get('href')
        time = datetime.datetime.strptime(item.find(class_='ticketscloud-event-item__time').text.replace(',', ''), "%d.%m.%Y %H:%M")
        city = item.find('span', class_=None)
        loc = item.find('span', itemprop="name")

        if item.find(class_='ticketscloud-event-item__ticket-price'):
            price = re.sub('\s+', ' ', item.find(class_='ticketscloud-event-item__ticket-price').find('b').text.strip())
        else:
            price = None

        events_list.append ({
            'event_title': title.text,
            'event_href': href,
            'event_time': time,
            'event_city': city.text,
            'event_loc': loc.text,
            'event_price': price,
        })

    return events_list

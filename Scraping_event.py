#pip install beautifulsoup4 lxml re
from bs4 import BeautifulSoup
import requests
import re

def ticketscloud_event(url):
    event_info = {}

    link = requests.get(url).text
    soup = BeautifulSoup(link, 'lxml')

    event_info['event_title'] = soup.find('div', class_='event-info-se__title').text.strip()
    event_info['event_price'] = re.sub('\s+', ' ', soup.find('div', class_='buy-button-se__button').text.strip())

    if soup.find('article', class_='col-md-9 col-sm-12 showroom-event-slide__content showroom-event-slide__content_desc'):
        event_info['event_descrip'] = re.sub(r'\.(\w)', r'. \1', soup.find('article', class_='col-md-9 col-sm-12 showroom-event-slide__content showroom-event-slide__content_desc').find('p').text)

    address_name = re.sub('\s+', ' ', soup.find('div', class_='event-info-se__address-part').find('address').text.strip())
    event_info['event_address_name'] = re.sub('Санкт-Петербург, ', '', address_name)

    event_info['event_address'] = re.sub('\s+', ' ', soup.find('article', class_='col-md-9 col-sm-12').find('span').text.strip())
    event_info['event_time'] = re.sub('\s+', ' ', soup.find('div', class_='event-info-se__address-part').find('time').text.strip())
    event_info['even_org_id'] = str(re.findall(r'"org":{"id":"\w+"', str(soup.contents[1]))[0])[13:-1]

    return event_info



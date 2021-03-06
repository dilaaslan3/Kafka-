from time import sleep
from wsgiref import headers
from bs4 import BeautifulSoup
import requests
from kafka import KafkaProducer

#fetching raw data from allrecipes.com
def fetch_raw(recipe_url):
    html = None
    print('proccessing..{}'.format(recipe_url))
    try:
        r= requests.get(recipe_url, headers=headers)
        if r.status_code == 200:
            html = r.text
    except Exception as exception:
        print(("Exception while accessing raw html"))
        print(str(exception))
    finally:
        return html.strip()


def get_recipes():
    recipies = []
    salad_url = 'https://www.allrecipes.com/recipes/96/salad/'
    url = 'https://www.allrecipes.com/recipes/96/salad/'
    print("accessing list")

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            html = r.text
            soup = BeautifulSoup(html, 'lxml') #BeautifulSoup is a library for pulling data out of HTML and XML files
            links = soup.select('.fixed-recipe-card__h3 a') #getting links of all receipes
            idx = 0
            for link in links:
                sleep(2)
                receipe = fetch_raw(link['href'])
                recipies.append(receipe) #list
                idx += 1
                if idx > 2:
                    break
    except Exception as exception:
        print("Exception in get_recipes")
        print(str(exception))


#publishing message
def publish_message(procuder_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        procuder_instance.send(topic_name, key=key_bytes, value=value_bytes)
        procuder_instance.flush() #Python automatically flushes the files when closing them. But i want to flush the data before closing any file.
        print("Message published successfully.")
    except Exception as exception:
        print("exception in publishing message")
        print(str(exception))


#connecting kafka
def connect_kafka_producer():
    _producer =  None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version =(0,10))
    except Exception as exception:
        print("exception while connecting kafka")
        print(str(exception))
    finally:
        return _prod




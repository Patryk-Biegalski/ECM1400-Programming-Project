import requests
import json
import copy
import logging

logging.basicConfig(filename='logger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s - %(module)s - %(lineno)s ')

def read_config():
    with open("config.json", "r") as conf:
        return json.load(conf)

# fetched data from news API
def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    temp = read_config()
    key = temp["news_api_key"]
    try:
        data = requests.get('https://newsapi.org/v2/everything?q='+(covid_terms)+'&language=en&sortBy=publishedAt&apiKey='+str(key))
    except Exception as e:
        logging.exception("Could not access the news API")
    return(data)

# Gets fetched news data using news_API_request
# Updates a file with the titles of all read articles
# removes read articles from fetched articles and returns the rest
def update_news(new_title, search_terms):
    print(str(new_title)+" has just been deleted")
    list_of_read_titles = []
    req = (news_API_request(search_terms))
    new_data = req.json()
    new_articles = new_data["articles"]
    # Adds all previously read titles to a list
    # Adds the new_title to the list
    # Saves the new list to the file
    try:
        with open('sample.json','r') as y:
            read_articles = json.load(y)
            titles=read_articles["titles"]
            for title in titles:
                list_of_read_titles.append(title)
    except FileNotFoundError:
        logging.debug("New file for saving read articles has been created")
    list_of_read_titles.append(new_title)
    data = {"titles":list_of_read_titles}
    print (("list of read articles: ")+str(data))
    with open('sample.json','w') as x:
        json.dump(data,x)

    # iterates through newly fetched articles and removes any that
    # are in the list of read articles
    # returns the remaining articles
    for new_article in new_articles[:]:
        if new_article["title"] in list_of_read_titles:
            print(str(new_article["title"])+" should be saved as read")
            new_articles.remove(new_article)
    return (new_articles)



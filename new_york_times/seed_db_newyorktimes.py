from requests import get # Web requests
from bs4 import BeautifulSoup # Web scraping
from pprint import pprint # Format prints nicely
from subprocess import run # Copy to clipboard
from json import dumps # Turn json to string
from mongoengine import *
from datetime import datetime

def main(month, year):
    # Connect to mongodb
    connect(host="mongodb://127.0.0.1:27017/politic")
    # Create mongodb collection to connect to
    class NYT(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        abstract = StringField()
        publication_date = DateTimeField(required=True)

    # Get NYT article as a JSON
    new_york_times = get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key=jUoQoVxEjhnPqV8rAoZAzp5dFDjkmvQS').json()
    # Get length of articles
    new_york_times_length = len(new_york_times['response']['docs'])
    # Loop through all articles
    for i in range(0, new_york_times_length):
        # Get html text for nth article
        nyt_article = get(new_york_times['response']['docs'][i]['web_url']).text
        # Create beautiful soup parser
        soup = BeautifulSoup(nyt_article, 'html.parser')

        # Get the article contents
        if soup.select('section[name]') != []:
            results = soup.select('section[name]')[0].text.strip()
        elif soup.select('div.g-story') != []:
            results = soup.select('div.g-story')[0].text.strip()
        elif soup.select('div.rad-story-body') != []:
            results = soup.select('div.rad-story-body')[0].text.strip()
        else:
            # Skip article if it does now work
            print(f"THIS ARTICLE DOES NOT WORK! {new_york_times['response']['docs'][i]['web_url']}")
            pass

        # Get the article source
        source = new_york_times['response']['docs'][i]['source']
        # Get the article URL
        url = new_york_times['response']['docs'][i]['web_url']
        # Get the print headline
        headline = new_york_times['response']['docs'][i]['headline']['print_headline']
        # Get the article's abstract
        abstract = new_york_times['response']['docs'][i]['abstract']
        # Get the article's publication date
        pub_date = new_york_times['response']['docs'][i]['pub_date'][0:10]

        # Skip this article if already in database
        if NYT.objects(web_url = url, publication_date = pub_date):
            print("Article " + str(i) + " already in db" + " : " + new_york_times['response']['docs'][i]['web_url'])
            pass
        else: 
            # Print the article number in list and URL
            print(str(i) + ": " + new_york_times['response']['docs'][i]['web_url'])

            # Save the article in the mongoDB database
            NYT(
                source           = source,
                web_url          = url,
                headline         = headline,
                content          = results,
                abstract         = abstract,
                publication_date = pub_date
            ).save()

if __name__ == "__main__":
    year = None
    month = None
    while month not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        month = int(input("""
Which month do you want to seed?
1 = January,   2  = February, 3 = March,     4 = April,
5 = May,       6  = June,     7 = July,      8 = August,  
9 = September, 10 = October, 11 = November, 12 = December      

> """))

    while year is None:
        year = int(input("""
Which year do you want to seed?    

> """))
    main(month, year)

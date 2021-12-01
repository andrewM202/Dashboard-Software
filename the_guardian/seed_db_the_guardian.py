from requests import get
from bs4 import BeautifulSoup
from mongoengine import *
from datetime import datetime, timedelta

def main():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")
    # Collection to connect to
    class Guardian(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        section = StringField()
        publication_date = DateTimeField(required=True)
    
    # Current page number calling
    page_num = 1
    # Call Guardian API
    guardian = get(f'https://content.guardianapis.com/search?page={page_num}&api-key=89e18c9c-1ff8-489e-a8d1-764a71a26779').json()
    # Date of first article being parsed
    date = guardian['response']['results'][0]['webPublicationDate']
    # Get last date of previous month
    # Date is like '2021-11-27T16:13:47Z', so date[0:10]
    # Shaves off everything except 2021-11-27
    date = datetime.strptime(date[0:10], '%Y-%m-%d')
    # Get first of the month
    first_of_month = date.replace(day=1)
    prev_month = first_of_month - timedelta(days=1)

    # Amount of pages API returns per call
    page_size = guardian['response']['pageSize']

    # Total articles processed
    article_processed_number = 0

    # Keep pulling articles until an article
    # Is found that is not in the current month
    pull_articles = True
    while pull_articles:
        # Call Guardian API
        guardian = get(f'https://content.guardianapis.com/search?page={page_num}&api-key=89e18c9c-1ff8-489e-a8d1-764a71a26779').json()
        page_num += 1
        for i in range(0, page_size):

            # Get content
            guardian_article = get(guardian['response']['results'][i]['webUrl']).text

            soup = BeautifulSoup(guardian_article, "html.parser")
            # Change how we get content based on the sectionID
            # Business, politics, science, world, technology
            sectionID = guardian['response']['results'][i]['sectionId']
            article_type = guardian['response']['results'][i]['type']
            if article_type == 'liveblog':
                content_parts = soup.select("div.block-elements")
                content = ''
                for con in content_parts:
                    content += con.text + ' '
            elif article_type == 'article':
                content = soup.select("section.css-jjd5tl")
                if content == []:
                    content = soup.select("div#maincontent")
                content = content[0].text

            article_date = guardian['response']['results'][i]['webPublicationDate'][0:10]
            article_date = datetime.strptime(article_date, '%Y-%m-%d')

            # Stop looping if article is from previous month
            if article_date <= prev_month:
                pull_articles = False
                break

            article_processed_number += 1

            # Skip this article if already in database
            if Guardian.objects(web_url = guardian['response']['results'][i]['webUrl'], publication_date = article_date):
                print("Article " + str(article_processed_number) + " already in db" + ": " + guardian['response']['results'][i]['webUrl'])
                pass
            else: 
                # Print the article number in list and URL
                print(str(i) + ": " + guardian['response']['results'][i]['webUrl']) 

                Guardian(
                    source           = "The Guardian",
                    web_url          = guardian['response']['results'][i]['webUrl'],
                    headline         = guardian['response']['results'][i]['webTitle'],
                    content          = content,
                    section          = sectionID,
                    publication_date = article_date
                ).save()

if __name__ == "__main__":
    main()

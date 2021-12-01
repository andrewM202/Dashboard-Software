from requests import get          # Make get requests
from mongoengine import *         # Database
from bs4 import BeautifulSoup     # HTML parsing
from dataclasses import dataclass # Easier classes
import datetime                   # Formatting dates

def main():
    # Connect to MongoDB
    connect(host="mongodb://127.0.0.1:27017/politic")
    # Create collection to interact with
    class ZH(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        abstract = StringField()
        publication_date = DateTimeField(required=True)

    # The homepage number in url
    homepage_number = 0

    # Current article processed. Used solely
    # To see article number in buffer
    article_processed_number = 0

    prev_month = None

    # Keep pulling articles until an article 
    # Is found that is not in the current month
    pull_articles = True
    while pull_articles == True:

        # Increase homepage number so we can 
        # Move to next page
        homepage_number += 1

        # Make get request for web page
        zerohedge = get(f"https://www.zerohedge.com/page/{homepage_number}").text
        # Initialize beautiful soup parser
        soup = BeautifulSoup(zerohedge, "html.parser")

        # Get the article headlines, abstract, and link
        headlines = soup.select("main.main-content > div > div > div > div > h2 > a")
        article_links = soup.select("main.main-content > div > div > div > div > h2 > a")
        abstracts = soup.select("main.main-content > div > div > div div.Article_desktopLineClamp__1bUBu")

        # List for all the article objects
        article_container = []
        
        # Add all the headlines, article links, 
        # And abstracts to array as article instances
        for i in range(0, len(article_links)):
            # Increase article processed
            article_processed_number += 1

            # Get article contents based off of gathered links
            article_link = "https://www.zerohedge.com" + article_links[i]['href']
            # Make get request to the article
           # So we can get contents
            zerohedge_article = get(article_link).text
            # Make parser for the article
            soupy_article = BeautifulSoup(zerohedge_article, "html.parser")
            # Get content of the article
            content = soupy_article.select("main.main-content > article div.NodeContent_body__2clki")[0]
            # Get publication date and format it correctly
            # (Otherwise like SATURDAY, NOV 20, 2021 - 07:15 AM)
            date = soupy_article.select("main.main-content > article > header > footer > div")[1].text
            comma = date.find(",") + 1
            date = date[comma:]
            # Now its like NOV 20, 2021 - 07:15 AM 
            # Remove everything hyphon and after
            hyphon = date.find("-")
            date = date[:hyphon].strip()
            # Now its NOV 20, 2021
            # Remove comma
            date = date.replace(",", "")
            # Format into yyyy-mm-dd format for MongoDB
            date = datetime.datetime.strptime(date, '%b %d %Y')

            # Check whether this date is too far back
            # Set previous month if this is first loop
            if article_processed_number == 1:
                # Check whether this date is too far back
                # Get first of the month
                first = date.replace(day=1)
                prev_month = first - datetime.timedelta(days=1)

            # If date in article is further back than
            # Current month, break loop
            if date <= prev_month:
                pull_articles = False
                break

            # Skip this article if already in database
            if ZH.objects(web_url = article_link, publication_date = date):
                print(f"Article {article_processed_number} already in db : {date} : {article_link}")
                pass
            else:
                # Print current article to buffer
                print(f"{article_processed_number} : {date}  : {article_link}")

                ZH(
                    source           = "ZeroHedge",
                    web_url          = article_link,
                    headline         = headlines[i].text.strip(),
                    content          = content.text,
                    abstract         = abstracts[i].text.strip(),
                    publication_date = date
                ).save()

if __name__ == "__main__":
    main()

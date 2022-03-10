from requests import get
from bs4 import BeautifulSoup

def main():
    # Make get request to fox news US news
    fox_news = get("https://www.foxnews.com/us").text
    # Initialize beautiful soup parser
    soup = BeautifulSoup(fox_news, 'html.parser')
    # Narrow down results
    results = soup.select('section.collection-article-list article.article')
    for result in results:
        #print(result.prettify())
        print(result.text.strip() + "\n")


if __name__ == "__main__":
    main()

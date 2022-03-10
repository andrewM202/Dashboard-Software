from mongoengine import *
from json import loads
import spacy # Used for NLP (natural language processing)


def main():
    # Connect to mongodb
    con = connect(host="mongodb://127.0.0.1:27017/politic")
    # class to query
    class NYT(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        abstract = StringField()
        publication_date = DateTimeField(required=True)

    #dbs=con.list_database_names()
    art_cont = []
    for obj in NYT.objects:
        obj = obj._data['content'].lower().strip().replace(",", "").replace(".", "").replace("\\", "")
        for norm_exception in spacy.lang.norm_exceptions.BASE_NORMS:
            obj = obj.replace(f"{norm_exception}", "")
        art_cont.append(obj)
    
    d = dict()

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    for article in art_cont:
        # Get all the individual words in the article
        words = article.split(" ")
        for word in words:
            word = word.strip()
            if word in nlp.Defaults.stop_words:
                pass
            elif word == "":
                pass
            elif word in d:
                d[word] = d[word] + 1
            else:
                d[word] = 1

    words = dict(sorted(d.items(), key=lambda item: item[1]))
    for key in words:
        if d[key] > 1:
        #if d[key]:
            print(key, ":", d[key])

if __name__ == "__main__":
    main()

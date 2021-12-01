from mongoengine import *
import spacy

def main():
    # Connect to MongoDB
    con = connect(host="mongodb://127.0.0.1:27017/politic")
    # Class to query
    class Guardian(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        section = StringField()
        publication_date = DateTimeField(required=True)

    article_content = []
    for obj in Guardian.objects:
        obj = obj._data['content'].lower().strip().replace(",", "").replace(".", "").replace("\\", "").replace(";", "")
        for norm_exception in spacy.lang.norm_exceptions.BASE_NORMS:
            obj = obj.replace(f"{norm_exception}", "")
        article_content.append(obj)

    d = dict()

    # load spacy
    nlp = spacy.load("en_core_web_sm")

    for article in article_content:
        # Get individual words in article
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
        if d[key] > 500:
        #if d[key]:
            print(key, ":", d[key])

if __name__ == "__main__":
    main()


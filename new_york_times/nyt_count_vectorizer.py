from sklearn.feature_extraction.text import CountVectorizer
from mongoengine import *
from json import loads


def main():
    # Connect to mongodb
    db_name = 'politic'
    con = connect(host="mongodb://127.0.0.1:27017/politic")
    # class to query
    class new_york_times(Document):
        source = StringField(required=True)
        web_url = URLField(required=True)
        headline = StringField(required=True)
        content = StringField(required=True)
        abstract = StringField()
        publication_date = DateTimeField(required=True)

    dbs=con.list_database_names()
    #print(con.get_database(db_name).list_collection_names())
    #print(new_york_times.objects)
    #for db in dbs:
        #print(db)
    art_cont = []
    for obj in new_york_times.objects:
        #print(obj._data['content'])
        #art_cont.append(obj._data['content'])
        pass
    
    art_cont.append(new_york_times.objects[0]._data['content'])
    print(new_york_times.objects[0]._data['web_url'])

    print(art_cont)

    # Create vectorizer object
    vectorizer = CountVectorizer()
    vectorizer.fit(art_cont)
    vectorizer.strip_accents
    vectorizer.lowercase
    # Printing the identified Unique words along with their indices
    print("Vocabulary: ", vectorizer.vocabulary_)
    # Encode the Document
    vector = vectorizer.transform(art_cont)
    # Summarizing the Encoded Texts
    print("Array of encoded texts")
    print(vector.toarray())
        



if __name__ == "__main__":
    main()

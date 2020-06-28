import json
import pandas as pd
from elasticsearch import Elasticsearch


database = pd.read_csv("./stylefarming/data/nmwa_100pgs.csv")

database['num_likes'] = database['num_likes'].fillna(0)
es_client = Elasticsearch(http_compress=True)

df=database.copy()

INDEX="nmwa" # Its name in Elasticsearch
TYPE= "record"

def rec_to_actions(df):
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}'% (INDEX, TYPE))
        yield (json.dumps(record, default=int))

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = e.bulk(rec_to_actions(df))
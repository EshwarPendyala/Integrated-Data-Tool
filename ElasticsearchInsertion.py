import json
import os
import pandas as pd
from pathlib import Path
from time import sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
client = Elasticsearch("localhost:9200")

def searchQueryResultDisplay():
    query_all = {
        'size': 10000,
        'query': {
            'match_all': {}
        }
    }

    sleep(2)
    resp = client.search(
        index="some_index",
        body=query_all
    )

    print("search() response:", json.dumps(resp, indent=4))
    # print("Length of docs returned by search():", len(resp['hits']['hits']))

def getDataFromFile(self):
    return [l.strip() for l in open(str(self), encoding="utf8", errors='ignore')]


def indexAndInsert(docs, doc_list):
    for num, doc in enumerate(docs):
        try:
            doc = doc.replace("True", "true")
            doc = doc.replace("False", "false")
            dict_doc = json.loads(doc)
            dict_doc["timestamp"] = datetime.now()
            dict_doc["_id"] = num
            doc_list += [dict_doc]
        except json.decoder.JSONDecodeError as err:
            print("ERROR for num:", num, "-- JSONDecodeError:", err, "for doc:", doc)
            print("Dict docs length:", len(doc_list))
    
    try:
        print("\nAttempting to index the list of docs using helpers.bulk()")
        resp = helpers.bulk(
            client,
            doc_list,
            index="some_index",
            )
        print("helpers.bulk() RESPONSE:", resp)
        print("helpers.bulk() RESPONSE:", json.dumps(resp, indent=4))

    except Exception as err:
        print("Elasticsearch helpers.bulk() ERROR:", err)
        quit()
    
def insertDataInElasticsearch():
    jsonFiles = Path("/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store").glob("**/*.json")
    for file in jsonFiles:
        doc_list = []
        docs = getDataFromFile(os.path.abspath(file))
        try:
            indexAndInsert(docs, doc_list)
            searchQueryResultDisplay()
        except Exception as err:
            print("Here is the error",err)

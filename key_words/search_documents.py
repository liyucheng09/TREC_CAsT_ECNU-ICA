from elasticsearch import Elasticsearch
from pprint import pprint
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)['configuration']


def search(words, field="BODY", size=10, debug=True):
    es = Elasticsearch([config['server']['host']], http_auth=(config['server']['username'], config['server']['password']))
    query = {
        "query": {
            "bool": {
                "should": [{"term": {field: word}} for word in words]
            }
        }
    }
    if debug:
        pprint(query)
    try:
        res = es.search(index=config['elasticsearch']['index'], body=query, size=size)
        if debug:
            pprint(res)
        return res["hits"]["hits"]
    except Exception as e:
        raise e



# pprint(search("BODY", ["in", "world"], 1, True))

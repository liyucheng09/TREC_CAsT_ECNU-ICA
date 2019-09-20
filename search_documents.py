from elasticsearch import Elasticsearch
from pprint import pprint
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)['configuration']

def search_test(query, size=10):
    es = Elasticsearch([config['server']['host']], http_auth=(config['server']['username'], config['server']['password']))
    res = es.search(index=config['elasticsearch']['index'], body=query, size=size, request_timeout=30)
    return res["hits"]["hits"]


def search(words_weight, size=10, field="BODY", debug=False):
    es = Elasticsearch([config['server']['host']], http_auth=(config['server']['username'], config['server']['password']))
    query = {
        "query": {
            "bool": {
                "should": [
                           {"match_phrase": 
                               {field: {"query": word, "boost": weight}}} for word, weight in words_weight.items()]
            }
        }
    }
    if debug:
        pprint(query)
    try:
        # print(query)
        res = es.search(index=config['elasticsearch']['index'], body=query, size=size, request_timeout=30)
        return res["hits"]["hits"]
    except Exception as e:
        raise e


if __name__=='__main__':
    pprint(search({"Yet the":2.0, "world":1.0}, size=2, debug=True))

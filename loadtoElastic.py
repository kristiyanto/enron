#################################################################
# Enron Email for Slack Coding Challenge
# by Daniel Kristiyanto, danielkr@uw.edu 
# Palo Alto, Autumn 2016
#
# This script is to walk the directory, parse (using Berkeley's parser) 
# the enron data and load it into elasticsesarch
#################################################################

import os
import json
from elasticsearch import Elasticsearch
from enronparser import enronEmail

es = Elasticsearch(['192.168.0.216'], port=9200)

# Directory where the raw enron data is located
def main():
    rootDir = '{}/rawdata/enron_with_categories'.format(os.getcwd())

    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            # Skip if the file is related to categories.
            if fname != "categories.txt" and fname[0] != "." and fname.endswith("txt"): 
                result = storeToEs(enronEmail.parse_email(os.path.join(dirName, fname)))
               
  
                
def storeToEs(data, es_index):
    header, message = data
    q = '{{"doc": {},  "doc_as_upsert" : "true"}}'.format(json.dumps(header))
    res1 = es.update(index=header, doc_type='enron', id=fname, \
                                    body=q)
    
    m = json.dumps({'Message-ID': header['Message-ID'], 'Message': message})
    m = '{{"doc": {},  "doc_as_upsert" : "true"}}'.format(m)
    res2 = es.update(index='message', doc_type='enron', id=fname, \
                    body=m)
    
    return (res1, res2)

if __name__ == '__main__':
    main()

            
            
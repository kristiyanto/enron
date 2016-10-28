from elasticsearch import Elasticsearch
es = Elasticsearch(['192.168.0.216'], port=9200)

header = {'Content-Transfer-Encoding': {'type': 'string',  "include_in_all": "false"},
          'Content-Type': {'type': 'string',  "include_in_all": "false"},
          'Date': {'type': 'date',  "include_in_all": "true", 'format':'basic_ordinal_date_time_no_millis'},
          'From': {'type': 'string',  "include_in_all": "false"},
          'Message-ID': {'type': 'string',  "include_in_all": "true"},
          'Mime-Version': {'type': 'string',  "include_in_all": "false"},
          'Subject': {'type': 'string',  "include_in_all": "false"},
          'To': {'type': 'string',  "include_in_all": "false"},
          'X-Bcc': {'type': 'string',  "include_in_all": "false"},
          'X-Cc': {'type': 'string',  "include_in_all": "false"},
          'X-FileName': {'type': 'string',  "include_in_all": "false"},
          'X-Folder':{'type': 'string',  "include_in_all": "false"},
          'X-From': {'type': 'string',  "include_in_all": "false"},
          'X-Origin': {'type': 'string',  "include_in_all": "false"},
          'X-To': {'type': 'string',  "include_in_all": "false"}}


message= {'Message-ID': {'type': 'string',  "include_in_all": "true"},
          'Message': {'type': 'string',  "include_in_all": "false"},
         }


header_mapping = {
  'settings' : {
                    'number_of_shards' : 5,
                    'number_of_replicas' : 1 },  
                    'mappings': {
                    'enron':{
                    'properties': header }
                }}

message_mapping = {
  'settings' : {
                    'number_of_shards' : 20,
                    'number_of_replicas' : 2 },  
                    'mappings': {
                    'enron':{
                    'properties': message }
                }}

es.indices.delete(index='header', ignore=[400, 404])
es.indices.delete(index='message', ignore=[400, 404])

es.indices.create(index='header', body=header_mapping, ignore=400)
es.indices.create(index='message', body=message_mapping, ignore=400)


#!bin/bash
docker run -d -p 9200:9200 -p 9300:9300 -v "$PWD/elasticsearch":/usr/share/elasticsearch/data elasticsearch 


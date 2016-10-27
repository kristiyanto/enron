#!/bin/bash
docker run --name enronmysql -e MYSQL_ROOT_PASSWORD=enron -p 3306:3306 -v $PWD/mysql:/data -d mysql:latest
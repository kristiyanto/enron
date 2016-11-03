FROM mysql:latest
MAINTAINER Daniel Kristiyanto <danielkr@uw.edu>

RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv libmysqlclient-dev && \
  rm -rf /var/lib/apt/lists/*
RUN pip install pytz 
RUN pip install python-dateutil
RUN pip install mysql-connector

WORKDIR /enron
ADD enronparser enronparser
ADD mysql mysql
ADD queries queries
ADD rawdata rawdata
ADD Parse_and_Load_Data_To_MySQL.py Parse_and_Load_Data_To_MySQL.py

EXPOSE 3306
CMD ["bash"]


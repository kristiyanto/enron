[![](https://images.microbadger.com/badges/image/kristiyanto/enron.svg)](https://microbadger.com/images/kristiyanto/enron "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/kristiyanto/enron.svg)](https://microbadger.com/images/kristiyanto/enron "Get your own version badge on microbadger.com")

# ENRON EMAIL 
### by Daniel Kristiyanto - Palo Alto, Autumn 2016

## Intro
Enron, the infamous energy company that went bankrupt in the early 2000s after engaging in massive accounting fraud, was a heavy user of email. As part of the government’s investigation into Enron’s malfeasance, a large number of emails written by Enron’s executive team was released to the public, and this corpus has since become a useful resource for computer scientists, computational linguists, and sociologists.

This excericse is to address following questions:

1. How many emails did each person receive each day?
2. Let's label an email as "direct" if there is exactly one recipient and "broadcast" if it has multiple recipients. Identify the person (or people) who received the largest number of direct emails and the person (or people) who sent the largest number of broadcast emails.
3. Find the five emails with the fastest response times. (A response is defined as a message from one of the recipients to the original sender whose subject line contains all of the words from the subject of the original email, and the response time should be measured as the difference between when the original email was sent and when the response was sent.)


# ANSWERS
Please refer to [queries](queries) and [results](results) for more detailed information. 

Data representation for the answer are also available on [Tableau Public: https://public.tableau.com/shared/H8MHYTKD3](https://public.tableau.com/shared/H8MHYTKD3)

1.  Please refer to [results\Email_Per_Day.csv](results\Email_Per_Day.csv)  
2.  A: maureen.mcvicker@enron.com Received the largest of direct email with the total of 115 emails.  
    B: steven.kean@enron.com sent most of broadcast emails (email with recipients >1), with total of 253 emails.
3. As follow:  

| Date (Sender1)      | Date (Sender2)      | Respond Time (seconds) | Subject                                                                 | Sender1                   | Sender2                     |
|---------------------|---------------------|------------------------|-------------------------------------------------------------------------|---------------------------|-----------------------------|
| 2001-11-21 08:52:26 | 2001-11-21 08:49:58 |                    148 | FW: Confidential - GSS Organization Value to ETS                        | stanley.horton@enron.com | rod.hayslett@enron.com      |
| 2001-05-10 06:51:00 | 2001-05-10 06:55:00 |                    240 | RE: Eeegads...                                                          | paul.kaufman@enron.com   | jeff.dasovich@enron.com     |
| 2001-10-26 09:18:58 | 2001-10-26 09:13:36 |                    322 | RE: CONFIDENTIAL Personnel issue                                        | michelle.cash@enron.com  | lizzette.palmer@enron.com   |
| 2001-11-21 10:59:36 | 2001-11-21 11:12:04 |                    748 | RE: Confidential - GSS Organization Value to ETS                        | rod.hayslett@enron.com   | morris.brassfield@enron.com |
| 2001-11-14 14:34:57 | 2001-11-14 15:24:08 |                   2951 | RE: PG&E PX Credit Calculation -- CONFIDENTIAL ATTY CLIENT WORK PRODUCT | alan.comnes@enron.com    | d..steffes@enron.com        |


# Folder Structures:
**mysql**               : Schema for MySQL  
**queries**             : Queries to answer the questions  
**rawdata**             : Extracted Data of [Enron Emails from UC Berkeley](http://bailando.sims.berkeley.edu/enron/enron_with_categories.tar.gz)  
**enronparser**         : contains script downloaded from [UC Berkeley](http://courses.ischool.berkeley.edu/i290-2/f04/assignments/enronEmail.py), written by Andrew Fiore to Parse Enron email to Dictionary.  
  
**Parse_and_Load_Data_To_MySQL.py** : A python script to load the data into MySQL  
**runMySQL.sh**         : A shell script to run MySQL as a Docker Container.  
**run-spark-python.sh** : A shell script to run Spark-enabled Python Docker Container --Only used to debug/further analysis. Not used for submission.  
**README.md**           : This file.  


# Requirements
1. MySQL (Latest version)
2. Python 2.7, Packages: dateutil, mysql.connector, email.utils, pytz

## Manual
1. Install MySQL (Or using Docker, script: `runMySQL.sh`).
```bash
bash runMySQL.sh
```
2. Create MySQL Schema (script: `mysql\schema.sql.txt`)
```bash
# for Docker solution, default password is: enron
mysql -u root --password=password

## Within mysql console:
    source schema.sql.txt
```
3. Make sure Python MySQL connector is installed. More info: https://dev.mysql.com/downloads/connector/python/
4. Make sure additional python libraries installed.
4. The enron email data should be ready (and extracted) under folder `rawdata/`
5. Run `Parse_and_Load_Data_To_MySQL.py`
```python
python Parse_and_Load_Data_To_MySQL.py
```

## Docker 
The solution is also available as a docker container.
On Docker enabled machines:
```bash
docker run -ti -p 3306:3306 kristiyanto\enron
```
Once docker is loaded:
```bash
cd mysql
service mysql start
mysql -u root

# On mysql console:
    CREATE database enron;
    source schema.sql.txt
    exit

cd ..
python Parse_and_Load_Data_To_MySQL.py

## The script does not produce any startard output. 
```
Now that the data is loaded to MySQL, queries can be performed either within the docker directly, or can be linked to external applications (e.g. Tableau) or Microsoft Excel.


# Architecture
Emails were downloaded from [Enron Emails from UC Berkeley](http://bailando.sims.berkeley.edu/enron/enron_with_categories.tar.gz), and extracted. A python script with leverage a parser (also from UC Berkeley) was used to load the email data into MySQL. 
To answer the questions, SQL queries were performed. Results are saved as CSV in results folder.

- Please refer to [schema.sql.txt](mysql/schema.sql.txt) for more detailed about the SQL schema
- Please refer to [Parse_and_Load_Data_To_MySQL.py](Parse_and_Load_Data_To_MySQL.py) for more detailed information about how the data were loaded to MySQL
- Please refer to [queries](queries) folder for more detailed information for each queies


# Assumptions
Within each query (in queries folder), a more detailed information is provided, but in general:
- All emails (both Enron-specific and external emails) were treated equally
- Sender with average recipients over time are considered as the largest number of broadcast email
- Only DISTINCT recipients are performed (e.g if a recipient is included in both To and CC, is considered as 1 recipient)
- All the dates were converted to Pacific Time (GMT -7)
- Some of the data show wrong dates (back in 1979), this data was not treated differently --assuming that there was some explanation for this mistake (e.g. Server misconfiguration, or Millenium bug/Y2K problem.). Given that there was no email sent/received between Dec 29, 1999 - Jan 3, 2000, Y2K millennium bug may be considered as the problem, however, a further investigation needed. Reference: https://www.britannica.com/technology/Y2K-bug
- Although some email may appear unusual, e.g. email address containing apostrophes or two dots, these addresses are a valid address and often used for internal usage. These emails were treated no differently. More Info: https://tools.ietf.org/html/rfc5322 


# Contact 
Daniel Kristiyanto


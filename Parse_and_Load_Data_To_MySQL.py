#!/usr/bin/python
#################################################################
# Enron Email for Slack Coding Challenge
# by Daniel Kristiyanto, danielkr@uw.edu 
# Palo Alto, California -- Autumn 2016
#
# This script is to walk the directory, parse (using Berkeley's parser) 
# the enron data and load it into MySQL
#################################################################


import os
from enronparser import enronEmail
from dateutil import parser
import mysql.connector
from email.utils import getaddresses
import pytz


#mysql_host = '192.168.0.216'
mysql_host = '127.0.0.1'


def main():
    # Walk trough all the files in the directory
    rootDir = '{}/rawdata/enron_with_categories'.format(os.getcwd())
    
    
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            # Only read mail files (XXX.txt)
            if fname != "categories.txt" and fname[0] != "." and fname.endswith(".txt"):
                header, message = enronEmail.parse_email(os.path.join(dirName, fname))
                result = storeToMysql(header, message)

                
############################################
# Normalize Time from parser
# Input: time (str)
# Return: converted time (str) 
############################################

def dateConv(dt):
    dt = parser.parse(dt).astimezone(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
    return dt




############################################
# Store parsed data to MySQL
# Input: header (Dict), message (Str)
# Return: None
############################################

def storeToMysql(header, message):
    
    
    
    '''
        MySQL connection and Database Schema
        Tables:
            addrbook: Addressbook (Email and Name)
            header: Header information (Message-ID, Sender, Date, Subject, etc..)
            msg: Email body (Message-ID, Body)
            recipients: The recipients (Message-ID, Email, Type: Bcc. To., etc)
        please refer to folder ../msql for more complete schema.
        
    '''
    
    cnx = mysql.connector.connect(user='root', password='enron', host=mysql_host,
                              database='enron')
    cursor = cnx.cursor()
    head = ['`Message-ID`', 'Sender', 'Subject', 'Date']
    emp = ['Email', 'Name']
    rec = ['Type', '`Message-ID`', 'Recipient']
    msg = ['`Message-ID`', '`Mime-Version`', 'ContentType', '`Content-Transfer-Encoding`',
    '`X-Folder`', 'body']
    
    
    
    
    
    '''
        Query builder for each tables
    '''
    add_addrbook = (("INSERT IGNORE INTO addrbook ({}) VALUES (%s, %s)".format(", ".join(emp))),
                    (header['From'], header['X-From']))
 
    add_msg = (("INSERT IGNORE INTO msg ({}) VALUES (%s, %s, %s, %s, %s, %s)").format(", ".join(msg)),
               (header['Message-ID'], header['Mime-Version'], header['Content-Type'], 
                header['Content-Transfer-Encoding'], header['X-Folder'], message))
    
    add_head = (("INSERT IGNORE INTO header ({}) VALUES (%s, %s, %s, %s)".format(", ".join(head))), 
               (header["Message-ID"], header["From"], header["Subject"], dateConv(header['Date'])))    
    
    
    cursor.execute(*add_addrbook)
    cursor.execute(*add_msg)    
    cursor.execute(*add_head)

    
    
    
    
    '''
        Recipients section. Read each recipients and store it into recipient table as well into
        the addressbook table.
    '''

    for rtype in ['To', 'Cc', 'Bcc']:
        if rtype in header.keys():
            add_rec = ("INSERT IGNORE INTO recipients ({}) VALUES (%s, %s, %s)".format(", ".join(rec)))

            add_employee_rec = ("INSERT IGNORE INTO addrbook (Name, Email) VALUES (%s, %s)",
                     [(name, email) for name, email in getaddresses([header[rtype]])])

            cursor.executemany(add_rec,                [(rtype, header['Message-ID'], email[1]) for email in getaddresses([header[rtype]])])
            cursor.executemany(*add_employee_rec)
                

    cnx.commit()
    cursor.close()
    cnx.close()

    
    
if __name__ == '__main__':
    main()






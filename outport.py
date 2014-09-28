#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
some db interface 
"""
import pymongo
import pycurl
from BeautifulSoup import BeautifulSoup 
import StringIO
import time
from django.utils.encoding import smart_str, smart_unicode
import os 
import traceback
from datetime import datetime,timedelta
import datetime
import  json
#from smallgfw import GFW
import os 
import os.path
from pymongo import ASCENDING,DESCENDING 
import requests 
from urlparse import urlparse
import sys
import urlparse
import re
import types 
import sys
import logging  
import urllib
from urllib import urlencode

import time, MySQLdb


logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'),level = logging.WARN, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')


mktime=lambda dt:time.mktime(dt.utctimetuple())




conn=MySQLdb.connect(host="localhost",user="root",passwd="fubendong",db="wangwang",charset="utf8")  
cursor = conn.cursor()
    

def imports (num):
    files = str(datetime.date.today())+ "_" + num
    print files
    filename = "./wangwang/" + files + ".txt"
    print filename
    num = int(num)
    file_object = open(filename, 'a')
    
    i = 1
    try:
        while True:
            
            count=cursor.execute('SELECT username FROM `wangwang_detal` where type = 1 and displayRateSum < 250  ORDER BY `Lastweek` DESC, `displayRateSum` DESC, `Lastmonth` DESC, `Lastsixmonth` DESC  limit 1 ')
            #print 'there has %s rows record' % count
            
            result=cursor.fetchone()
            #print result
            username = result[0].encode('UTF8')
            sql = " update wangwang_detal set type = 0 where username = '%s' " % username
            #print sql
            res = cursor.execute(sql)

            sql = " update wangwang_tmall set type = 0 where username = '%s' " % username
            #print sql
            res = cursor.execute(sql)

            print res
            file_username = result[0].encode('UTF8') + "\n"
            file_object.write(file_username)
#             file_username = str(file_username)
            
            
            
            i = i + 1
            print  i
            print num
            if i > num :
                print 'aaaaa'
                break ;
            
    except Exception ,e:
        print e
        
#      file_object.close()






if __name__ == "__main__":
    if len(sys.argv) >1:
        print sys.argv[1]
        num = sys.argv[1]
        imports(num)
            
            
            
            

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
    

def imports ():
    filename = "nvzhuang"
    file = open(filename)
    type = "nvzhuang";
    i = 1
    try:
        while 1:
            try:
                
                line = file.readline()
                if not line:
                    break
                print line
                line = line.strip('\n')
    #             username = result[0].encode('UTF8')
                sql = "insert into keyword values('', '%s' ,'%s', 1, '%s' )" % (line , type, int(time.time()))
                print sql
                res = cursor.execute(sql)
                print res
            except Exception ,e:
                 print e
    except Exception ,e:
        print e
        
#      file_object.close()






if __name__ == "__main__":
    imports()
            
            
            
            

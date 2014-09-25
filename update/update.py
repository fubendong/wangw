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


# logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'),level = logging.WARN, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')


mktime=lambda dt:time.mktime(dt.utctimetuple())
######################db.init######################
# connection = pymongo.Connection('localhost', 27017)
# 
# db=connection.x


conn=MySQLdb.connect(host="localhost",user="root",passwd="fubendong",db="wangwang",charset="utf8")  
cursor = conn.cursor()
    

#browser = requests.session()
######################gfw.init######################
#gfw = GFW()
#gfw.set(open(os.path.join(os.path.dirname(__file__),'keyword.txt')).read().split('\n'))
#
#lgfw = GFW()
#lgfw.set(['thunder://','magnet:','ed2k://'])



def zp(data):
    """
    print dict list
    """
    for k in data:
        print '%s:'%k,data[k]

def get_html(url,referer ='',verbose=False,protocol='http'):
    if not url.startswith(protocol):
        url = protocol+'://'+url
    url = str(url)
    
    time.sleep(1)
    html=''
    headers = ['Cache-control: max-age=0',]
    try:
        crl = pycurl.Curl()
        crl.setopt(pycurl.VERBOSE,1)
        crl.setopt(pycurl.FOLLOWLOCATION, 1)
        crl.setopt(pycurl.MAXREDIRS, 5)
        crl.setopt(pycurl.CONNECTTIMEOUT, 8)
        crl.setopt(pycurl.TIMEOUT, 30)
        crl.setopt(pycurl.VERBOSE, verbose)
        crl.setopt(pycurl.MAXREDIRS,15)
        crl.setopt(pycurl.USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1')
        #crl.setopt(pycurl.HTTPHEADER,headers)
        if referer:
            crl.setopt(pycurl.REFERER,referer)
        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.URL, url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        crl.perform()
        html=crl.fp.getvalue()
        crl.close()
    except Exception,e:
        print('\n'*9)
        traceback.print_exc()
        print('\n'*9)
        return None
    return html

    #r = requests.get(url)
    #return r.text

    #r = browser.get(url)
    #return r.content

def executeNonQuery(sql):
    while cursor.nextset(): 
        pass
    cursor.execute(sql)
    
    
def runcrawler():
    j = 1
    num = ''
    url = "http://member1.taobao.com/member/user_profile.jhtml?user_id=%s"
    while True:
        
        count=cursor.execute('SELECT id, username FROM `wangwang_tmall` where displayRateSum < 900 and  displayRateSum > 150 and is_update = 0 and type = 1 ORDER BY `id` DESC  limit 1')
#         print 'there has %s rows record' % count
        if count == 0 :
            print "end"
            break
        row = cursor.fetchone() 
        username = row[1]
        id = row[0]
        sql1 = " update wangwang_tmall set is_update = 1 where id = %s " % (id)
        res = cursor.execute(sql1)
#         print "fsa %s" % username
        if username :
            try:
                username_encode = username.encode('GBK')
#                 username_encode = '%B8%B6%B1%BE%B6%AB1'
                url = "http://member1.taobao.com/member/user_profile.jhtml?user_id=%s"% username_encode
                logging.warning(url)
#                 print " %s ", url
                html=get_html(url)
                soup = BeautifulSoup(html,fromEncoding='gbk')
                #print soup
                user_rate = soup.find('ul',{'class':'TabBarLevel1'}).findAll('li')[1].a
#                 user_rate_url = user_rate.findAll('li')[1].a
                item_url = user_rate['href']
#                 print item_url
                html=get_html(item_url)
                soup_item = BeautifulSoup(html,fromEncoding='gbk')
                
                user_credit = soup_item.find('li',{'class':'credit'}).a.string
                logging.warning(user_credit)
                print user_credit
                user_data = soup_item.findAll('td',{'class':'rateok'})
                rateok  = []
                for user_rateok in user_data:
                    rateok.append(user_rateok.a.string)
                Lastweek = rateok[0]
                Lastmonth = rateok[1]
                Lastsixmonth = rateok[2]
                
                sql1 = " update wangwang_tmall set is_update = 1 ,displayRateSum = '%s', Lastweek = '%s',Lastmonth = '%s',Lastsixmonth = '%s'  where id = %s " % (user_credit,Lastweek ,Lastmonth,Lastsixmonth, id)
#                 print sql1
                res = cursor.execute(sql1)
                
                sql2 = "INSERT INTO `wangwang_detal`( `username`, `displayRateSum`, `Lastweek`, `Lastmonth`, `Lastsixmonth`, `is_update`, `type`, `add_time`)  VALUES ('%s','%s','%s','%s','%s',1,1,'%s')" % (username ,user_credit ,Lastweek , Lastmonth ,Lastsixmonth, int(time.time())  )
                
                res = cursor.execute(sql2)
#                 print res
                
            except Exception,e:
                
                print e
                sql1 = " update wangwang_tmall set is_update = 1 where id = %s " % (id)
#                  print sql1
                res = cursor.execute(sql1)
#                  print res
                 
                 
                 
                 
if __name__ == "__main__":
    
    runcrawler()

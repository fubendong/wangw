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
######################db.init######################
connection = pymongo.Connection('localhost', 27017)

db=connection.x


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

def transtime(stime):
    """
    将'11-12-13 11:30'类型的时间转换成unixtime
    """
    if stime and ':' in stime:
        res=stime.split(' ')
        year,mon,day=[int(i) for i in res[0].split('-')]
        hour,second=[int(i) for i in res[1].split(':')]
        unixtime=mktime(datetime.datetime(year,mon,day,hour,second))
        return unixtime
    else:
        return int(time.time())
       



def searchcrawler(url,keyword=''):
    """
    tb搜索页爬虫
    """
    html=get_html(url)
    print url
    if html:
        soup = BeautifulSoup(html,fromEncoding='gbk')
        items_row = soup.findAll('div',{'class':'item-box st-itembox'})
        #items_row = soup.find('div',{'class':'item-box st-itembox'})
        #print items_row
        if items_row:
            print '=======================row search row=========================='
            for item in items_row:
                item_info = item.find('h3',{'class':'summary'}).a
                item_url = item_info['href']
                url_info = urlparse.urlparse(item_url)
                item_id = urlparse.parse_qs(url_info.query,True)['id'][0]
                item_id = 16862466992
                download_reply_by_id(item_id)

def download_reply_by_id(iid):
    i = 1;
    data = []
    url="http://a.m.tmall.com/ajax/rate_list.do?item_id=%s&p=1&ps=50"%iid
    while True:
        res_json=get_html(url)
        
        res_json = json.loads(res_json)
        total = res_json["total"]
        if total == 0:
            break;
        for info in res_json["items"]:
            info_annoy = info["annoy"]
            if info_annoy == 0 :
                #info_buyer = json.dumps(info['buyer'],ensure_ascii=False)
                
                username = str(info["buyer"].encode('utf-8'))
                save_download_wangwang(username)
                logging.warning(info["buyer"]) 
        if i >= total:
            break;
        if total > 1 :
            i = i +1
            url="http://a.m.tmall.com/ajax/rate_list.do?item_id=%s&p=%s&ps=50"%(iid,i)
#             res_json=get_html(url)

def save_download_wangwang(username):
    """
    save item crawler log
    """
#     sql = "insert into wangwang values('',%s,'%s')" 
#     print sql
#     
#     param = (username,int(time.time()))    
#     n = cursor.execute(sql,param)    
#     print n
    
    try:
        sql = "insert into wangwang values('',%s,2,'%s')" 
        param = (username,int(time.time()))
        n = cursor.execute(sql,param)
    except:
        #nothing
        a =1
        
        
        
   
    
    
    
def runcrawler():
    j = 1
    num = ''
    url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc"
    for k in db.keyword.find():
        if k :
            j = 1;
            while j < 4 :
                try:
                    name = json.dumps(k['name'],ensure_ascii=False,indent=2)
                    name = name.encode('utf-8').replace('\r\n', '\\r\\n')
                    logging.warning(name) 
                    f = { 'q' : name}

                    key = urllib.urlencode(f)
                    print j
                    print url
                    url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc&s=%s"%(key,num)
                    
                    searchcrawler(url,keyword=k['name'])
                    num = 44 * j
                    j = j +1
                    
#                     url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc&s=%s"%key
                    
                    
                except:
                    j = j +1
                    num = 44 * j
                    url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc&s=%s"%(key,num)
                    
           
            
           
        

def update_item_date(interval=86000):
    for item in db.item.find():
        try:
            if check_item_update_time(item['itemid'],item['site'],interval):
                continue
            if item['site'] == 'tm':
                data = getTmallItemInfo(item['itemid'],'tm')
            elif item['site'] == 'tb':
                data = getTaobaoItemInfo(item['itemid'],'tb')
            save_item(data)
        except Exception ,e:
            print locals()
            print traceback.print_exc()
            continue

def cleandata():
    db.item.drop() 
    db.itemlog.drop() 
    db.shop.drop() 

if __name__ == "__main__":
    if len(sys.argv) >1:
        print sys.argv[1]
        if sys.argv[1] == 'search':
            runcrawler()
        elif sys.argv[1] == 'update':
            update_item_date()

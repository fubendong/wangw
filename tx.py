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
       



def searchcrawler(url):
    
    html=get_html(url)
#     print url
    if html:
        soup = BeautifulSoup(html,fromEncoding='gbk')
        items_row = soup.findAll('div',{'class':'product-iWrap'})
        #items_row = soup.find('div',{'class':'item-box st-itembox'})
#         print items_row
        if items_row:
            print '=======================row search row=========================='
            for item in items_row:
#                 print item
                item_info = item.find('p',{'class':'productTitle'}).a
                item_url = item_info['href']
#                 print item_url
                
                url_info = urlparse.urlparse(item_url)
                item_id = urlparse.parse_qs(url_info.query,True)['id'][0]
                print item_id
#                 item_id = 16862466992
                download_reply_by_id(item_id)

def download_reply_by_id(iid):
    i = 1;
    data = []
    #http://rate.tmall.com/list_detail_rate.htm?itemId=16862466992&order=1&currentPage=2&append=0&content=1&tagId=&posi=&picture=&_ksTS=1410515765306_2008&callback=jsonp2009
    url = "http://rate.tmall.com/list_detail_rate.htm?itemId=%s&order=1&currentPage=%s&append=0&content=1&tagId=&posi=&picture=&_ksTS=1410515765306_2008&callback=jsonp2009"%(iid,i)
#     print url
    res_json=get_html(url)
    while True:
        try:
            res_json = res_json[13:]
            res_json=res_json[:-1]
            res_json = json.loads(res_json,encoding='gbk')
            for info in res_json["rateDetail"]["rateList"]:
                info_annoy = info["anony"]
                if  info_annoy == False  :
                    #info_buyer = json.dumps(info['buyer'],ensure_ascii=False)
    #                 logging.warning(info["displayUserNick"]) 
                    data = {}
                    data['username'] = str(info["displayUserNick"].encode('utf-8'))
                    data['displayRateSum'] = info["displayRateSum"]
                    data['tamllSweetLevel'] = info["tamllSweetLevel"]
                    data['displayUserNumId'] = info["displayUserNumId"]
                    logging.warning(data['username']) 
                    
                    save_download_wangwang(data)
            
            lastPage = res_json["rateDetail"]["paginator"]["lastPage"]
            page     = res_json["rateDetail"]["paginator"]["page"]
            if lastPage - page <= 1 :
                print url
                break;
            i = i + 1
            url = "http://rate.tmall.com/list_detail_rate.htm?itemId=%s&order=1&currentPage=%s&append=0&content=1&tagId=&posi=&picture=&_ksTS=1410515765306_2008&callback=jsonp2009"%(iid,i)
            res_json=get_html(url)
#             print url
            
        except Exception,e:
            print e
            i = i + 1
            url = "http://rate.tmall.com/list_detail_rate.htm?itemId=%s&order=1&currentPage=%s&append=0&content=1&tagId=&posi=&picture=&_ksTS=1410515765306_2008&callback=jsonp2009"%(iid,i)
            res_json=get_html(url)

def save_download_wangwang(data):
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
        type =1 
        sql = "insert into wangwang_tmall ( `username`, `displayRateSum`, `tamllSweetLevel`, `displayUserNumId`, `type`, `add_time`) values(%s,%s,%s,%s,%s,'%s')" 
        param = (data['username'], data['displayRateSum'],data['tamllSweetLevel'],data['displayUserNumId'],type,int(time.time()))
        
        n = cursor.execute(sql,param)
        print n
    except:
        #nothing
        print "a"
        a =1
        
        
        
   
    
    
    
def runcrawler():
    j = 1
    num = ''
    url = "http://list.tmall.com/search_product.htm?&q=%s&sort=d"
    for k in db.nvzhuang.find():
        if k :
            j = 1;
            while j < 4 :
                try:
#                     print k['_id']
                    id =  k['_id']
#                     print fdsafdsa
                    db.nvzhuang.remove(id)
#                     print res
#                     sys.exit()
                    name = json.dumps(k['name'],ensure_ascii=False,indent=2)
                    name = name.encode('GBK').strip('\"')
#                     logging.warning(name)
                    name = urllib.quote(name)
#                     f = { 'q' : name}
#                     key = urllib.urlencode(f)
                     
                    url = "http://list.tmall.com/search_product.htm?q=%s&sort=d&s=%s"%(name,num)
                    print url
                    searchcrawler(url)
                    num = 30 * j
                    j = j +1
#                     
# #                     url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc&s=%s"%key
#                     
                    
                except Exception,e:
                    print e
                    j = j +1
#                     num = 30 * j
#                     url = "http://s.taobao.com/search?%s&commend=all&search_type=item&sourceId=tb.index&sort=sale-desc&s=%s"%(name,num)
                    
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

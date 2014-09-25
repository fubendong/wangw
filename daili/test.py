#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
#@author zcwang3@gmail.com
#@version 2010-10-18 16:47 初始做成

import urllib2
import httplib
import datetime
import logging

#目标URL
targetUrl = "http://www.baidu.com"
#取多少次访问速度的平均值
testCount = 10
proxyAddrSpeedList = []
def openUrl(proxyAddr):
    totalS = 0
    #测试，取10次平均值
    for i in range(testCount):
        try:
            starttime = datetime.datetime.now()
            #使用无验证的代理
            proxy_handler = urllib2.ProxyHandler({"http": proxyAddr})
            opener = urllib2.build_opener(proxy_handler)
            opener.open(targetUrl)
            endtime = datetime.datetime.now()
            print str(endtime - starttime) + "|" + proxyAddr
            totalS += (endtime - starttime).seconds * 1000 + (endtime - starttime).microseconds
        except urllib2.URLError,e:
            #输出错误信息，如果代理一直出错，该代理应该废弃
            print proxyAddr + "|" + str(e)
            if (str(e) == "<urlopen error (10054, 'Connection reset by peer')>" 
                or str(e) == "<urlopen error (10060, 'Operation timed out')>"
                or str(e) == "<urlopen error (10061, 'Connection refused')>"
                or str(e) == "<urlopen error (10065, 'No route to host')>"
                or str(e) == "HTTP Error 502: Bad Gateway"
                or str(e) == "HTTP Error 503: Service Unavailable"
                or str(e) == "HTTP Error 504: Gateway Time-out"
                or str(e) == "HTTP Error 404: Not Found"
                ):
                #出错就重试
                openUrl(proxyAddr)
                return
        except httplib.BadStatusLine, e:
            print proxyAddr + "|" + "httplib.BadStatusLine"
            #出错就重试
            openUrl(proxyAddr)
            return
    print totalS
    #输出10次的平均值，单位秒  
    proxyAddrSpeedList.append(str(totalS / testCount / 1000000.) + u"秒|" + proxyAddr)

#测试的代理地址列表，逗号分隔
proxyAddressArray = "http://113.118.27.159:9999,http//58.59.174.174:3128".split(",")
for p in proxyAddressArray:
    openUrl(p)
#     print u"已测试地址排序开始"
    tempAddList = []
    tempSpeedList = []
    proxyAddrSpeedList.sort()
    for p1 in proxyAddrSpeedList:
        tempSpeedList.append(p1.split("|")[0])
        tempAddList.append(p1.split("|")[1])
        print p1.split("|")[1]
        
    
    logging.warning(tempSpeedList)
#     print "speed = %s" %(",".join(tempSpeedList))
    #输出：逗号分隔的代理地址
#     print "proxyAddressArray = %s" %(",".join(tempAddList))
#     print u"已测试地址排序结束"


#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import string
import argparse
import os
import sys
import threading
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def getHtmlSummary(url):
    page = urllib.urlopen(url)
    content = page.read()
    return content

def getHtmlurl(html):
    reg = r'href="(.*?)" title'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,html)
    return urllist

def getDomains():
    domains0 = [d.strip() for d in open('factories.txt').readlines()]
    domains1 = ["mail."+d for d in domains0]
    return domains0 + domains1

def emails():
    mails=[]
    htmls=[]
    domains = getDomains()
    res = []
    for i in xrange(1, 2):
        page = str(i)
        try :
    		htmlSummary = getHtmlSummary("https://github.com/search?o=desc&p="+str(i)+"&q=mail+password&s=indexed&type=Code&utf8=✓")
    		urllist = getHtmlurl(htmlSummary)
        except:
            pass
        print "searching on the page "+page+",please wait..."
        for url in urllist[2:12]:
            print url
            try:
                htmlDetail = getHtmlSummary("https://github.com"+url)
                reg_emails1 = re.compile('[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*'+'@(?:[\w](?:[\w-]*[\w])?\.)'+'[\w](?:[\w-]*[\w])?')
                reg_emails2 = re.compile('[\w!#$%&\'*+/=?^_`{|}~-]+(?:\.[\w!#$%&\'*+/=?^_`{|}~-]+)*'+'@(?:[\w](?:[\w-]*[\w])?\.)'+'(?:[\w](?:[\w-]*[\w])?\.)'+'[\w](?:[\w-]*[\w])?')
                mail1 = reg_emails1.findall(htmlDetail)
                mail2 = reg_emails2.findall(htmlDetail)
                mail = mail1+mail2
                mails.extend(mail)
            except:
    		    pass
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    for item in mails:
        domain = item.split('@',1)[1]
        if domain in domains:
            res.append(item)
    if res:
        print res
        with open('mail_harvest.txt', 'w') as f:
            for r in res:
                print r
                f.write(r + '\n')


emails()

# coding: utf-8
import re
import urllib2
import lxml.html

def gethtml(url, data = ''):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Referer', 'http://www.icefilms.info/')
            if data == '':
                response = urllib2.urlopen(req)
            else:
                response = urllib2.urlopen(req, data)   
            print "RESPONSE"
            print response 
            htmldoc = str(response.read())
            response.close()
            return htmldoc 
        except :
            print "exception gethtml"

if __name__ == '__main__':
    #lxml.html.parse('http://example.com/').xpath('//a/@href')
    url = "http://www.cineblog01.org/category/animazione-aggiornato/"
    html = gethtml(url)
    tree = lxml.html.fromstring(html)
    videos = [2,5,0,11]
    del videos[-1]
    print videos
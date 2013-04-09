'''
Created on Apr 1, 2013

@author: ledzgio
'''
import urllib2, re
from Tools.Directories import fileExists

import resolver.resvk as resvk
import resolver.nowvideo as nowvideo
import resolver.putlocker as putlocker

def gethtml(url, data = ''):
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Referer', 'http://www.icefilms.info/')
            if data == '':
                response = urllib2.urlopen(req)
            else:
                response = urllib2.urlopen(req, data)
            htmldoc = str(response.read())
            response.close()
            return htmldoc 
        except :
            print "Exception on utils.gethtml"
            

def checkPix(filename):
        parts = filename.split('/')
        totsp = len(parts) - 1
        localfile = '/tmp/' + parts[totsp]
        if fileExists(localfile):
            pass
        else:
            url =  filename
            handler = urllib2.urlopen(url)
            if handler:
                content = handler.read()
                fileout = open(localfile, 'wb')
                fileout.write(content)
                handler.close()
                fileout.close()
        return localfile
    
def getCover(html):
        #Try to get imageshack cover from icefilms
        cover = False
        try:
            cover = re.search("""<img width=[150-300].+?src=(.+?) style='.+?'>""", html).group(1)
        except:
            #pass
            print "no icefilms cover "   
        if not cover:
            # Check for imdb link
            imdbLink = False
            try:
                imdbString = re.compile("http://www.imdb.com/title/(.+?)/", re.DOTALL).findall(html)[0]
                imdbLink = "http://www.imdb.com/title/" + imdbString + "/"
            except:
                #pass
                print "no icefilms imdblink"
            if imdbLink:
                try:
                    # get cover from imdb
                    html = gethtml(imdbLink)
                    imdbCover = re.search("""<a href=".+?" > <img height=".+?"
width=".+?"
alt=".+?Poster"
title=".+?"
src="(.+?)"
itemprop="image" />
</a>""", html).group(1)
                    print imdbLink
                    cover = imdbCover
                except:
                    pass
                    print "no imdb cover"
        if not cover:
            cover = "http://img571.imageshack.us/img571/3810/nocover.png"
        print cover        
        return cover
    
def getResolverURL(url):
    if re.match('http://.+?putlocker.com', url):
        return putlocker.resolve(url)
    elif re.match('http://.+?vk.com', url) or re.match('http://vk.com', url):
        return resvk.getURL(url)
    elif re.match('http://.+?nowvideo..+?', url):
        return nowvideo.resolve(url)
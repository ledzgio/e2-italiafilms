# coding: utf-8
'''
Created on Apr 1, 2013

@author: ledzgio
'''

import re
import lxml.html

class Bongstreaming():
    osdList = []
    max_pages = 10
    to_sort = False
    description = "\nBongStreaming.org\nFilm gratis in steaming.\nhttp://www.bongstreaming.com/"
    osdList.append((_("Ultimi arrivi"), "http://www.bongstreaming.com/"))
    osdList.append((_("Film piu visti"), "http://www.bongstreaming.com/film-piu-visti-in-streaming"))
    osdList.append((_("Film piu votati"), "http://www.bongstreaming.com/i-film-piu-votati"))
    osdList.append((_("Film al cinema"), "http://www.bongstreaming.com/film-al-cinema"))
    osdList.append((_("Film casuali"), "http://www.bongstreaming.com/film-casuali-streaming"))

    def getPages(self, html):
        try:
            pages = []                    
            return pages
        except:
            print "Exception in getPages!"
            return None
    
    def getVideos(self, html):
        try:
            videos = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'thumb\']//a')
            for div in elems:
                href = div.xpath('@href')[0]
                title = div.xpath('@title')[0]
                title = title.encode('UTF-8')
                videos.append([title, href, "IMG"])
                
            return videos
        
        except:
            print "Exception in BongStreaming - getVideos"
            return None

    def getMovie(self, html, movie_title):
        try:
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//iframe')
            movies = []
            title = ""
            for iframe in elems:
                url = iframe.xpath('@src')[0]
                if re.match('http://vk.com', url):
                    title = movie_title + " (VK)"
                    movies.append([url, title])
                    
            return movies
    
        except:
            print "Exception in BongStreaming - getMovie"
            return None
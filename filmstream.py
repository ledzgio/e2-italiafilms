# coding: utf-8
'''
Created on Apr 1, 2013

@author: ledzgio
'''

import re
import lxml.html

class Filmstream():
    osdList = []
    max_pages = 10
    to_sort = True
    description = "\nFilm-Stream.TV\nItalian film streaming.\nhttp://film-stream.tv/"
    osdList.append((_("DVD-Rip"), "http://film-stream.tv/tag/dvd-rip/"))
    osdList.append((_("Avventura"), "http://film-stream.tv/category/avventura/"))
    osdList.append((_("Azione"), "http://film-stream.tv/category/azione/"))
    osdList.append((_("Biografico"), "http://film-stream.tv/category/avventura/"))
    osdList.append((_("Comico"), "http://film-stream.tv/category/comico/"))
    osdList.append((_("Commedia"), "http://film-stream.tv/category/commedia/"))
    osdList.append((_("Documentario"), "http://film-stream.tv/category/documentario/"))
    osdList.append((_("Drammatico"), "http://film-stream.tv/category/drammatico/"))
    osdList.append((_("Fantascienza"), "http://film-stream.tv/category/fantascienza/"))
    osdList.append((_("Fantasy"), "http://film-stream.tv/category/fantasy/"))
    osdList.append((_("Featured"), "http://film-stream.tv/category/featured/"))
    osdList.append((_("Guerra"), "http://film-stream.tv/category/guerra/"))
    osdList.append((_("Horror"), "http://film-stream.tv/category/horror/"))
    osdList.append((_("Romantico"), "http://film-stream.tv/category/romantico/"))
    osdList.append((_("Storico"), "http://film-stream.tv/category/storico/"))
    osdList.append((_("Thriller"), "http://film-stream.tv/category/thriller/"))
    osdList.append((_("Serie-TV"), "http://film-stream.tv/category/serie-tv/"))
    
    def getPages(self, html):
        try:
            pages = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@id=\'wp_page_numbers\']//a')
            if len(elems) > 1:
                elems = elems[1:len(elems)-1]
            for a in elems:
                href = a.xpath('@href')[0]
                pages.append(href)
                
            if self.max_pages > 0:
                if len(pages) > self.max_pages:
                    pages = pages[:self.max_pages]
                    
            return pages

        except:
            print "Exception in getPages"
            return None
    
    def getVideos(self, html):
        #TODO: catch the image url
        try:
            videos = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'galleryitem\']//h3//a')
            for a in elems:
                href = a.xpath('@href')[0]
                title = a.text_content()
                title = title.encode('UTF-8')
                videos.append([title, href, "IMG"])
    
            return videos
        
        except:
            print "Exception in getVideos"
            return None

    def getMovie(self, html, movie_title):
        try:
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//table[@class=\'aligncenter\']//a')
            movies = []
            for a in elems:
                title = a.text_content()
                title = title.encode('UTF-8')
                url = a.xpath('@href')[0]
                if re.match('http://.+?putlocker.com', url):
                    if "Putlocker" in title:
                        title = movie_title + " (Putlocker "+title+")"
                    else:
                        title = movie_title + " ("+title+")"
                    movies.append([url, title])
                    
                elif re.match('http://.+?vk.com', url):
                    title = movie_title + " (VK "+title+")"
                    movies.append([url, title])
                    
                elif re.match('http://.+?nowvideo..+?', url):
                    if "Nowvideo" in title:
                        title = movie_title + " ("+title+")"
                    else:
                        title = movie_title + " (Nowvideo "+title+")"
                    movies.append([url, title])
                    
            return movies
    
        except:
            print "Exception in getMovie"
            return None
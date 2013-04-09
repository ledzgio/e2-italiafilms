# coding: utf-8
'''
Created on Apr 1, 2013

@author: ledzgio
'''

import re
import lxml.html

class Filmpertutti():
    osdList = []
    max_pages = 10
    to_sort = True
    description = "\nFilmPerTutti.TV\nFilm in Streaming Senza Limiti per Tutti.\nhttp://filmpertutti.tv/"
    osdList.append((_("Serie-TV"), "http://filmpertutti.tv/category/serie-tv/"))
    osdList.append((_("Animazione"), "http://filmpertutti.tv/category/animazione/"))
    osdList.append((_("Avventura"), "http://filmpertutti.tv/category/avventura/"))
    osdList.append((_("Azione"), "http://filmpertutti.tv/category/azione/"))
    osdList.append((_("Comici"), "http://filmpertutti.tv/category/comico/"))
    osdList.append((_("Biografico"), "http://filmpertutti.tv/category/biografico/"))
    osdList.append((_("Commedia"), "http://filmpertutti.tv/category/commedia/"))
    osdList.append((_("Documentario"), "http://filmpertutti.tv/category/documentario/"))
    osdList.append((_("Drammatico"), "http://filmpertutti.tv/category/drammatico/"))
    osdList.append((_("Fantascienza"), "http://filmpertutti.tv/category/fantascienza/"))
    osdList.append((_("Fantasy"), "http://filmpertutti.tv/category/fantasy/"))
    osdList.append((_("Gangster"), "http://filmpertutti.tv/category/gangster/"))
    osdList.append((_("Guerra"), "http://filmpertutti.tv/category/guerra/"))
    osdList.append((_("Horror"), "http://filmpertutti.tv/category/horror/"))
    osdList.append((_("Musical"), "http://filmpertutti.tv/category/musicale/"))
    osdList.append((_("Polizioesco"), "http://filmpertutti.tv/category/poliziesco/"))
    osdList.append((_("Romantico"), "http://filmpertutti.tv/category/romantico/"))
    osdList.append((_("Storico"), "http://filmpertutti.tv/category/storico/"))
    osdList.append((_("Thriller"), "http://filmpertutti.tv/category/thriller/"))
    osdList.append((_("Western"), "http://filmpertutti.tv/category/western/"))
    
    def getPages(self, html):
        try:
            pages = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'Navi\']//a')
            if len(elems) > 1:
                elems = elems[:len(elems)-2]
                
            for a in elems:
                href = a.xpath('@href')[0]
                if len(elems) > 2:
                    pages.append(href)

            if self.max_pages > 0:
                if len(pages) > self.max_pages:
                    pages = pages[:self.max_pages]
                    
            return pages
        
        except:
            print "Exception in Filmpertutti - getPages"
            return None

    
    def getVideos(self, html):
        try:
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'xboxcontent\']//a')
            videos = []
            for a in elems:
                href = a.xpath('@href')[0]
                title = a.xpath('@title')[0]
                title = title.encode('UTF-8')
                videos.append([title, href, "IMG"])
            
            return videos
        
        except:
            print "Exception in Filmpertutti - getVideos"
            return None
    
    def getMovie(self, html, movie_title):
        try:
            
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//iframe')
            movies = []
            for iframe in elems:
                title = ""
                url = iframe.xpath('@src')[0]
                if re.match('http://vk.com', url):
                    title = movie_title + " (VK)"
                    movies.append([url, title])
                    
            elems = tree.xpath('//a[@target=\'_blank\']')
            for a in elems:
                url = a.xpath('@href')[0]
                title = a.text_content()
                title = title.encode('UTF-8')
                if re.match('http://.+?putlocker.com', url):
                    if not "PutLocker" in title:
                        title = movie_title + " (Putlocker "+title+")"
                    else:
                        title = movie_title +" ("+title+")"
    
                    movies.append([url, title])
                elif re.match('http://.+?nowvideo..+?', url):
                    if not "NowVideo" in title:
                        title = movie_title + " (Nowvideo "+title+")"
                    else:
                        title = movie_title +" ("+title+")"
    
                    movies.append([url, title])
            
            return movies
        except:
            print "Exception in getMovie"
            return None
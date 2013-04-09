# coding: utf-8
'''
Created on Apr 1, 2013

@author: ledzgio
'''

import re
import lxml.html

class Cineblog01():
    osdList = []
    max_pages = 10
    to_sort = True
    description = "\nCineblog01.org\nFilm gratis in steaming.\nhttp://www.cineblog01.org/"
    #osdList.append((_("Ultimi 100 Film aggiunti"), "http://www.cineblog01.org/lista-film-ultimi-100-film-aggiunti/"))
    osdList.append((_("Animazione"), "http://www.cineblog01.org/category/animazione-aggiornato/"))
    osdList.append((_("Avventura"), "http://www.cineblog01.org/category/avventura-aggiornato/"))
    osdList.append((_("Azione"), "http://www.cineblog01.org/category/azione-aggiornato/"))
    osdList.append((_("Biografico"), "http://www.cineblog01.org/category/biografico-aggiornato/"))
    osdList.append((_("Comico"), "http://www.cineblog01.org/category/comico-aggiornato/"))
    osdList.append((_("Commedia"), "http://www.cineblog01.org/category/commedia-aggiornato/"))
    osdList.append((_("Crimine"), "http://www.cineblog01.org/category/crimine-aggiornato/"))
    osdList.append((_("Documentario"), "http://www.cineblog01.org/category/documentario-aggiornato/"))
    osdList.append((_("Drammatico"), "http://www.cineblog01.org/category/drammatico-aggiornato/"))
    osdList.append((_("Erotico"), "http://www.cineblog01.org/category/erotico-aggiornato/"))
    osdList.append((_("Fantascienza"), "http://www.cineblog01.org/category/fantascienza-aggiornato/"))
    osdList.append((_("Fantasy"), "http://www.cineblog01.org/category/fantasy-fantastico-aggiornato/"))
    osdList.append((_("Gangster"), "http://www.cineblog01.org/category/gangster-aggiornato/"))
    osdList.append((_("Grottesco"), "http://www.cineblog01.org/category/grottesco-aggiornato/"))
    osdList.append((_("Guerra"), "http://www.cineblog01.org/category/guerra-aggiornato/"))
    osdList.append((_("Horror"), "http://www.cineblog01.org/category/horror-aggiornato/"))
    osdList.append((_("Musical"), "http://www.cineblog01.org/category/musical-aggiornato/"))
    osdList.append((_("Noir"), "http://www.cineblog01.org/category/noir-aggiornato/"))
    osdList.append((_("Poliziesco"), "http://www.cineblog01.org/category/poliziesco-aggiornato/"))
    osdList.append((_("Sentimentale"), "http://www.cineblog01.org/category/sentimentale-aggiornato/"))
    osdList.append((_("Storico"), "http://www.cineblog01.org/category/storico-aggiornato/"))
    osdList.append((_("Thriller"), "http://www.cineblog01.org/category/thriller-aggiornato/"))
    osdList.append((_("Western"), "http://www.cineblog01.org/category/western-aggiornato/"))
    osdList.append((_("Serie-TV"), "http://www.cineblog01.info/serietv/"))
    
    def getPages(self, html):
        try:
            pages = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@id=\'wp_page_numbers\']//a')
            if len(elems) > 1:
                elems = elems[1:len(elems)-2]
            for a in elems:
                href = a.xpath('@href')[0]
                pages.append(href)
                
            if self.max_pages > 0:
                if len(pages) > self.max_pages:
                    pages = pages[:self.max_pages]
                    
            return pages
        except:
            print "Exception in getPages!"
            return None
    
    def getVideos(self, html):
        try:
            videos = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@id=\'post-title\']//a')
            for a in elems:
                href = a.xpath('@href')[0]
                title = a.text_content()
                title = title.encode('UTF-8')
                videos.append([title, href, "IMG"])
    
            return videos
        
        except:
            print "Exception in Cineblog01 - getVideos"
            return None

    def getMovie(self, html, movie_title):
        try:
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//table[@bgcolor=\'#F7F7F7\']//a')
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
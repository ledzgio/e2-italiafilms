# coding: utf-8
'''
Created on Apr 1, 2013

@author: giorgio
'''

import lxml.html
import re

class Terrafilms():
    osdList = []
    description = "\nTerraFilms.TV\nCinema online. Guarda film online e guarda film nuovi gratis.\nhttp://terrafilms.tv/"
    max_pages = 10
    to_sort = True
    osdList.append((_("Animazione"), "http://terrafilms.tv/animazione"))
    osdList.append((_("Avventura"), "http://terrafilms.tv/avventura"))
    osdList.append((_("Azione"), "http://terrafilms.tv/azione"))
    osdList.append((_("Commedia"), "http://terrafilms.tv/commedia"))
    osdList.append((_("Concerti"), "http://terrafilms.tv/concerti"))
    osdList.append((_("Documentario"), "http://terrafilms.tv/documentario"))
    osdList.append((_("Drammatico"), "http://terrafilms.tv/drammatico"))
    osdList.append((_("Fantascienza"), "http://terrafilms.tv/fantascienza"))
    osdList.append((_("Horror"), "http://terrafilms.tv/horror"))
    osdList.append((_("Musical"), "http://terrafilms.tv/musical"))
    osdList.append((_("Romantico"), "http://terrafilms.tv/romantico"))
    osdList.append((_("Sportivo"), "http://terrafilms.tv/sportivo"))
    osdList.append((_("Thriller"), "http://terrafilms.tv/thriller"))
    osdList.append((_("Serie-TV"), "http://terrafilms.tv/serie-tv"))
    
    def getPages(self, html):
        try:
            pages = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'navigation\']//a')
            if len(elems) > 1:
                elems = elems[:len(elems)-1]
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
        try:
            videos = []
            tree = lxml.html.fromstring(html)
            elems = tree.xpath('//div[@class=\'prew-film-content\']//a')
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
            elems = tree.xpath('//iframe')
            movies = []
            for iframe in elems:
                url = iframe.xpath('@src')[0]
                title = iframe.text_content()
                title = title.encode('UTF-8')
                if re.match('http://vk.com', url):
                    if title:
                        title = movie_title + " (VK "+title+")"
                    else:
                        title = movie_title + " (VK)"
                    movies.append([url, title])
                    
            return movies
        except:
            print "Exception in getMovie"
            return None
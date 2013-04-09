# coding: utf-8
###########################################################################
##################### By:ledzgio ##########################################
##################### Thanks to subixonfire  www.satforum.me ##############
###########################################################################
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer as MP_parent
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from ServiceReference import ServiceReference
from enigma import eServiceReference, eConsoleAppContainer, ePicLoad, getDesktop, eServiceCenter, loadPic
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Pixmap import Pixmap
from Screens.InputBox import InputBox
from Components.Label import Label
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from cookielib import CookieJar
from filmstream import Filmstream
from terrafilms import Terrafilms
from filmpertutti import Filmpertutti
from cineblog01 import Cineblog01
from bongstreaming import Bongstreaming
import os
import utils
import socket
from twisted.internet.defer import returnValue
socket.setdefaulttimeout(300) #in seconds


###########################################################################

class ItaliaFilms(Screen):
    wsize = getDesktop(0).size().width()
    hsize = getDesktop(0).size().height()
    print "wsize " + str(wsize)
    plugin_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    
    skin = """
        <screen flags="wfNoBorder" position="0,0" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="ItaliaFilms" >
        <ePixmap alphatest="on" pixmap=\"""" + plugin_dir + """main.png" position="0,0" size=\"""" + str(wsize) + "," + str(hsize) + """\"  zPosition="-2"/>
            <widget name="myMenu" position="210,60" size=\"""" + str((wsize/2)+100) + "," + str(hsize - 260) + """\" scrollbarMode="showOnDemand" font="Regular;20"/>
            <widget name="myText" position="210,505" size=\"""" + str((wsize/2)+100) + "," + str(160) +"""\" font="Regular;19"/>
        </screen>"""
        #<widget name="myCover" position="200,390" size="720,380" zPosition="1" alphatest="on" />
            
    fileTitle1 = ""
    fileTitle2 = ""
    plugin_description = "\nItaliaFilms, i migliori film dai migliori siti di streaming online."
    about_text = "ItaliaFilms by ledzgio\nVersione 1.0 beta\nhttps://github.com/ledzgio/e2-italiafilms\nThanks to subixonfire"
    theFunc = "main"
    downDir = "/mnt/hdd"
    mainobj = []
    lastVideosList = []
    osdList = []
    osdList.append((_("Cineblog01.org"), Cineblog01()))
    osdList.append((_("BongStreaming.org"), Bongstreaming()))
    osdList.append((_("FilmPerTutti.tv"), Filmpertutti()))
    osdList.append((_("Film-Stream.tv"), Filmstream()))
    osdList.append((_("Terrafilms.tv"), Terrafilms()))
    #osdList.append((_("About"), "about"))
    historyList = []
    historyInt = 0
        
    def __init__(self, session):
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(self.osdList)
        self["myText"] = Label()
        self["myText"].setText(self.plugin_description)
        self["myActionMap"] = ActionMap(["SetupActions","ColorActions"],
        {
        "ok": self.go,
        "cancel": self.cancel,
        "green": self.download,
        "yellow": self.downdir
        }, -1)
        
           
    def go(self):
        returnTitle = self["myMenu"].l.getCurrentSelection()[0]
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        returnIndex = self["myMenu"].getSelectedIndex()
        
        if not self.theFunc == "host":
            try:
                self.historyList[int(self.historyInt)] = [self.theFunc, self.osdList, returnIndex]
            except:    
                self.historyList.append([self.theFunc, self.osdList, returnIndex])
                
            self.historyInt = self.historyInt + 1
            
        if self.theFunc == "main":
            print ">>>>>>>>>>>>main"
            print self.theFunc
            if not returnValue == "about":
                self.mainobj = returnValue
                self["myMenu"].setList(returnValue.osdList)
                self["myText"].setText(self.mainobj.description)
                self.theFunc = "genres"
            else:
                self.askForWord(self.about_text)
        
        elif self.theFunc == "genres":
            if not returnValue == "about":
                print ">>>>>>>>>>>>genres"
                print self.theFunc
                url = returnValue
                html = utils.gethtml(url)
                first_page = [returnValue]
                print url
                pages = self.mainobj.getPages(html)
                if pages == None:
                    return
                pages = first_page + pages
                videos = []
                if pages:
                    for page in pages:
                        url = page
                        print "URL >>>>>>>>>: "+url
                        html = utils.gethtml(url)
                        vids_tmp = self.mainobj.getVideos(html)
                        if vids_tmp:
                            videos = videos + vids_tmp

                if not videos:
                    return
                
                self.osdList = [(x[0],x[1],x[2]) for x in videos]
                if self.mainobj.to_sort:
                    self.osdList.sort()
                self.lastVideosList = self.osdList
                self["myMenu"].setList(self.osdList)
                num_videos = len(videos)
                self["myText"].setText(self.mainobj.description + "\n\nSono presenti "+str(num_videos)+" film nella categoria "+returnTitle)
                self.theFunc = "movie"

        elif self.theFunc == "movie":
            print self.theFunc
            url = returnValue
            print url
            html = utils.gethtml(url)
            vklink = self.mainobj.getMovie(html, returnTitle)
            if vklink == None:
                return
            
            self["myText"].setText("\nTitolo Film: "+returnTitle+"\n"+"URL: "+url)
            self.osdList = []
            if vklink:
                tmpindex = 0
                for link in vklink:
                    self.osdList.append((_(link[1] + " / " + str(tmpindex)), link[0]))
                    tmpindex = tmpindex + 1

                self["myMenu"].setList(self.osdList)
                self.theFunc = "host"
            else:
                print "#### NO VIDEO LINKS FOUND"
                print url
                text = str(self["myText"].getText()) + "\n\nSpiacente, nessun servizio di streaming trovato!"
                self["myText"].setText(text)
                print self.historyInt
                self.theFunc = "movie"
            
        elif self.theFunc == "show":
            pass
        
        
        elif self.theFunc == "episode":
            pass
        
            
        elif self.theFunc == "host":
            print ">>>>>>>>>>>>host"
            print self.theFunc
            print returnValue
            returnUrl = returnValue
            returnUrl = utils.getResolverURL(returnUrl)
        
            if returnUrl:       
                fileRef = eServiceReference(4097,0,returnUrl)
                fileRef.setData(2,10240*1024)
                fileRef.setName(returnTitle)
                self.session.open(MoviePlayer, fileRef)
            else:
                return
                     
        self["myMenu"].moveToIndex(0)
        print "HOST"
        print self.theFunc        
        
    def download(self):
        returnTitle = self["myMenu"].l.getCurrentSelection()[0]
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        if self.theFunc == "file":
            command = "wget \"" + returnValue.replace("&amp;", "&").replace(" ", "%20") + "\" -O \"" + self.downDir + "/" + returnTitle + "\""
            print "burek: " + command
            os.system(command)    
    
    def downdir(self):
        if self.downDir == "/mnt/hdd":
            self.downDir = "/mnt/usb"
            self.session.open(MessageBox,_("Download all to /mnt/usb !"), MessageBox.TYPE_INFO)
        else:
            self.downDir = "/mnt/hdd"
            self.session.open(MessageBox,_("Download all to /mnt/hdd !"), MessageBox.TYPE_INFO)
        
        #self.session.open(self, MessageBox,_("Download all to " + downDir + " !"), MessageBox.TYPE_INFO)        
    
    def cancel(self):
        print "######## CANCEL #######"
        print self.theFunc
        print self.historyInt
        if self.historyInt == 1 or self.historyInt == 3:
            self.historyInt = self.historyInt - 1
            self.theFunc = self.historyList[self.historyInt][0]
            self.osdList = self.historyList[self.historyInt][1]
            self["myMenu"].setList(self.osdList)
            self["myMenu"].moveToIndex(self.historyList[self.historyInt][2])
            if self.historyInt == 0:
                self["myText"].setText(self.plugin_description)
            else:
                self["myText"].setText(""+self.mainobj.description)

        elif self.historyInt == 2:
            self.historyInt = self.historyInt - 1
            self.theFunc = self.historyList[self.historyInt][0]
            self.osdList = self.historyList[self.historyInt][1]
            self["myMenu"].setList(self.mainobj.osdList)
            self["myMenu"].moveToIndex(self.historyList[self.historyInt][2])

        elif self.historyInt > 3:
            self.historyInt = self.historyInt - 1
            self.theFunc = self.historyList[self.historyInt][0]
            self.osdList = self.historyList[self.historyInt][1]
            self["myMenu"].setList(self.lastVideosList)
            self["myMenu"].moveToIndex(self.historyList[self.historyInt][2])
            
        else:    
            self.close(None)

    def askForWord(self, word):
        if word is None:
            pass
        else:
            self.session.open(MessageBox,_(word), MessageBox.TYPE_INFO)
            
###########################################################################

def main(session, **kwargs):
    
    burek = session.open(ItaliaFilms)
        
                  
###########################################################################    

class MoviePlayer(MP_parent):
    def __init__(self, session, service):
        self.session = session
        self.WithoutStopClose = False
        
        MP_parent.__init__(self, self.session, service)

    def leavePlayer(self):
        self.is_closing = True
        self.close()

    def leavePlayerConfirmed(self, answer):
        self.is_closing = True
        self.close

    def doEofInternal(self, playing):
        if not self.execing:
            return
        if not playing :
            return
        self.leavePlayer()

    def showMovies(self):
        self.WithoutStopClose = False
        self.close()

    def movieSelected(self, service):
        self.leavePlayer(self.de_instance)

    def __onClose(self):
        if not(self.WithoutStopClose):
            self.session.nav.playService(self.lastservice)	
###########################################################################

def Plugins(**kwargs):
    return PluginDescriptor(
        name="ItaliaFilms",
        description="taliaFilms, i migliori film dai siti italiani di streaming online.",
        where = [ PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU ],
        icon="./icon.png",
        fnc=main)
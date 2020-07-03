import os, sys, re
import xbmc, xbmcaddon, xbmcgui
import json, urllib2

__addon__ = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonPath__ = __addon__.getAddonInfo('path')
__addonResourcePath__ = xbmc.translatePath(os.path.join(__addonPath__, 'resources', 'lib'))
__addonIconFile__ = xbmc.translatePath(os.path.join(__addonPath__, 'icon.png'))
sys.path.append(__addonResourcePath__)

from prefsettings import settings

settings = settings()

LOG_NONE = 0
LOG_ERROR = 1
LOG_INFO = 2
LOG_DEBUG = 3

class Main:
    def __init__(self):
        self._init_vars()
        if (not settings.service_enabled):
            log(LOG_INFO, "Service not enabled")

        settings.readPrefs()
        self._daemon()

    def _init_vars( self ):
        self.Monitor = Kodi_Monitor()
        self.Player = Kodi_Player()        

    def _daemon( self ):
        while (not xbmc.abortRequested):
            xbmc.sleep(500)
           
class Kodi_Monitor(xbmc.Monitor):
  def __init__(self):
      xbmc.Monitor.__init__(self)
        
  def onSettingsChanged(self):
      settings.init()
      settings.readPrefs()

class Kodi_Player(xbmc.Player):
    
    def __init__(self, *args):
       xbmc.Player.__init__(self, *args)
        
    def onAVStarted(self):
        debug('entering onAVStarted')
        if self.isPlayingVideo():
            ifttt(settings.eventStart)
            
    def onPlayBackPaused(self):
        debug('entering onPlayBackPaused')
        if self.isPlayingVideo():
            ifttt(settings.eventPause)
            
    def onPlayBackResumed(self):
        debug('entering onPlayBackResumed')
        if self.isPlayingVideo():
            ifttt(settings.eventResume)

    def onPlayBackStopped(self):
        debug('entering onPlayBackStopped')
        ifttt(settings.eventStop)

def ifttt(event):
    urllib2.urlopen(settings.iftttUrl + event + settings.iftttPath + settings.iftttKey).read()

def debug(msg, *args):
    try:
        txt=u''
        msg=unicode(msg)
        for arg in args:
            if type(arg) == int:
                arg = unicode(arg)
            if type(arg) == list:
                arg = unicode(arg)
            txt = txt + u"/" + arg
        if txt == u'':
            xbmc.log(u"LPM: {0}".format(msg).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
        else:
            xbmc.log(u"LPM: {0}#{1}#".format(msg, txt).encode('ascii','xmlcharrefreplace'), xbmc.LOGDEBUG)
    except:
        print "LPM: Error in Debugoutput"
        print msg
        print args

    
def log(level, msg):
    if level <= settings.logLevel:
        if level == LOG_ERROR:
            l = xbmc.LOGERROR
        elif level == LOG_INFO:
            l = xbmc.LOGINFO
        elif level == LOG_DEBUG:
            l = xbmc.LOGDEBUG
        xbmc.log("[Language Preference Manager]: " + str(msg), l)

if ( __name__ == "__main__" ):
    log(LOG_INFO, 'service {0} version {1} started'.format(__addonname__, __addonversion__))
    main = Main()
    log(LOG_INFO, 'service {0} version {1} stopped'.format(__addonname__, __addonversion__))

#      Baris Ata
#   <brsata@gmail.com>
#       Kocaeli Universitesi
#
#

import appuifw
import e32
import globalui
import time
import urllib
import random
import graphics
from graphics import Image
from key_codes import *
import sys
import positioning
import math
import os

APP_LOCK = e32.Ao_lock()
DEFAULT_ZOOM = 14
GMAPS_KEY = "ABQIAAAAuRDNlyhItuuePzKf3qKzehTkHcIfiZf7NqfRPrxZiOraXnGCTBSu41SbT9Wo1zf7bwWyRUtltyMV7Q"
GOOGLE_IMAGE_FORMAT = "jpg"
EXTENSIONS = {"gif": "gif", "jpg": "jpg", "jpg-baseline": "jpg",
              "png8": "png", "png32": "png"}
TEMP_FILE = u"e:\\tmp_map."+EXTENSIONS[GOOGLE_IMAGE_FORMAT]
MIN_ZOOM = 0
MAX_ZOOM = 19
GMAPS_URL = "http://maps.google.com/staticmap?center=%f,%f&format="+GOOGLE_IMAGE_FORMAT+"&zoom=%d&size=%dx%d&maptype=%s&markers=%s&key="+GMAPS_KEY


class GoogleMaps:
        def __init__(self, (width, height), mapType="mobile", markerColor="green",
                 markerSize="small"):
                self.width = width
                self.height = height
                self.mapType = mapType
                self.markerColor = markerColor
                self.markerSize = markerSize
     
        def makeMarkerString(self, positions):
                str = ""
                for (lat, lon) in positions:
                        str = str + ("%f,%f,%s%s|" % (lat, lon, self.markerSize,
                                                                                  self.markerColor))
                return str
        
        # Set the width and height for all subsequent requests.
        def setImageSize(self, pos):
                width, height = pos
                self.width = width
                self.height = height
        
        # Get the map centered at centerLatLon, at zoom factor zoom,
        # with markers at positions markerPositions, which may be empty.
        def getMapImage(self, centerLatLon, zoom, markerPositions):
                
                lat, lon = centerLatLon
                url = (GMAPS_URL % (lat, lon, zoom, self.width, self.height,
                                   self.mapType, self.makeMarkerString(markerPositions)))
                
                file, ignoredHeaders = urllib.urlretrieve(url, TEMP_FILE)
                
                return Image.open(file)     
                
                
class FileSelector:
    def __init__(self,dir=".",ext='.jpg'):
        self.dir = dir
        self.ext = ext
        self.files = {}
 
        def iter(fileselector,dir,files):
            for file in files:
                b,e = os.path.splitext(file)
                if e == fileselector.ext:
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
 
        os.path.walk(self.dir,iter,self)
        self.sortedkeys = self.files.keys()
        self.sortedkeys.sort()
 
    def GetKeys(self):
        return self.sortedkeys
 
    def GetFile(self,index):
        return self.files[self.sortedkeys[index]]
 
 

 
 

class Application(object):
        def __init__(self):
                appuifw.app.title = u"Mapys"
                appuifw.app.screen = "normal"
                self.app_lock = e32.Ao_lock()
                appuifw.app.exit_key_handler = self.quit
                appuifw.app.menu = [(u"Exit", self.quit)]
                #search_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 16458,16459)
                world_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif",16544,16545)
                folder_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17506, 17507)
                about_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 16588, 16589)
                self.items = [(u"My Position",u"Learn your position",world_icon),
                                                           (u"Favourites",u"Saved locations",folder_icon),
                                                           (u"About",u"About Mapys",about_icon)]
                self.mylistbox = appuifw.Listbox(self.items,self.handle_selection)
                appuifw.app.body = self.mylistbox
                self.__menuMain = appuifw.app.menu
                self.__bgMain = appuifw.app.body

 
        def handle_selection(self):
                
                if (self.items[self.mylistbox.current()][0] == "My Position"):
                        self.my_position()
                if (self.items[self.mylistbox.current()][0] == "Find Places"):
                        self.find_places()
                if (self.items[self.mylistbox.current()][0] == "Favourites"):
                        self.favourites()
                if (self.items[self.mylistbox.current()][0] == "About"):
                        self.about()
        
        
        def my_position(self):
                
                appuifw.app.menu = [(u"Save Map",self.saveMap),(u"Back",self.back),(u"Exit",self.quit)]
                mapFactory = GoogleMaps((360,360), mapType="satellite")
                image = None
                canvas = None
                zoom = [DEFAULT_ZOOM]
                
                def setZoom(newValue):
                        zoom[0] = newValue
                def getZoom():
                        return zoom[0]
                def drawImage(rect):
                        canvas.blit(image)
                        canvas.text(((10, 20)),
                                        u"Zoom: %d%%" % ((100.0 * getZoom()) / MAX_ZOOM))
                
                def handleEvent(event):
                        try:
                                if event["type"] == appuifw.EEventKeyUp:
                                        if event["scancode"] == EScancodeUpArrow:
                                        # zoom in (larger factor)
                                                setZoom(min(MAX_ZOOM, getZoom() + 1))
                                        elif event["scancode"] == EScancodeDownArrow:
                                        # zoom out (smaller factor)
                                                setZoom(max(MIN_ZOOM, getZoom() - 1))
                        except:
                                pass
                def initialize_gps():
                        appuifw.note(u'Intializing GPS')
                        
                        global gps_data
                        gps_data = {'satellites':{'horizontal_dop': 0.0, 'used_satellites': 0, 'vertical_dop': 0.0, 'time': 0.0,'satellites': 0,'time_dop':0.0},
                                                        'position':{'latitude': 0.0, 'altitude': 0.0, 'vertical_accuracy': 0.0, 'longitude': 0.0,'horizontal_accuracy': 0.0},
                                                        'course': {'speed': 0.0, 'heading': 0.0, 'heading_accuracy': 0.0, 'speed_accuracy': 0.0}}
                        try:
                # Set requesters - it is mandatory to set at least one
                                
                                positioning.set_requestors([{"type":"service","format":"application","data":"gps_app"}])
                # Request for a fix every 0.5 seconds
                                positioning.position(course=1,satellites=1,callback=cb_gps, interval=500000,partial=0)
                # Sleep for 3 seconds for the intitial fix
                                e32.ao_sleep(5)
                        except:
                                appuifw.note(u'Problem with GPS','error')
                
                def cb_gps(event):
                        global gps_data
                        gps_data = event
                
                def stop_gps():
                        try:
                                positioning.stop_position()
                                appuifw.note(u'GPS stopped','error')
                        except:
                                appuifw.note(u'Problem with GPS','error')
                
                #initialize G
               
                initialize_gps()
                
                canvas = appuifw.Canvas(redraw_callback=drawImage,
                                                        event_callback=handleEvent)
                appuifw.app.body = canvas
                
                
                oldLatLon = None
                while True:
                        latLon = gps_data['position']['latitude'], gps_data['position']['longitude']
                        if oldLatLon == latLon:
                                                        e32.ao_sleep(1)
                                                        continue
                                                        
                        oldLatLon = latLon
                        image = mapFactory.getMapImage(latLon, getZoom(), (latLon,))
                        drawImage(())
                self.app_lock.wait()
                        
                
        def favourites(self):
                def handle_redraw(rect):
                        canvas.blit(img)
                try:
                    selector = FileSelector("e:\\myPlaces",".jpg")
                    index = appuifw.selection_list(selector.GetKeys())
                except:
                    appuifw.note(u"File does not exist", "info")
                img=Image.open(selector.GetFile(index))
                canvas=appuifw.Canvas(redraw_callback=handle_redraw)
                appuifw.app.body=canvas
                appuifw.app.menu = [(u"Back",self.back),(u"Exit", self.quit)]
                
        def about (self):
                pass
               
        def back(self):
                        appuifw.app.menu = self.__menuMain
                        appuifw.app.body = self.__bgMain
        def saveMap(self):
                        i=0
                        for f in os.listdir("e:"):
                                if f=="myPlaces":
                                        i=1
                                        
                        if i==0:
                                os.mkdir("e:\\myPlaces")
                                
                        word = appuifw.query(u"Enter a name for this map", 'text')
                        source="e:\\tmp_map.jpg"
                        target="e:\\myPlaces\\"+word+".jpg"
                        
                        try:
                                                        e32.file_copy(target,source)
                                                        appuifw.note(u'Map Saved','info')
                                                       
                        except:
                                                        appuifw.note(u'Map Could Not Saved','info')
                                                        
       
                        
        def quit(self):
                self.app_lock.signal()
                appuifw.app.set_exit()  
                
        def loop(self):

                self.app_lock.wait()
                
if __name__ == "__main__":
    mapys = Application()
    mapys.loop()
   
        
        

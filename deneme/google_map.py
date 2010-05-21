import urllib
from graphics import Image
import random
import e32, appuifw
from graphics import Image
import graphics
from key_codes import *
import sys
import positioning
import math
APP_LOCK = e32.Ao_lock()
DEFAULT_ZOOM = 8
GMAPS_KEY = "ABQIAAAAuRDNlyhItuuePzKf3qKzehTkHcIfiZf7NqfRPrxZiOraXnGCTBSu41SbT9Wo1zf7bwWyRUtltyMV7Q"
GOOGLE_IMAGE_FORMAT = "jpg"
EXTENSIONS = {"gif": "gif", "jpg": "jpg", "jpg-baseline": "jpg",
              "png8": "png", "png32": "png"}
TEMP_FILE = u"e:\\tmp"+str(random.randint(0, 10000))+"."+EXTENSIONS[GOOGLE_IMAGE_FORMAT]
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
        self.tmp_file = u'e:\\test.png'
        self.offset = 268435456
        self.radius = self.offset / math.pi
        self.api_key=GMAPS_KEY
    def makeMarkerString(self, positions):
        str = ""
        for (lat, lon) in positions:
            str = str + ("%f,%f,%s%s|" % (lat, lon, self.markerSize,
                                          self.markerColor))
        return str
    def setImageSize(self, pos):
        width, height = pos
        self.width = width
        self.height = height
    def getMapImage(self, centerLatLon, zoom, markerPositions):
        lat, lon = centerLatLon
        url = (GMAPS_URL % (lat, lon, zoom, self.width, self.height,
               self.mapType, self.makeMarkerString(markerPositions)))
        file, ignoredHeaders = urllib.urlretrieve(url, TEMP_FILE)
        return Image.open(file)
    def retrieveStaticImage(self, width, height, lng, lat, zoom, format):
        urllib.urlretrieve(self.getMapUrl(width, height,
                                          lng, lat, zoom,
                                          format), self.tmp_file)
        return graphics.Image.open(self.tmp_file)
    def getGeocodeError(self, errorCode):
        dictError = {400: "Bad request",
                     500: "Server error",
                     601: "Missing query",
                     602: "Unknown address",
                     603: "Unavailable address",
                     604: "Unknown directions",
                     610: "Bad API key",
                     620: "Too many queries"}
 
        return dictError.get(errorCode, "Generic error")
 
    def getGeocodeUrl(self, url):
        urlbase = "http://maps.google.com/maps/geo"
        return "%(urlbase)s?%(params)s" % {'params': urllib.urlencode({'q':url,
                                         'output':'csv',
                                         'key':self.api_key
                                        }),
             'urlbase': urlbase}
 
    def getMapUrl(self, width, height, lng, lat, zoom, format):
        urlbase = "http://maps.google.com/staticmap"
        params = ["center=%(lat)s,%(lng)s" % {"lat":lat,"lng":lng}]
        params.append("format=%(format)s" % {"format":format})
        params.append("zoom=%(zoom)s" % {"zoom":zoom})
        params.append("size=%(width)sx%(height)s" % {"width":width,"height":height})
        params.append("key=%(api_key)s" % {"api_key":self.api_key})
        return  "%(urlbase)s?%(params)s" % {"urlbase":urlbase,"params":"&".join(params)}
 
    def adjust(self, lat, lng, deltaX, deltaY, z):
        return (self.XToL( self.LToX(lat) + (deltaX<<(21-z))),
               self.YToL(self.LToY(lng) + (deltaY<<(21-z))))
 
    def LToX(self, x):
        return round(self.offset + self.radius * math.radians(x))
 
    def LToY(self, y):
        return round( self.offset - self.radius *
            (math.log((
            (1 + math.sin(math.radians(y)))
            /
            (1 - math.sin(math.radians(y)))
            )
        )) / 2)
 
    def XToL(self, x):
        return math.degrees((round(x) - self.offset) / self.radius)
 
    def YToL(self, y):
        return math.degrees(math.pi / 2 - 2 * (
                math.atan(
                    math.exp(((round(y)-self.offset)/self.radius))
                )
            ))
def main():
    appuifw.app.screen='normal'
    appuifw.exit_key_handler = lambda:APP_LOCK.signal()
    mapFactory = GoogleMaps((360,640), mapType="satellite")
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
            e32.ao_sleep(3)
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
 
#initialize GPS
    initialize_gps()
 
    canvas = appuifw.Canvas(redraw_callback=drawImage,
                            event_callback=handleEvent)
    appuifw.app.body = canvas
 
    oldLatLon = None
    while True:
        latLon = gps_data['position']['latitude'], gps_data['position']['longitude']
        if oldLatLon == latLon:
            e32.ao_sleep(3)
            continue
        oldLatLon = latLon
        image = mapFactory.getMapImage(latLon, getZoom(), (latLon,))
        drawImage(())
 
    APP_LOCK.wait()
 
if __name__ == "__main__":
    main()

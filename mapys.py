#
#
#	Baris Ata
#   <brsata@gmail.com>
#	Kocaeli Universitesi
#
#

####
#  imports...
####
# -*- coding: utf-8 -*-
import appuifw
import e32
import globalui
import time
import urllib
import random
import graphics
from key_codes import *
import sys
import positioning
import math

class Application(object):
	def __init__(self):
		appuifw.app.title = u"Mapys"
		appuifw.app.screen = "normal"
		self.app_lock = e32.Ao_lock()
		appuifw.app.exit_key_handler = self.quit
		appuifw.app.menu = [(u"Exit", self.quit)]
		#map_icon = appuifw.Icon(u"z:\\resource\apps\avkon2.mbm",16412, 16413)
		#map_icon2 = appuifw.Icon(u"z:\\resource\apps\avkon2.mbm", 16424, 16425)
		self.items = [(u"My Position"), (u"Find Places"),(u"Favurites"),(u"Help"),(u"About")]
		self.mylistbox = appuifw.Listbox(self.items)
		appuifw.app.body = self.mylistbox


	def handle_selection(self):
		appuifw.note(u" has been selected.", 'info')
	
	def quit(self):
		self.app_lock.signal()
		appuifw.app.set_exit()	
		
	def loop(self):

		self.app_lock.wait()
		
if __name__ == "__main__":
    mapys = Application()
    mapys.loop()
   
	
	

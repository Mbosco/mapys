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
		search_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 16458,16459)
		world_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif",16544,16545)
		folder_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 17506, 17507)
		about_icon = appuifw.Icon(u"Z:\\resource\\apps\\avkon2.mif", 16588, 16589)
		self.items = [(u"My Position",u"Learn your position",world_icon), 
						(u"Find Places",u"Find a location",search_icon),
						(u"Favourites",u"Saved locations",folder_icon),
						(u"About",u"About Mapys",about_icon)]
		self.mylistbox = appuifw.Listbox(self.items,self.handle_selection)
		appuifw.app.body = self.mylistbox


	def handle_selection(self):
		appuifw.note(self.items[self.mylistbox.current()][0] + u" has been selected.", 'info')
	
	def quit(self):
		self.app_lock.signal()
		appuifw.app.set_exit()	
		
	def loop(self):

		self.app_lock.wait()
		
if __name__ == "__main__":
    mapys = Application()
    mapys.loop()
   
	
	

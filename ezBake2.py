#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class winMain:
	
	def __init__(self):
		
		# Get GUI from Glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ezBake2.glade")
		self.builder.connect_signals(self)
		
		# Display main window
		self.windowMain = self.builder.get_object("winMain")
		self.windowMain.show()
	
	def main(self):
		Gtk.main()
	
	def on_winMain_destroy(self, widget, data=None):
		print("on_winMain_destory")
		Gtk.main_quit()
		
if __name__ == "__main__":
	app = winMain()
	app.main()

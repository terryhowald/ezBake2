#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject 

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas	
from matplotlib.figure import Figure
import numpy as np

import os
import random

class winMain:
	
	def __init__(self):
		
		# Get GUI from Glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ezBake2.glade")
		self.builder.connect_signals(self)

		self.toolQuit = self.builder.get_object("toolQuit")
		self.toolQuit.connect("clicked", self.toolQuit_clicked)	
		self.toolQuit.set_sensitive(True)			
		
		# Setup status bar
		self.statusBar = self.builder.get_object("bar_status")
		self.context_id = self.statusBar.get_context_id("status")
		self.status_count = 0

		# Update status bar
		status_text = "Random number = " + str(random.randint(1,101))
		self.statusBar.push(self.context_id, status_text)							

		# Start timer
		timer_interval = 1
		GObject.timeout_add_seconds(timer_interval, self.on_handle_timer)		

		# Display main window
		self.winMain = self.builder.get_object("winMain")
		self.winMain.show_all()		
	
	def main(self):
		Gtk.main()
	
	def on_winMain_destroy(self, widget, data=None):
		print("on_winMain_destory")
		Gtk.main_quit()

	def on_file_quit_activate(self, widget, data=None):
		print("on_file_quit")
		self.winMain.destroy()		

	def on_handle_timer(self):
		# Update status bar
		self.statusBar.pop(self.context_id)
		status_text = "Random number = " + str(random.randint(1,101))
		self.statusBar.push(self.context_id, status_text)			
		return True		

	def toolQuit_clicked(self, widget, data = None):
		self.on_winMain_destroy(self)		
		
if __name__ == "__main__":
	app = winMain()
	app.main()

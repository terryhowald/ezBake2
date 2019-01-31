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

		# Set New button initial state
		self.toolNew = self.builder.get_object("toolNew")
		self.toolNew.set_sensitive(True)

		# Set Open button initial state
		self.toolOpen= self.builder.get_object("toolOpen")
		self.toolOpen.set_sensitive(True)

		# Set Start button initial state
		self.toolStart= self.builder.get_object("toolStart")
		self.toolStart.set_sensitive(True)

		# Set Stop button initial state
		self.toolStop = self.builder.get_object("toolStop")
		self.toolStop.set_sensitive(True)		

		# Set Save button initial state
		self.toolSave = self.builder.get_object("toolSave")
		self.toolSave.set_sensitive(True)												

		# Set Quit button initial state
		self.toolQuit = self.builder.get_object("toolQuit")
		self.toolQuit.set_sensitive(True)			
		
		# Setup status bar
		self.statusBar = self.builder.get_object("bar_status")
		self.context_id = self.statusBar.get_context_id("status")
		self.status_count = 0

		# Setup graph
		self.fig = Figure(figsize=(5,5), dpi=100)
		self.fig.patch.set_facecolor('0.8')
		self.ax = self.fig.add_subplot(111)	
		self.canvas = FigureCanvas(self.fig)
		self.setupplot()
		self.winScroll = self.builder.get_object("winScroll")
		self.winScroll.add_with_viewport(self.canvas)	

		# Setup callback for graph clicks
		self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

		# Update status bar
		status_text = "Random number = " + str(random.randint(1,101))
		self.statusBar.push(self.context_id, status_text)							

		# Start timer
		#timer_interval = 1
		#GObject.timeout_add_seconds(timer_interval, self.on_handle_timer)		

		# Display main window
		self.winMain = self.builder.get_object("winMain")
		self.winMain.show_all()		
	
	def main(self):
		Gtk.main()
	
	def on_winMain_destroy(self, widget, data=None):
		print("on_winMain_destory")
		self.fig.canvas.mpl_disconnect(self.cid)
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

	def on_toolNew_clicked(self, widget, data = None):
		print("on_toolNew_clicked")	

	def on_toolOpen_clicked(self, widget, data = None):
		print("on_toolOpen_clicked")		

	def on_toolStart_clicked(self, widget, data = None):
		print("on_toolStart_clicked")			

	def on_toolStop_clicked(self, widget, data = None):
		print("on_toolStop_clicked")			

	def on_toolSave_clicked(self, widget, data = None):
		print("on_toolSave_clicked")					

	def on_toolQuit_clicked(self, widget, data = None):
		print("on_toolQuit_clicked")			
		self.on_winMain_destroy(self)	

	def setupplot(self):
		self.ax.set_title('Kiln Firing Schedule')
		self.ax.set_xlabel('Time (h)')
		self.ax.set_ylabel('Temp (C)')
		self.ax.set_xlim(0,24)
		self.ax.set_ylim(0,1000)
		self.ax.patch.set_facecolor('0.8')			

	def onclick(self, event):
		print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
			('double' if event.dblclick else 'single', event.button,
			event.x, event.y, event.xdata, event.ydata))
		
if __name__ == "__main__":
	app = winMain()
	app.main()

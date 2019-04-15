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
import csv 
import sys
import numpy as np
import time
import math

class winMain:
	
	def __init__(self):
		
		# Get GUI from Glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ezBake2.glade")
		self.builder.connect_signals(self)

		# Set New button initial state
		self.toolNew = self.builder.get_object("toolNew")
		self.toolNew.set_sensitive(False)

		# Set Open button initial state
		self.toolOpen= self.builder.get_object("toolOpen")
		self.toolOpen.set_sensitive(True)

		# Set Start button initial state
		self.toolStart= self.builder.get_object("toolStart")
		self.toolStart.set_sensitive(False)

		# Set Stop button initial state
		self.toolStop = self.builder.get_object("toolStop")
		self.toolStop.set_sensitive(False)		

		# Set Save button initial state
		self.toolSave = self.builder.get_object("toolSave")
		self.toolSave.set_sensitive(False)												

		# Set Quit button initial state
		self.toolQuit = self.builder.get_object("toolQuit")
		self.toolQuit.set_sensitive(True)			
		
		# Setup status bar
		self.statusBar = self.builder.get_object("bar_status")
		self.context_id = self.statusBar.get_context_id("status")
		self.status_count = 0

		# Update status bar
		#status_text = "Random number = " + str(random.randint(1,101))
		status_text = "Click on New or Open to begin"
		self.statusBar.push(self.context_id, status_text)	

		# Setup entry fields
		self.currTempEntry = self.builder.get_object("currTempEntry")
		self.currTempEntry.set_text("0.0 °C")	
		self.targTempEntry = self.builder.get_object("targTempEntry")
		self.targTempEntry.set_text("0.0 °C")	
		self.roomTempEntry = self.builder.get_object("roomTempEntry")
		self.roomTempEntry.set_text("0.0 °C")	
		self.runnTimeEntry = self.builder.get_object("runnTimeEntry")
		self.runnTimeEntry.set_text("00:00:00")
		self.remaTimeEntry = self.builder.get_object("remaTimeEntry")
		self.remaTimeEntry.set_text("00:00:00")
		self.pwmDutyEntry = self.builder.get_object("pwmDutyEntry")
		self.pwmDutyEntry.set_text("0%")
		self.oxygenEntry = self.builder.get_object("oxygenEntry")
		self.oxygenEntry.set_text("Off")												

		# Setup graph
		self.fig = Figure(figsize=(5,5), dpi=100)
		#self.fig.patch.set_facecolor('0.8')
		self.ax = self.fig.add_subplot(111)	
		self.canvas = FigureCanvas(self.fig)
		self.setupplot()
		self.winScroll = self.builder.get_object("winScroll")
		self.winScroll.add_with_viewport(self.canvas)	

		# Setup callback for graph clicks
		self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)						

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

		# Clear out data lists
		self.xdata = []
		self.ydata = []	
		self.curTemp = []
		self.curTime = []

		# Load temp data from csv file
		f = open('temp.csv')
		data = csv.reader(f)
		for row in data:
		    self.xdata.append(float(row[0]))
		    self.ydata.append(float(row[1]))	    
		f.close()

		# Interpret data
		self.interp_data()		

		# Plot temp data
		self.plotdata()					

		self.toolStart.set_sensitive(True)
		self.toolOpen.set_sensitive(False)				

	def on_toolStart_clicked(self, widget, data = None):
		print("on_toolStart_clicked")
		self.toolStart.set_sensitive(False)
		self.toolOpen.set_sensitive(False)
		self.toolStop.set_sensitive(True)
		self.toolQuit.set_sensitive(False)					

	def on_toolStop_clicked(self, widget, data = None):
		print("on_toolStop_clicked")
		self.toolStop.set_sensitive(False)
		self.toolOpen.set_sensitive(True)
		self.toolQuit.set_sensitive(True)					

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
		#self.ax.patch.set_facecolor('0.8')			

	def onclick(self, event):
		print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
			('double' if event.dblclick else 'single', event.button,
			event.x, event.y, event.xdata, event.ydata))

	def interp_data(self):
		# Create target temp data every 1 minute
		xmax = self.xdata[-1]
		xinc = 1.0/60.0
		self.xval = np.arange(0.0, float(xmax)+xinc, xinc)
		self.yint = np.interp(self.xval, self.xdata, self.ydata)

	def setupplot(self):
		self.ax.legend(loc='upper right')
		self.ax.set_title('Kiln Firing Schedule')
		self.ax.set_xlabel('Time (h)')
		self.ax.set_ylabel('Temp (C)')
		self.ax.set_axis_bgcolor((0.75,0.75,0.75))
		self.ax.set_xlim(0,24)
		self.ax.set_ylim(0,1000)
		
	def resetplot(self):
		self.ax.cla()		

	def plotdata(self):
		self.resetplot()
		self.setupplot()
		self.ax.set_xlim(0, int(self.xdata[-1]))
		self.ax.scatter(self.xdata, self.ydata, color='black')
		self.ax.plot(self.xval, self.yint, color='black')
		#self.ax.plot(self.oxdata, self.oydata, color='blue')
		self.ax.scatter(self.curTime, self.curTemp, color='red')
		self.fig.canvas.draw()					
		
if __name__ == "__main__":
	app = winMain()
	app.main()

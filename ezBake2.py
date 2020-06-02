#!/usr/bin/env python3

from guizero import App, Box, Text, TextBox, PushButton

import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import constants

class winMain:
    def __init__(self):
        # Setup the app
        self.app = App(title = "ezBake", width = constants.APP_WIDTH, height = constants.APP_HEIGHT, visible=False)       

        # Setup the toolbar
        toolbar_box = Box(self.app, width="fill", align="top", border=True, layout="grid")
        self.newButton = PushButton(toolbar_box, command=self.handle_newButton, text="New", width=6, grid=[0,0])
        self.openButton = PushButton(toolbar_box, command=self.handle_openButton, text="Open", width=6, grid=[1,0])
        self.startButton = PushButton(toolbar_box, command=self.handle_startButton, text="Start", width=6, grid=[2,0])
        self.stopButton = PushButton(toolbar_box, command=self.handle_stopButton, text="Stop", width=6, grid=[3,0])
        self.saveButton = PushButton(toolbar_box, command=self.handle_saveButton, text="Save", width=6, grid=[4,0])
        self.quitButton = PushButton(toolbar_box, command=self.handle_quitButton, text="Quit", width=6, grid=[5,0])

        # Set initual toolbar button states
        self.openButton.disable()
        self.startButton.disable()
        self.stopButton.disable()
        self.saveButton.disable()  

        # Setup the status bar
        status_box = Box(self.app, width="fill", align="bottom", border=True)
        self.statusText = Text(status_box, align="left", text="Status")                         

        # Setup sensor feedback box
        data_box = Box(self.app, height="fill", align="right", border=True)
        Text(data_box)
        currTempText = Text(data_box, text="Current Temp")
        self.currTempTextBox = TextBox(data_box, text="0.0 °C", enabled=False)
        Text(data_box)
        targTempText = Text(data_box, text = "Target Temp")
        self.targTempTextBox = TextBox(data_box, text="0.0 °C", enabled=False)
        Text(data_box)        
        roomTempText = Text(data_box, text = "Room Temp")
        self.roomTempTextBox = TextBox(data_box, text="0.0 °C", enabled=False)
        Text(data_box)        
        runTempText = Text(data_box, text = "Running Time")
        self.runTempTextBox = TextBox(data_box, text="00:00:00", enabled=False)
        Text(data_box)           
        remTempText = Text(data_box, text = "Remaining Time")
        self.remTempTextBox = TextBox(data_box, text="00:00:00", enabled=False)
        Text(data_box)           
        pwmDutyCycleText = Text(data_box, text = "PWM Duty Cycle")
        self.pwmDutyCycleTextBox = TextBox(data_box, text="0%", enabled=False)  

        # Initialize Time and Temp arrays
        self.timePoints = []
        self.tempPoints = [] 
        self.timePoints.append(0.0)
        self.tempPoints.append(0.0)                                                           

        # Setup graph display
        self.graph_box = Box(self.app, align="top", width="fill", border=False)
        self.figure = Figure(figsize=(6.75, 5.3))
        self.plot = self.figure.add_subplot(1, 1, 1)

        # Setup plot
        self.maxTime = constants.INIT_TIME
        self.maxTemp = constants.INIT_TEMP
        self.setupPlot()

        # Call handle_quitButtion() when Close Window selected
        self.app.when_closed = self.handle_quitButton

        # Call handle_repeat() every 1000 msec
        #self.app.repeat(1000, self.handle_repeat)

        # Center program on screen
        self.centerWindow()
        self.app.visible = True  
               
    def main(self):
        self.app.display()
        
    def onPlotClick(self, event):
        # Ignore if outside plot
        if event.inaxes == None:         
            return  
        # Check data
        if event.xdata > max(self.timePoints):
            # Append plot data and replot
            self.timePoints.append(event.xdata)
            self.tempPoints.append(event.ydata)
            self.setupPlot()                         

    def onMouseMove(self, event):
        # Clear status if outside plot
        if event.inaxes == None:
            self.statusText.value = ""             
            return       

        # Round mouse coordinates for display
        xval = str(round(event.xdata, 2))
        yval = str(round(event.ydata, 2))

        # Display time and temp values in the status box
        self.statusText.value = "Time = " + xval + ", Temp = " + yval                   

    def handle_newButton(self):
        # Retrieve maximum time from user
        value = self.app.question("Maximum Time", "Enter maximum time in hours")
        if value == None or value == '':
            return
        self.maxTime = float(value)
        if self.maxTime <= constants.MIN_TIME or self.maxTime > constants.MAX_TIME:
            return

        # Retrieve maximum temp from user
        value = self.app.question("Maximum Temp", "Enter maximum temp in Celcius")
        if value == None:
            return
        self.maxTemp = float(value)            
        if self.maxTemp <= constants.MIN_TEMP or self.maxTemp > constants.MAX_TEMP:
            return

        # Reset plot
        self.resetPlot()

        # Setup plot
        self.timePoints = []
        self.tempPoints = []
        self.timePoints.append(0.0)
        self.tempPoints.append(0.0)             
        self.setupPlot()

        # Activate Start button
        self.startButton.enable()        
 
    def resetPlot(self):
        # Reset plot
        self.plot.cla()  

    def setupPlot(self):
        # Setup plot
        self.plot.set_title('Kiln Firing Schedule')
        self.plot.set_xlabel('Time (h)')
        self.plot.set_ylabel('Temp (°C)')        
        self.plot.set_xlim(0,self.maxTime)
        self.plot.set_ylim(0,self.maxTemp)  

        # Plot data
        self.plot.plot(self.timePoints, self.tempPoints, color="black")
        self.plot.scatter(self.timePoints, self.tempPoints, color="black")

        # Display plot
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_box.tk)
        self.canvas.get_tk_widget().grid(row=0, column=0)  

        # Setup callback for plot clicks
        self.figure.canvas.mpl_connect('button_press_event', self.onPlotClick) 
        self.figure.canvas.mpl_connect('motion_notify_event', self.onMouseMove)                         

    def handle_openButton(self):
        print("openButton pressed")

    def handle_startButton(self):
        print("startButton pressed")

    def handle_stopButton(self):
        print("stopButton pressed")

    def handle_saveButton(self):
        print("saveButton pressed")

    def handle_quitButton(self):
        print("quitButton pressed")
        # Shutdown program
        self.app.destroy()

    def handle_repeat(self):
        print("handle_repeat called")

    def centerWindow(self):
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.app.tk.winfo_screenwidth()/2 - constants.APP_WIDTH/2)
        positionDown = int(self.app.tk.winfo_screenheight()/2 - constants.APP_HEIGHT/2)  

        # Positions the window in the center of the page.
        self.app.tk.geometry("+{}+{}".format(positionRight, positionDown))                                          

if __name__ == "__main__":

	app = winMain()
	app.main()

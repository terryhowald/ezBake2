#!/usr/bin/env python3

from guizero import App, Box, Text, TextBox, PushButton

import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class winMain:
    def __init__(self):
        # Setup the app
        self.app = App(title = "ezBake", width = 800, height = 600)

        # Setup the toolbar
        toolbar_box = Box(self.app, width="fill", align="top", border=True, layout="grid")
        self.newButton = PushButton(toolbar_box, command=self.handle_newButton, text="New", width=6, grid=[0,0])
        self.openButton = PushButton(toolbar_box, command=self.handle_openButton, text="Open", width=6, grid=[1,0])
        self.startButton = PushButton(toolbar_box, command=self.handle_startButton, text="Start", width=6, grid=[2,0])
        self.stopButton = PushButton(toolbar_box, command=self.handle_stopButton, text="Stop", width=6, grid=[3,0])
        self.saveButton = PushButton(toolbar_box, command=self.handle_saveButton, text="Save", width=6, grid=[4,0])
        self.quitButton = PushButton(toolbar_box, command=self.handle_quitButton, text="Quit", width=6, grid=[5,0])

        # Set initual toolbar button states
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

        # Setup graph display
        graph_box = Box(self.app, align="top", width="fill", border=False)
        figure = Figure(figsize=(6.75, 5.3))
        plot = figure.add_subplot(1, 1, 1)
        plot.set_title('Kiln Firing Schedule')
        plot.set_xlabel('Time (h)')
        plot.set_ylabel('Temp (°C)')
        plot.set_xlim(0,24)
        plot.set_ylim(0,1000)        
        #plot.plot(self.t, self.s, color="blue")
        canvas = FigureCanvasTkAgg(figure, graph_box.tk)
        canvas.get_tk_widget().grid(row=0, column=0)      

        # Call handle_quitButtion() when Close Window selected
        self.app.when_closed = self.handle_quitButton

        # Call handle_repeat() every 1000 msec
        #self.app.repeat(1000, self.handle_repeat)

        # Center program on screen
        #self.app.tk.
     
    def main(self):
        self.app.display()

    def handle_newButton(self):
        print("newButton pressed")

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

if __name__ == "__main__":

	app = winMain()
	app.main()

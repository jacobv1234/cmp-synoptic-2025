# class that contains all of the tkinter graphical stuff
from tkinter import *
class AppDisplay:
    # initialiser function
    def __init__(self, width = 480, height = 720):
        self.width = width
        self.height = height

        self.window = Tk() # main window object
        self.window.protocol("WM_DELETE_WINDOW", self.close) # stop the main loop if the X button is pressed

        # Canvas allows for shapes/images to be drawn to the screen + handles user input
        self.c = Canvas(self.window, width=width, height=height, bg='white') 
        self.c.pack()

        self.running = True
    
    # run every frame
    def update(self):
        self.window.update()
    
    def close(self):
        self.running = False
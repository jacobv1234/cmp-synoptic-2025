# class that contains all of the tkinter graphical stuff
from tkinter import *
from PIL import Image, ImageTk
from lib.databaseConnectionFront import displayDBData
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

        # lists to hold objects drawn to the screen - cobjects is for stuff on the canvas, widgets is for buttons, labels, etc
        self.cobjects = []
        self.widgets = []

        # loaded images go in this dictionary so they remain loaded
        self.images = {}

        
        self.running = True

        self.draw_front_page()

    def draw_front_page(self):
        self.clear_screen()

        textExample = StringVar()
        getDBTestData = str(displayDBData())
        textExample.set(getDBTestData) #a text variable is used in tkinter to dsiplay text here we need to SET the variable

        #Here we create the label for the text 
        label = Label(self.window, textvariable=textExample, anchor=CENTER, height=3, width=30, bd=3, padx=15, pady=15, justify=CENTER, relief=RAISED, underline=0, wraplength=250)
        label.place(relx = 0.5, rely=0.5, anchor = CENTER)
        self.widgets.append(label)

        img = Image.open('images/Enivronment App Logo.png')
        imgSmallerResize = img.resize((360, 480))
        self.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

        self.cobjects.append(self.c.create_image(250, 150, anchor=CENTER, image=self.images['logo']))

    def clear_screen(self):
        for object in self.cobjects:
            self.c.delete(object)
        for widget in self.widgets:
            widget.destroy()
        self.cobjects = []
        self.widgets = []


    # run every frame
    def update(self):
        self.window.update()
    
    def close(self):
        self.running = False


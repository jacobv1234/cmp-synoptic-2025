from tkinter import *
from PIL import Image, ImageTk
from json import loads, dumps
from lib.databaseConnectionFront import getUserIcon, getUserTrashFound, getUserCleaned
#from lib.appdisplay import AppDisplay

def draw_profile_page(self):
    self.clear_screen()

    if self.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = '#2A2A2E'
        highlight = 'white'

    # back button
    img = Image.open('images/backArrow.png')
    imgSmallerResize = img.resize((40,40))
    self.images['backarrow'] = ImageTk.PhotoImage(imgSmallerResize)

    self.widgets.extend([
        Button(self.window, 
               image=self.images['backarrow'],
               foreground= '#3b7f3b',
               background=colour,
               font='Arial 40',
               borderwidth=0,
               relief='solid',
               command=self.open_map),
        
        Button(self.window,
               text='Apply',
               foreground='#3b7f3b',
               background=colour,
               font='Arial 25',
               borderwidth=0,
               relief='solid',
               highlightbackground='#3b7f3b',
               highlightcolor='#3b7f3b',
               highlightthickness=2,
               activeforeground=highlight,
               command=self.apply_settings)
    ])

    self.widgets[0].place(x = 10, y = self.height-10, width = 40, height = 40, anchor = 'sw')

    #Here we get all nessecary user details for displaying on their profile 

    from lib.appdisplay import AppDisplay
    self.username = AppDisplay.username
    self.getUserPfp = getUserIcon(self.username)
    self.getUserTrashFound = getUserTrashFound(self.username)
    self.getUserCleaned = getUserCleaned(self.username)

    
    
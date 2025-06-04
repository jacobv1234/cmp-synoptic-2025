from tkinter import *
from PIL import Image, ImageTk
#from lib.appdisplay import AppDisplay

def draw_settings_page(self):
    self.clear_screen()

    # back button
    img = Image.open('images/backArrow.png')
    imgSmallerResize = img.resize((40,40))
    self.images['backarrow'] = ImageTk.PhotoImage(imgSmallerResize)

    self.widgets.append(
        Button(self.window, 
               image=self.images['backarrow'],
               foreground= '#3b7f3b',
               font='Arial 40',
               borderwidth=0,
               relief='solid',
               command=self.open_map)
    )

    self.widgets[0].place(x = 5, y = self.height-5, width = 40, height = 40, anchor = 'sw')

    # top
    self.cobjects.extend([
        self.c.create_image(self.width-5, 5, image = self.icon_images['settings'], anchor='ne'),
        self.c.create_text(20,8, fill='#3b7f3b', font='Arial 20', text='Settings', anchor='nw')
    ])
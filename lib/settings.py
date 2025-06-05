from tkinter import *
from PIL import Image, ImageTk
from json import loads, dumps
#from lib.appdisplay import AppDisplay

def draw_settings_page(self):
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
    self.widgets[1].place(x = self.width - 10, y = self.height - 10, width = 100, height = 40, anchor = 'se')

    # top
    self.cobjects.extend([
        self.c.create_image(self.width-5, 5, image = self.icon_images['settings'], anchor='ne'),
        self.c.create_text(20,8, fill='#3b7f3b', font='Arial 20', text='Settings', anchor='nw')
    ])

    # labels
    self.cobjects.extend({
        self.c.create_rectangle(self.width-112, self.height-52, self.width-8, self.height-8, fill='#3b7f3b', outline='#3b7f3b'),

        self.c.create_text(self.width/2 -50, self.height/2 -200, fill='#3b7f3b', font='Arial 20', text='Language', anchor='e'),
        self.c.create_text(self.width/2 -50, self.height/2, fill='#3b7f3b', font='Arial 20', text='Theme', anchor='e')
    })

    # entry boxes
    # self.widgets[2] = language entry box
    # self.widgets[3] = theme
    
    self.language = StringVar(self.window, self.settings['language'])
    self.theme = StringVar(self.window, self.settings['theme'])

    self.widgets.extend([
        OptionMenu(self.window, 
            self.language,
            'English', 'Afrikaans', 'Swazi', 'Xhosa', 'Zulu' # options
            ),
        OptionMenu(self.window,
            self.theme,
            'Light', 'Dark'
        )
    ])

    # due to how the OptionMenu init works, we cannot do this when creating it
    self.widgets[2].config(font = 'Arial 15',
        highlightbackground = '#3b7f3b', highlightcolor = '#3b7f3b', highlightthickness = 2, borderwidth = 0,
        background = colour, foreground = highlight)
    
    self.widgets[3].config(font = 'Arial 15',
        highlightbackground = '#3b7f3b', highlightcolor = '#3b7f3b', highlightthickness = 2, borderwidth = 0,
        background = colour, foreground = highlight)
    
    self.window.nametowidget(self.widgets[2].menuname).config(font = 'Arial 15')
    self.window.nametowidget(self.widgets[3].menuname).config(font = 'Arial 15')

    self.widgets[2].place(x = self.width/2, y = self.height / 2 - 200, width = self.width * 0.4, height = 30, anchor = 'w')
    self.widgets[3].place(x = self.width/2, y = self.height / 2, width = self.width * 0.4, height = 30, anchor = 'w')



def load_settings(filename = 'settings.json'):
    text = ''
    with open(filename, 'r') as f:
        text = f.read()
    settings = loads(text)
    return settings

def save_settings(settings, filename  ='settings.json'):
    with open(filename, 'w') as f:
        f.write(dumps(settings, indent=4))

def apply_settings(self):
    settings = {
        'language': self.language.get(),
        'theme': self.theme.get()
    }

    save_settings(settings)

    self.settings = settings

    if self.settings['theme'] == 'Light':
        self.c.configure(bg='white')
    else:
        self.c.configure(bg='black')

    self.open_map()
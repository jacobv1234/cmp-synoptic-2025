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
    
    if self.settings['textsize'] == 'Normal':
        textsize = 20
        smalltext = 15
        bigtext = 40
    else:
        textsize = 30
        smalltext = 20
        bigtext = 50

    # back button
    img = Image.open('images/backArrow.png')
    imgSmallerResize = img.resize((bigtext,bigtext))
    self.images['backarrow'] = ImageTk.PhotoImage(imgSmallerResize)

    self.widgets.extend([
        Button(self.window, 
               image=self.images['backarrow'],
               foreground= '#3b7f3b',
               background=colour,
               font=f'Arial {bigtext}',
               borderwidth=0,
               relief='solid',
               command=self.open_map),
        
        Button(self.window,
               text='Apply',
               foreground='#3b7f3b',
               background=colour,
               font=f'Arial {bigtext - 15}',
               borderwidth=0,
               relief='solid',
               highlightbackground='#3b7f3b',
               highlightcolor='#3b7f3b',
               highlightthickness=2,
               activeforeground='black',
               command=self.apply_settings)
    ])

    self.widgets[0].place(x = 10, y = self.height-10, width = bigtext, height = bigtext, anchor = 'sw')
    self.widgets[1].place(x = self.width - 10, y = self.height - 10, width = int(bigtext*2.5), height = bigtext, anchor = 'se')

    # top
    self.cobjects.extend([
        self.c.create_image(self.width-5, 5, image = self.icon_images['settings'], anchor='ne'),
        self.c.create_text(20,8, fill='#3b7f3b', font=f'Arial {textsize}', text='Settings', anchor='nw')
    ])

    # labels
    self.cobjects.extend({
        self.c.create_rectangle(self.width-int(bigtext*2.5)-12, self.height-bigtext-12,
                                self.width-8, self.height-8, fill='#3b7f3b', outline='#3b7f3b'),

        self.c.create_text(self.width/2 -50, self.height/2 -150, fill='#3b7f3b', font=f'Arial {textsize}', text='Language', anchor='e'),
        self.c.create_text(self.width/2 -50, self.height/2, fill='#3b7f3b', font=f'Arial {textsize}', text='Theme', anchor='e'),
        self.c.create_text(self.width/2 -50, self.height/2 +150, fill='#3b7f3b', font=f'Arial {textsize}', text='Text Size', anchor='e')
    })

    # entry boxes
    # self.widgets[2] = language entry box
    # self.widgets[3] = theme
    # self.widgets[4] = text size
    
    self.language = StringVar(self.window, self.settings['language'])
    self.theme = StringVar(self.window, self.settings['theme'])
    self.textsize = StringVar(self.window, self.settings['textsize'])

    self.widgets.extend([
        OptionMenu(self.window, 
            self.language,
            'English', 'Afrikaans', 'Swazi', 'Xhosa', 'Zulu' # options
            ),
        OptionMenu(self.window,
            self.theme,
            'Light', 'Dark'
        ),
        OptionMenu(self.window,
            self.textsize,
            'Normal', 'Large'
        )
    ])

    # due to how the OptionMenu init works, we cannot do this when creating it
    self.widgets[2].config(font = f'Arial {smalltext}',
        highlightbackground = '#3b7f3b', highlightcolor = '#3b7f3b', highlightthickness = 2, borderwidth = 0,
        background = colour, foreground = highlight)
    
    self.widgets[3].config(font = f'Arial {smalltext}',
        highlightbackground = '#3b7f3b', highlightcolor = '#3b7f3b', highlightthickness = 2, borderwidth = 0,
        background = colour, foreground = highlight)
    
    self.widgets[4].config(font = f'Arial {smalltext}',
        highlightbackground = '#3b7f3b', highlightcolor = '#3b7f3b', highlightthickness = 2, borderwidth = 0,
        background = colour, foreground = highlight)
    
    self.window.nametowidget(self.widgets[2].menuname).config(font = f'Arial {smalltext}',)
    self.window.nametowidget(self.widgets[3].menuname).config(font = f'Arial {smalltext}',)
    self.window.nametowidget(self.widgets[4].menuname).config(font = f'Arial {smalltext}',)

    self.widgets[2].place(x = self.width/2, y = self.height / 2 - 150, width = self.width * 0.4, height = smalltext + 15, anchor = 'w')
    self.widgets[3].place(x = self.width/2, y = self.height / 2, width = self.width * 0.4, height = smalltext + 15, anchor = 'w')
    self.widgets[4].place(x = self.width/2, y = self.height / 2 + 150, width = self.width * 0.4, height = smalltext + 15, anchor = 'w')



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
        'theme': self.theme.get(),
        'textsize': self.textsize.get(),
        'saved_user': self.settings['saved_user']
    }

    save_settings(settings)

    self.settings = settings

    if self.settings['theme'] == 'Light':
        self.c.configure(bg='white')
    else:
        self.c.configure(bg='#2A2A2E')

    self.open_map()
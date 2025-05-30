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

        # load the logo into self.images
        img = Image.open('images/logo.png')
        imgSmallerResize = img.resize((250,250))
        self.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

        #bg = PhotoImage(file = "images/southafricanbuilding.jpg")
        #mainBG = Label(self.window, image = bg)
        #Place image on canvas 

        self.cobjects.extend([
            self.c.create_image(self.width/2, 150, image = self.images['logo'], anchor = 'center'),
            # labels for text entry
            self.c.create_text(self.width/2, self.height/2, font='Arial 15', text='Email', anchor='center'),
            self.c.create_text(self.width/2, self.height/2 +70, font='Arial 15', text='Password', anchor='center')
        ])

        # data entry points
        # self.widgets[0] = email / name / whatever we settle on
        # self.widgets[1] = password
        # use .get() on the above for the values entered
        self.widgets.extend([
            Entry(self.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb'),
            Entry(self.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF')
        ])
        self.widgets[0].place(x=self.width/2, y=(self.height/2)+30, anchor='center', width=int(self.width*2/3), height=40)
        self.widgets[1].place(x=self.width/2, y=(self.height/2)+100, anchor='center', width=int(self.width*2/3), height=40)


        # buttons
        # self.widgets[2] = log in
        # self.widgets[3] = go to register
        self.widgets.extend([
            Button(self.window, font='Arial 20', justify='center', background="#3b7f3b", foreground='white',
                    activebackground="#226D22", activeforeground='white',
                    text='Log In Now \u2192', command = self.log_in_pressed),

            Button(self.window, font='Arial 10', justify='center', background="#bbbbbb",
                   text='Register', command = self.draw_register_page)
        ])
        self.widgets[2].place(x=self.width/2, y=(self.height/2)+170, anchor='center', width=int(self.width*2/3), height=40)
        self.widgets[3].place(x=self.width/2, y=self.height-40, anchor='center', width=int(self.width/2), height=30)


    def draw_register_page(self):
        self.clear_screen()

        self.cobjects.extend([
            self.c.create_image(self.width/2, 150, image = self.images['logo'], anchor = 'center'),
            # labels for text entry
            self.c.create_text(self.width/2, self.height/2, font='Arial 10', text='Name', anchor='n'),
            self.c.create_text(self.width/2, self.height/2 +50, font='Arial 10', text='Email', anchor='n'),
            self.c.create_text(self.width/2, self.height/2 +100, font='Arial 10', text='Password', anchor='n'),
            self.c.create_text(self.width/2, self.height/2 +150, font='Arial 10', text='Confirm Password', anchor='n')
        ])

        # data entry points
        # self.widgets[0] = name
        # self.widgets[1] = email
        # self.widgets[2] = password
        # self.widgets[3] = confirm password
        # use .get() on the above for the values entered
        self.widgets.extend([
            Entry(self.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb'),
            Entry(self.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb'),
            Entry(self.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF'),
            Entry(self.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF')
        ])
        self.widgets[0].place(x=self.width/2, y=(self.height/2)+30, anchor='center', width=int(self.width*2/3), height=35)
        self.widgets[1].place(x=self.width/2, y=(self.height/2)+80, anchor='center', width=int(self.width*2/3), height=35)
        self.widgets[2].place(x=self.width/2, y=(self.height/2)+130, anchor='center', width=int(self.width*2/3), height=35)
        self.widgets[3].place(x=self.width/2, y=(self.height/2)+180, anchor='center', width=int(self.width*2/3), height=35)


        # buttons
        # self.widgets[4] = register
        # self.widgets[5] = go to log in
        self.widgets.extend([
            Button(self.window, font='Arial 20', justify='center', background="#3b7f3b", foreground='white',
                    activebackground="#226D22", activeforeground='white',
                    text='Register \u2192', command=self.register_pressed),

            Button(self.window, font='Arial 10', justify='center', background="#bbbbbb",
                   text='Log In', command=self.draw_front_page)
        ])
        self.widgets[4].place(x=self.width/2, y=(self.height/2)+230, anchor='center', width=int(self.width*2/3), height=40)
        self.widgets[5].place(x=self.width/2, y=self.height-40, anchor='center', width=int(self.width/2), height=30)


    def clear_screen(self):
        for object in self.cobjects:
            self.c.delete(object)
        for widget in self.widgets:
            widget.destroy()
        self.cobjects = []
        self.widgets = []
    

    # button functions
    def log_in_pressed(self):
        pass

    def register_pressed(self):
        value = self.widgets[0].get()
        print(value)


    # run every frame
    def update(self):
        self.window.update()
    
    # handle exiting the mainloop - bound to X button
    def close(self):
        self.running = False


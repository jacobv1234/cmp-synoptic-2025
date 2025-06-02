from tkinter import Button, Entry
from PIL import Image, ImageTk

def draw_front_page(app):
    app.clear_screen()

    # load the logo into app.images
    img = Image.open('images/logo.png')
    imgSmallerResize = img.resize((250,250))
    app.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

    # bg = PhotoImage(file = "images/southafricanbuilding.jpg")
    # mainBG = Label(app.window, image = bg)
    # Place image on canvas 

    app.cobjects.extend([
        app.c.create_image(app.width/2, 150, image = app.images['logo'], anchor = 'center'),
        # labels for text entry
        app.c.create_text(app.width/2, app.height/2, font='Arial 15', text='Username', anchor='center'),
        app.c.create_text(app.width/2, app.height/2 +70, font='Arial 15', text='Password', anchor='center')
    ])

    # data entry points
    # app.widgets[0] = name
    # app.widgets[1] = password
    # use .get() on the above for the values entered
    app.widgets.extend([
        Entry(app.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb'),
        Entry(app.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF')
    ])
    app.widgets[0].place(x=app.width/2, y=(app.height/2)+30, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[1].place(x=app.width/2, y=(app.height/2)+100, anchor='center', width=int(app.width*2/3), height=40)

    # buttons
    # app.widgets[2] = log in
    # app.widgets[3] = go to register
    app.widgets.extend([
        Button(app.window, font='Arial 20', justify='center', background="#3b7f3b", foreground='white',
                activebackground="#226D22", activeforeground='white',
                text='Log In Now \u2192', command = app.log_in_pressed),

        Button(app.window, font='Arial 10', justify='center', background="#bbbbbb",
               text='Register', command = app.draw_register_page)

        #Button(app.window, font='Arial 20', justify='center', background="#3b7f3b", foreground='white',
        #    activebackground="#226D22", activeforeground='white',
        #    text='Map', command=app.open_map), # map button for testing
    ])
    app.widgets[2].place(x=app.width/2, y=(app.height/2)+170, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[3].place(x=app.width/2, y=app.height-40, anchor='center', width=int(app.width/2), height=30)

def draw_register_page(app):
    app.clear_screen()

    app.cobjects.extend([
        app.c.create_image(app.width/2, 150, image = app.images['logo'], anchor = 'center'),
        # labels for text entry
        app.c.create_text(app.width/2, app.height/2, font='Arial 10', text='Username', anchor='n'),
        app.c.create_text(app.width/2, app.height/2 +50, font='Arial 10', text='Email', anchor='n'),
        app.c.create_text(app.width/2, app.height/2 +100, font='Arial 10', text='Password', anchor='n'),
        app.c.create_text(app.width/2, app.height/2 +150, font='Arial 10', text='Confirm Password', anchor='n')
    ])

    # data entry points
    # app.widgets[0] = name
    # app.widgets[1] = email
    # app.widgets[2] = password
    # app.widgets[3] = confirm password
    # use .get() on the above for the values entered
    app.widgets.extend([
        Entry(app.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb'),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb'),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF'),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF')
    ])
    app.widgets[0].place(x=app.width/2, y=(app.height/2)+30, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[1].place(x=app.width/2, y=(app.height/2)+80, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[2].place(x=app.width/2, y=(app.height/2)+130, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[3].place(x=app.width/2, y=(app.height/2)+180, anchor='center', width=int(app.width*2/3), height=35)

    # buttons
    # app.widgets[4] = register
    # app.widgets[5] = go to log in
    app.widgets.extend([
        Button(app.window, font='Arial 20', justify='center', background="#3b7f3b", foreground='white',
                activebackground="#226D22", activeforeground='white',
                text='Register \u2192', command=app.register_pressed),

        Button(app.window, font='Arial 10', justify='center', background="#bbbbbb",
               text='Log In', command = app.draw_front_page)         
    ])
    app.widgets[4].place(x=app.width/2, y=(app.height/2)+230, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[5].place(x=app.width/2, y=app.height-40, anchor='center', width=int(app.width/2), height=30)

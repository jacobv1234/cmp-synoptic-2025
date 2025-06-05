from tkinter import Button, Entry
from PIL import Image, ImageTk

def draw_front_page(app):
    app.clear_screen()

    if app.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = "#2A2A2E"
        highlight = 'white'

    # load the logo into app.images
    img = Image.open('images/logo_v2.png')
    imgSmallerResize = img.resize((200,200))
    app.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

    img = Image.open('images/southafricanbuilding.jpg')
    # resize to the new height
    imgResized = img.resize((int(img.width * (app.height/img.height)), app.height))
    imgcropped = imgResized.crop((0,0,app.width,app.height))
    app.images['bg'] = ImageTk.PhotoImage(imgcropped)

    app.cobjects.extend([
        #app.c.create_image(0,0,image = app.images['bg'], anchor='nw'),
        app.c.create_image(app.width/2, 150, image = app.images['logo'], anchor = 'center'),
        # labels for text entry
        app.c.create_text(app.width/2, app.height/2 -5, font='Arial 15', text='Username', anchor='center', fill='#3b7f3b'),
        app.c.create_text(app.width/2, app.height/2 +65, font='Arial 15', text='Password', anchor='center', fill='#3b7f3b')
    ])

    # data entry points
    # app.widgets[0] = name
    # app.widgets[1] = password
    # use .get() on the above for the values entered
    app.widgets.extend([
        #Entry(app.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb'),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground=highlight),
        #Entry(app.window, font='Arial 20', justify='center', borderwidth=5, background='#bbbbbb', show='\u25CF')
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, show='\u25CF', relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground='#3b7f3b')
    ])
    app.widgets[0].place(x=app.width/2, y=(app.height/2)+30, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[1].place(x=app.width/2, y=(app.height/2)+100, anchor='center', width=int(app.width*2/3), height=40)

    # buttons
    # app.widgets[2] = log in
    # app.widgets[3] = go to register
    app.widgets.extend([
        Button(app.window, font='Arial 20', justify='center', background="#3b7f3b", foreground=colour,
                activebackground="#226D22", activeforeground=colour,
                text='Log In', command = app.log_in_pressed),

        Button(app.window,
        text="Register Now",
        font=("Arial", 12, "bold"),
        bg=colour, fg="#3b7f3b",
        activebackground=colour, activeforeground="#3b7f3b",
        relief="flat",
        borderwidth=0,
        command=app.draw_register_page  # Go to register page
    )
    ])
    app.widgets[2].place(x=app.width/2, y=(app.height/2)+170, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[3].place(x=app.width/2, y=app.height-40, anchor='center', width=int(app.width/2), height=30)

def draw_register_page(app):
    app.clear_screen()

    if app.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = '#2A2A2E'
        highlight = 'white'

    img = Image.open('images/logo_v2.png')
    imgSmallerResize = img.resize((200,200))
    app.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

    app.cobjects.extend([
        #app.c.create_image(0,0,image = app.images['bg'], anchor='nw'),
        app.c.create_image(app.width/2, 150, image = app.images['logo'], anchor = 'center'),
        # labels for text entry
        app.c.create_text(app.width/2, app.height/2 -92, font='Arial 13', text='Username', anchor='n', fill='#3b7f3b'),
        app.c.create_text(app.width/2, app.height/2 -22, font='Arial 13', text='Email', anchor='n', fill='#3b7f3b'),
        app.c.create_text(app.width/2, app.height/2 +48, font='Arial 13', text='Password', anchor='n', fill='#3b7f3b'),
        app.c.create_text(app.width/2, app.height/2 +118, font='Arial 13', text='Confirm Password', anchor='n', fill='#3b7f3b')
    ])

    # data entry points
    # app.widgets[0] = name
    # app.widgets[1] = email
    # app.widgets[2] = password
    # app.widgets[3] = confirm password
    # use .get() on the above for the values entered
    app.widgets.extend([
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground=highlight),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground=highlight),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, show='\u25CF', relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground='#3b7f3b'),
        Entry(app.window, font='Arial 15', justify='center', borderwidth=0, background=colour, show='\u25CF', relief='solid', 
              highlightbackground='#3b7f3b', highlightcolor='#3b7f3b', highlightthickness=2, foreground='#3b7f3b')
    ])
    app.widgets[0].place(x=app.width/2, y=(app.height/2)-50, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[1].place(x=app.width/2, y=(app.height/2)+20, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[2].place(x=app.width/2, y=(app.height/2)+90, anchor='center', width=int(app.width*2/3), height=35)
    app.widgets[3].place(x=app.width/2, y=(app.height/2)+160, anchor='center', width=int(app.width*2/3), height=35)

    # buttons
    # app.widgets[4] = register
    # app.widgets[5] = go to log in
    app.widgets.extend([
        Button(app.window, font='Arial 20', justify='center', background="#3b7f3b", foreground=colour,
                activebackground="#226D22", activeforeground=colour,
                text='Register', command=app.register_pressed),

        Button(app.window,
        text="Log In",
        font=("Arial", 12, "bold"),
        bg=colour, fg="#3b7f3b",
        activebackground=colour, activeforeground="#3b7f3b",
        relief="flat",
        borderwidth=0,
        command=app.draw_front_page  # Go to login page
    )        
    ])
    app.widgets[4].place(x=app.width/2, y=(app.height/2)+230, anchor='center', width=int(app.width*2/3), height=40)
    app.widgets[5].place(x=app.width/2, y=app.height-40, anchor='center', width=int(app.width/2), height=30)

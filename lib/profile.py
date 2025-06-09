from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from json import loads, dumps
from lib.databaseConnectionFront import getUserIcon, getUserTrashFound, getUserCleaned
from io import BytesIO
#from lib.appdisplay import createPfpRectangle

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

    print(f"VARIABLES FOR USER PAGE {self.username, self.getUserTrashFound, self.getUserCleaned}")

    #Profile Frame Logic
    self.profileFrame = Frame(self.window, bg='white')
    self.profileFrame.place(relx=0.10, rely=0.0575, anchor='nw')
    self.widgets.append(self.profileFrame)
    
    self.createProfileRectangle = self.createPfpRectangle()


    userProfilePicture = Image.open(BytesIO(self.getUserPfp)).resize((200, 150))
    self.addProfileImg = ImageTk.PhotoImage(userProfilePicture)

    pfpLabel = Label(self.profileFrame, image=self.addProfileImg, bg='white')
    pfpLabel.pack(side='left')

    #Username Frame Logic

    self.usernameFrame = Frame(self.window, bg='white')
    self.usernameFrame.place(relx=0.39, rely=0.30, anchor='ne')
    self.widgets.append(self.profileFrame)

    usernameLabel = Label(self.usernameFrame, text=self.username, bg='white', font=("Arial, 20 bold")) 
    usernameLabel.pack(side='left')

    #Heading

    
    self.statsFrame = Frame(self.window, bg='white')
    self.statsFrame.place(relx=0.27, rely=0.40, anchor='ne')
    self.widgets.append(self.profileFrame)
    headingFont= font.Font(family="Arial", size=18, underline=True)
    userTrashFoundLabel = Label(self.statsFrame, text=f"User Stats", bg='white', font=headingFont) 
    
    userTrashFoundLabel.pack(side='left')

    #User stats Frame Logic - trash found

    self.statsFrame = Frame(self.window, bg='white')
    self.statsFrame.place(relx=0.40, rely=0.50, anchor='ne')
    self.widgets.append(self.profileFrame)

    userTrashFoundLabel = Label(self.statsFrame, text=f"Total Trash Marked: {self.getUserTrashFound}", bg='white', font=("Arial, 14")) 
    
    userTrashFoundLabel.pack(side='left')

    #User stats Frame Logic - trash cleaned

    
    self.statsFrameTwo = Frame(self.window, bg='white')
    self.statsFrameTwo.place(relx=0.4075, rely=0.60, anchor='ne')
    self.widgets.append(self.profileFrame)
    userTrashCleaned = Label(self.statsFrameTwo, text=f"Total Trash Cleaned:{self.getUserCleaned}", bg='white', font=("Arial, 14")) 

    userTrashCleaned.pack(side='bottom')




    
    
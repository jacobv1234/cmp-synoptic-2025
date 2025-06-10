from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, UnidentifiedImageError
from json import loads, dumps
from lib.databaseConnectionFront import getUserIcon, getUserTrashFound, getUserCleaned, getAllUserPfps
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
    
    if self.settings['textsize'] == 'Normal':
        textsize = 20
        smalltext = 14
    else:
        textsize = 25
        smalltext = 20

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
               command=self.open_map)
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
    self.profileFrame = Frame(self.window, bg=colour)
    self.profileFrame.place(relx=0.5, rely=0.0575, anchor='n')
    self.widgets.append(self.profileFrame)
    
    


    try:
        userProfilePicture = Image.open(BytesIO(self.getUserPfp)).resize((200, 150))
        self.addProfileImg = ImageTk.PhotoImage(userProfilePicture)

        self.cobjects.append(self.c.create_rectangle(100, 200, self.width-100, 40, fill="", outline=highlight))

    except UnidentifiedImageError:
        self.addProfileImg = PhotoImage(width=200,height=150)
        self.addProfileImg.put((highlight,), to=(0, 0, 199, 149))
        self.addProfileImg.put((colour,), to=(2, 2, 197, 147))
        
    pfpLabel = Label(self.profileFrame, image=self.addProfileImg, bg=colour, fg=highlight)
    pfpLabel.pack(side='left')
    self.widgets.append(pfpLabel)

    #Username Frame Logic

    self.usernameFrame = Frame(self.window, bg=colour)
    self.usernameFrame.place(relx=0.5, rely=0.32, anchor='center')
    self.widgets.append(self.usernameFrame)

    usernameLabel = Label(self.usernameFrame, text=self.username, bg=colour, fg=highlight, font=(f"Arial, {textsize} bold")) 
    usernameLabel.pack(side='left')
    self.widgets.append(usernameLabel)

    #Heading

    
    self.statsFrame = Frame(self.window, bg='white')
    self.statsFrame.place(relx=0.5, rely=0.40, anchor='n')
    self.widgets.append(self.statsFrame)
    headingFont= font.Font(family="Arial", size=textsize, underline=True)
    userTrashFoundLabel = Label(self.statsFrame, text=f"User Stats", bg=colour, font=headingFont, fg=highlight) 
    
    userTrashFoundLabel.pack(side='left')
    self.widgets.append(userTrashFoundLabel)

    #User stats Frame Logic - trash found

    self.statsFrame = Frame(self.window, bg=colour)
    self.statsFrame.place(relx=0.5, rely=0.50, anchor='n')
    self.widgets.append(self.statsFrame)

    userTrashFoundLabel2 = Label(self.statsFrame, text=f"Total Trash Marked: {self.getUserTrashFound}", bg=colour, fg=highlight, font=(f"Arial, {smalltext}")) 
    
    userTrashFoundLabel2.pack(side='left')
    self.widgets.append(userTrashFoundLabel2)

    #User stats Frame Logic - trash cleaned

    
    self.statsFrameTwo = Frame(self.window, bg=colour)
    self.statsFrameTwo.place(relx=0.5, rely=0.60, anchor='n')
    self.widgets.append(self.statsFrameTwo)
    userTrashCleaned = Label(self.statsFrameTwo, text=f"Total Trash Cleaned:{self.getUserCleaned}", bg=colour,fg=highlight, font=(f"Arial, {smalltext}")) 

    userTrashCleaned.pack(side='bottom')
    self.widgets.append(userTrashCleaned)

    #Subheading for choosing user picture frame logic

    
    self.profilePicSubH = Frame(self.window, bg=colour)
    self.profilePicSubH.place(relx=0.5, rely=0.70, anchor='n')
    self.widgets.append(self.profilePicSubH)

    subHeadingLabel = Label(self.profilePicSubH, text=f"Select your acquired profile picture:", bg=colour, fg=highlight, font=(f"Arial, 13")) 
    
    subHeadingLabel.pack(side='left')
    self.widgets.append(subHeadingLabel)


    #User profile pic selection frame logic

    self.selectProfileFrame = Frame(self.window, bg=colour)
    self.selectProfileFrame.place(relx=0.5, rely=0.80, anchor='n')
    self.widgets.append(self.selectProfileFrame)

    defaultPfpName = "CleanMEerkat"
    # defaultuserProfilePicture = Image.open("images/cleanmeakat.png")
    # defaultPicture = BytesIO()
    # defaultuserProfilePicture.save(defaultPicture, format='PNG')
    currentUserProfileImageNames = list(getAllUserPfps(self.username))
    currentUserProfileImageNames.append(defaultPfpName)
    self.selectedPfp = StringVar(self.selectProfileFrame)
    self.selectedPfp.set(defaultPfpName)

            
    options = OptionMenu(self.selectProfileFrame, self.selectedPfp, *currentUserProfileImageNames)
    options.pack(side="top")

    

    #User Profile pic button to update

    
    self.choosePfpFrame = Frame(self.window, bg=colour)
    self.choosePfpFrame.place(relx=0.5, rely=0.90, anchor='n')
    self.widgets.append(self.choosePfpFrame)


    from lib.appdisplay import AppDisplay
    selectPfpBtn = Button(self.choosePfpFrame, text= "Select Chosen Profile Picture", font=f'Arial 10', fg=highlight,
                       bg=colour, relief="raised", command=lambda:self.setProfilePicture(self.selectedPfp, self.username), compound='top')
    selectPfpBtn.pack(anchor='center')
    self.widgets.append(selectPfpBtn)




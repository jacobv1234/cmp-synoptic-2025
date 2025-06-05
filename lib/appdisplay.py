# class that contains all of the tkinter graphical stuff
from tkinter import *

from PIL import Image, ImageTk
from lib.databaseConnectionFront import registerUser, logInUser
import tkinter as tk
from lib.map import open_map
from lib.pages import draw_front_page, draw_register_page
from lib.shopping import draw_shopping_page
from lib.welcome import draw_welcome_page
from lib.settings import draw_settings_page, apply_settings
from lib.markers import draw_markers_page



class AppDisplay:
    # initialiser function
    username = ""
    def __init__(self, settings, width = 480, height = 720):
        self.width = width
        self.height = height

        self.settings = settings

        self.itemInfo = []
        self.map_widget = []

        self.window = Tk() # main window object
        self.window.protocol("WM_DELETE_WINDOW", self.close) # stop the main loop if the X button is pressed

        # name and icon
        self.window.iconbitmap('images/logo_v2.ico')
        self.window.title("Johannesburg Waste Tracker")
        
        # open window at the centre of the screen
        screen_width = self.window.winfo_screenwidth()
        window_pos = int((screen_width / 2) - (width / 2))
        self.window.geometry(f'{width}x{height}+{window_pos}+10')

        # Canvas allows for shapes/images to be drawn to the screen + handles user input
        self.c = Canvas(self.window, width=width, height=height, bg='white') 
        self.c.pack()

        # lists to hold objects drawn to the screen - cobjects is for stuff on the canvas, widgets is for buttons, labels, etc
        self.cobjects = []
        self.widgets = []

        # loaded images go in this dictionary so they remain loaded
        self.images = {}

        # load map by creating a frame for it
        self.map_frame = Frame(self.window, width=self.width, height=self.height)
        self.running = True # used to control the main loop

        # stores the username once logged in
        self.username = ''

        # Bind the page functions as methods
        self.draw_front_page = lambda: draw_front_page(self)
        self.draw_register_page = lambda: draw_register_page(self)
        self.open_map = lambda: open_map(self)
        self.open_welcome_page = lambda: draw_welcome_page(self)
        self.open_settings_page = lambda: draw_settings_page(self)
        self.apply_settings = lambda: apply_settings(self)

        
        self.open_welcome_page()

    def open_markers_page(self):
        self.clear_screen()
        
        # Draw the markers page
        draw_markers_page(self)

    def open_shopping_page(self):
        self.clear_screen()
            
        # Draw the shopping page
        draw_shopping_page(self)

    def return_to_front_page(self):
        self.clear_screen()

        # Recreate the front page
        self.draw_front_page()

    def clear_screen(self):
        for object in self.cobjects:
            self.c.delete(object)
        for widget in self.widgets:
            widget.destroy()
        self.cobjects = []
        self.widgets = []

        # Remove the map widget if it exists
        if self.map_widget != []:
            self.map_widget.destroy() # type: ignore
            self.map_widget = []
    
    # button functions
    def log_in_pressed(self):
        valueList = []
        print(len(self.widgets))
        for i in range(0, len(self.widgets)):
            if isinstance(self.widgets[i], Entry):
                valueList.append(self.widgets[i].get())
        
        # Call logInUser
        user_id = logInUser(valueList)
        
        if user_id:
            print("Successfully logged in!")
            self.username = valueList[0]
            self.user_id = user_id 
            AppDisplay.username = valueList[0]
            self.open_map()
        else:
            print("Error logging in...")
            self.cobjects.append(
                self.c.create_text(
                    self.width/2, (self.height/2)+240,
                    fill='red', font='Arial 12',
                    text='The email or password is incorrect.',
                    anchor='n'
                )
            )


    def register_pressed(self):
        print (type(self.widgets[0]))
        valueList = []
        print(len(self.widgets))
        for i in range(0, len(self.widgets)):
            if isinstance(self.widgets[i], Entry):
                valueList.append(self.widgets[i].get())
        print(valueList)

        inputUserData = registerUser(valueList)
        if inputUserData:
            print("User successfully registered!")
            # take them to the login page with the username already input
            self.draw_front_page()
            self.widgets[0].insert(0, valueList[0])

        else:
            print("user registration error/failed")
            # display error message
            self.cobjects.append(
                self.c.create_text(self.width/2, (self.height/2)+280, fill='red', font='Arial 12', text='An error occurred.', anchor='n')
            )

    # run every frame
    def update(self):
        self.window.update()
    
    # handle exiting the mainloop - bound to X button
    def close(self):
        self.window.destroy()
        self.running = False
    
    def getChecked(self):
        itemsSelected = []
        priceTotal = 0

        for i in self.itemInfo:
            isChecked = i[0]
            itemName = i[1]
            itemPrice = i[2]

            if isChecked.get():
                itemsSelected.append(itemName)
                priceTotal += itemPrice
            
        print(itemsSelected)
        print(priceTotal)

        if hasattr(self, "shopBasketFrame"):
            for widget in self.shopBasketFrame.winfo_children():
                    widget.destroy()
        
        if len(itemsSelected) <= 0:
            return
        
        self.shopBasketFrame = Frame(self.window, bg="white")            
        self.shopBasketFrame.place(relx=0.50, rely=0.50, anchor='center')
        self.widgets.append(self.shopBasketFrame)

        itemListLabel = Label(self.shopBasketFrame, text=f"YOUR CHECKOUT ITEMS: {itemsSelected}", font=('Arial', 14), bg='white')
        itemListLabel.pack(side="top")
        self.widgets.append(itemListLabel)

        totalPriceLabel = Label(self.shopBasketFrame, text=f"TOTAL COST: {priceTotal} TP", font=('Arial', 14), bg='white')
        totalPriceLabel.pack(side="top")
        self.widgets.append(totalPriceLabel)

        buyBtn = Button(self.shopBasketFrame, font='Arial 14', justify='center', background="#3b7f3b", foreground='white',activebackground="#226D22", activeforeground='white',text='Buy Item')
        buyBtn.pack(side="top")
        self.widgets.append(buyBtn)
        
          
    

            


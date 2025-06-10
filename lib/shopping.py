# shopping.py
from tkinter import Button, Label, Frame, Checkbutton, BooleanVar, PhotoImage, font
#from tkinter .messagebox import showinfo
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
from lib.databaseConnectionFront import getCurrentUserTP, getAllShopItems, getAllShopPrices


def draw_shopping_page(self):
    self.clear_screen()
    self.currency = 0
    self.itemInfo = []

    if self.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = "#2A2A2E"
        highlight = 'white'
    
    if self.settings['textsize'] == 'Normal':
        textsize = 12
        smalltext = 8
        bigtext = 30
    else:
        textsize = 20
        smalltext = 20
        bigtext = 30

    #Shop Heading

    headingFrame = Frame(self.window, bg=colour)
    headingFrame.place(relx=0.64, rely=0.05, anchor='ne')
    self.widgets.append(headingFrame)

    headingFont= font.Font(family="Arial", size=16)
    coin_label = Label(headingFrame, text="Profile Image Cosmetic Shop", bg=colour, fg=highlight, font=headingFont)
    coin_label.pack(side='left')


    # Display coin icon
    coin_url = "https://cdn-icons-png.flaticon.com/512/138/138292.png"
    coin_bytes = urlopen(coin_url).read()
    coin_stream = io.BytesIO(coin_bytes)
    coin_img = Image.open(coin_stream).resize((40, 40))
    self.images['coin'] = ImageTk.PhotoImage(coin_img) 

    # Start balance at users account balance
    from lib.appdisplay import AppDisplay
    print("HII" + AppDisplay.username)
    self.currency = getCurrentUserTP(AppDisplay.username)
    print(self.currency)

    # currency logic
    currency_frame = Frame(self.window, bg=colour)
    currency_frame.place(relx=0.95, rely=0.05, anchor='ne')
    self.widgets.append(currency_frame)

    coin_label = Label(currency_frame, image=self.images['coin'], bg=colour, fg=highlight)
    coin_label.pack(side='left')

    amount_label = Label(currency_frame, text=f"{self.currency}", font=('Arial', 30), bg='white')
    amount_label.pack(side='left')
    self.widgets.append(amount_label)
    
   
    

    #Generate the item shop list from DB

    shopListFrame = Frame(self.window, bg=colour)
    shopListFrame.place(relx=0.55, rely=0.1, anchor='ne')
    self.widgets.append(shopListFrame)

    # generate selector images
    self.images['on'] = PhotoImage(width= textsize+10, height= textsize+10)
    self.images['off'] = PhotoImage(width= textsize+10, height= textsize+10)

    self.images['on'].put((colour,), to=(0, 0, textsize+9, textsize+9))
    self.images['off'].put((highlight,), to=(0, 0, textsize+9, textsize+9))

    self.images['on'].put((highlight,), to=(2, 2, textsize+7, textsize+7))
    self.images['off'].put((colour,), to=(2, 2, textsize+7, textsize+7))

    

    self.shopItemNames = getAllShopItems()
    print(self.shopItemNames)
    self.shopItemPrice = getAllShopPrices()
    for i, j in zip(self.shopItemNames, self.shopItemPrice):
        checkItem = BooleanVar()
        self.itemInfo.append((checkItem, i, j))

        checkbox = Checkbutton(shopListFrame, text=f"    {i}: {j} TP", variable=checkItem, fg=highlight,
            font=f'Arial {textsize}', pady= 25-textsize, image = self.images['off'], selectimage = self.images['on'],
            indicatoron=False, compound='left', relief='solid', background=colour, borderwidth=0,
            activebackground=colour, activeforeground=highlight, selectcolor=colour)
        
        checkbox.pack(side="top")
        self.widgets.append(checkbox)
            
            #checkbox = Checkbutton(shopListFrame, text=f"{i,j}", variable=checkItem)
            #shopListLabel = Label(shopListFrame, text=f"{i,j}", font=('Arial', 14), bg='white')
            #checkbox.pack(side="top")
            #self.widgets.append(checkbox)

    # Create the bottom bar
    bottom_bar_height = 0.1 * self.height  # 10% of the height
    bottom_bar = Label(
        self.window,
        bg=colour,
        anchor='sw',
    )

    # Place the bar at the bottom
    bottom_bar.place(
        relx=0,
        rely=1,
        anchor='sw',
        relwidth=1,
        height=bottom_bar_height
    )
    self.widgets.append(bottom_bar)

    # Back to Map button
    img = Image.open('images/backArrow.png')
    imgSmallerResize = img.resize((50,50))
    self.images['backarrow'] = ImageTk.PhotoImage(imgSmallerResize)

    back_btn = Button(self.window, image=self.images['backarrow'], activebackground=colour,
                    command=self.open_map,bg=colour, relief='solid', borderwidth=0)
    back_btn.place(x=10, y=self.height-10, width=50, height=50, anchor='sw')
    self.widgets.append(back_btn)

    # Trolley icon
    trolley_url = "https://cdn-icons-png.flaticon.com/512/107/107831.png"
    image_bytes = urlopen(trolley_url).read()
    data_stream = io.BytesIO(image_bytes)
    img = Image.open(data_stream).resize((80, 80))
    self.images['trolley'] = ImageTk.PhotoImage(img)
    trolley_btn = Button(self.window, image=self.images['trolley'], font=f'Arial {textsize}', fg=highlight,
                       bg=colour, relief="flat", command=self.getChecked, text="Update\nBasket", compound='top')
    trolley_btn.place(relx=0.75,rely=0.25,anchor='center')
    self.widgets.append(trolley_btn)

    #basketLabel = Label(self.window, text=f"Add selected to cart", font=('Arial', 10), bg='white')
    #basketLabel.place(relx=0.78, rely=0.30, anchor='center')
    #self.widgets.append(basketLabel)


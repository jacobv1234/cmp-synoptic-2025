# shopping.py
from tkinter import Button, Label, Frame, Checkbutton, BooleanVar
#from tkinter .messagebox import showinfo
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
from lib.databaseConnectionFront import getCurrentUserTP, getAllShopItems, getAllShopPrices


def draw_shopping_page(self):
    self.clear_screen()
    self.currency = 0
    self.itemInfo = []

    # Display coin icon
    coin_url = "https://cdn-icons-png.flaticon.com/512/138/138292.png"
    coin_bytes = urlopen(coin_url).read()
    coin_stream = io.BytesIO(coin_bytes)
    coin_img = Image.open(coin_stream).resize((24, 24))
    self.images['coin'] = ImageTk.PhotoImage(coin_img) 

    # currency logic
    currency_frame = Frame(self.window, bg='white')
    currency_frame.place(relx=0.95, rely=0.05, anchor='ne')
    self.widgets.append(currency_frame)

    coin_label = Label(currency_frame, image=self.images['coin'], bg='white')
    coin_label.pack(side='left')

    amount_label = Label(currency_frame, text=f"{self.currency}", font=('Arial', 14), bg='white')
    amount_label.pack(side='left')
    self.widgets.append(amount_label)
    
    # Start balance at users account balance
    from lib.appdisplay import AppDisplay
    print("HII" + AppDisplay.username)
    self.currency = getCurrentUserTP(AppDisplay.username)
    
    
    currency_frame = Frame(self.window, bg='white')
    currency_frame.place(relx=0.95, rely=0.05, anchor='ne')
    self.widgets.append(currency_frame)

    coin_label = Label(currency_frame, image=self.images['coin'], bg='white')
    coin_label.pack(side='left')

    amount_label = Label(currency_frame, text=f"{self.currency}", font=('Arial', 14), bg='white')
    amount_label.pack(side='left')
    self.widgets.append(amount_label)

    #Generate the item shop list from DB

    shopListFrame = Frame(self.window, bg="white")
    shopListFrame.place(relx=0.50, rely=0.25, anchor='center')
    self.widgets.append(shopListFrame)

    

    self.shopItemNames = getAllShopItems()
    print(self.shopItemNames)
    self.shopItemPrice = getAllShopPrices()
    for i, j in zip(self.shopItemNames, self.shopItemPrice):
        checkItem = BooleanVar()
        self.itemInfo.append((checkItem, i, j))
        checkbox = Checkbutton(shopListFrame, text=f"{i}: {j} TP", variable=checkItem)
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
        bg="white",
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
    back_btn = Button(self.window, text="Back to Map", 
                    command=self.open_map)
    back_btn.place(x=20, y=self.height-40, width=100, height=30)
    self.widgets.append(back_btn)

    # Trolley icon
    trolley_url = "https://cdn-icons-png.flaticon.com/512/107/107831.png"
    image_bytes = urlopen(trolley_url).read()
    data_stream = io.BytesIO(image_bytes)
    img = Image.open(data_stream).resize((30, 30))
    self.images['trolley'] = ImageTk.PhotoImage(img)
    trolley_btn = Button(self.window, image=self.images['trolley'],
                       bg="white", relief="flat", command=self.getChecked, text="Add to Basket")
    trolley_btn.place(x=self.width-125, y=self.height-550)
    self.widgets.append(trolley_btn)


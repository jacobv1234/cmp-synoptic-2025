# shopping.py
from tkinter import Button, Label, Frame
from PIL import Image, ImageTk
import io
from urllib.request import urlopen

def draw_shopping_page(self):
    self.clear_screen()
    self.currency = 0

    # Currency display with coin icon
    coin_url = "https://cdn-icons-png.flaticon.com/512/138/138292.png"
    coin_bytes = urlopen(coin_url).read()
    coin_stream = io.BytesIO(coin_bytes)
    coin_img = Image.open(coin_stream).resize((24, 24))
    self.images['coin'] = ImageTk.PhotoImage(coin_img) 

    # currency logic here not finished
    currency_frame = Frame(self.window, bg='white')
    currency_frame.place(relx=0.95, rely=0.05, anchor='ne')
    self.widgets.append(currency_frame)

    coin_label = Label(currency_frame, image=self.images['coin'], bg='white')
    coin_label.pack(side='left')

    amount_label = Label(currency_frame, text=f"{self.currency}", font=('Arial', 14), bg='white')
    amount_label.pack(side='left')
    self.widgets.append(amount_label)
    
    # Start balance at 0
    self.currency = 0
    
    currency_frame = Frame(self.window, bg='white')
    currency_frame.place(relx=0.95, rely=0.05, anchor='ne')
    self.widgets.append(currency_frame)

    coin_label = Label(currency_frame, image=self.images['coin'], bg='white')
    coin_label.pack(side='left')

    amount_label = Label(currency_frame, text=f"{self.currency}", font=('Arial', 14), bg='white')
    amount_label.pack(side='left')
    self.widgets.append(amount_label)


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
                       bg="white", relief="flat")
    trolley_btn.place(x=self.width-50, y=self.height-45)
    self.widgets.append(trolley_btn)

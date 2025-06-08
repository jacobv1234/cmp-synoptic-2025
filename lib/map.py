import tkintermapview
import tkinter as tk
from tkinter import Label, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw
import io
from urllib.request import urlopen
from lib.markers import draw_markers_page
from lib.databaseConnectionFront import getMarkerCountForUser

def open_map(self):
    # Remove all widgets from the window
    self.clear_screen()

    if self.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = '#2A2A2E'
        highlight = 'white'

    # Create and pack the map widget directly in the main window
    self.map_widget = tkintermapview.TkinterMapView(
        self.window,
        width=self.width,
        height=self.height,
        corner_radius=0
    )

    # Place the map widget to fill the entire window
    self.map_widget.place(relx=0, rely=0, relwidth=1, relheight=1)
    # Configure map settings
    self.map_widget.set_position(-26.2041, 28.0473) # Example coordinates for Johannesburg
    self.map_widget.set_zoom(13)
    self.map_widget.set_marker(-26.2041, 28.0473)

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

    if not hasattr(self, 'icon_images'):
        self.icon_images = {}

    icon_size = int(bottom_bar_height * 0.6)
    icons_info = [
        ('back', 'https://cdn-icons-png.flaticon.com/512/6443/6443396.png', self.return_to_front_page),
        ('shop', 'https://cdn-icons-png.flaticon.com/512/2838/2838895.png', self.open_shopping_page),
        ('profile', 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png', lambda: print("Profile clicked")),
        ('settings', 'https://cdn-icons-png.flaticon.com/512/563/563541.png', self.open_settings_page)
    ]

    # Calculate spacing for icons
    total_icons = len(icons_info)
    spacing = self.width / (total_icons + 1) 

    for idx, (name, url, command) in enumerate(icons_info):
        # Download image from URL
        image_bytes = urlopen(url).read()
        data_stream = io.BytesIO(image_bytes)
        img = Image.open(data_stream).resize((icon_size, icon_size))
        self.icon_images[name] = ImageTk.PhotoImage(img)

        # Create green overlay
        green_color = (59, 127, 59, 255)
        green_img = Image.new("RGBA", img.size, green_color)
        green_icon = Image.composite(green_img, img, img.split()[-1])  # Use alpha channel
        self.icon_images[name] = ImageTk.PhotoImage(green_icon)

        btn = Button(
            self.window,
            image=self.icon_images[name],
            bg=colour,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=command
        )
        
        # Calculate x-position for even spacing
        x_position = spacing * (idx + 1) - (icon_size / 2)
        
        btn.place(
            x=x_position,
            y=self.height - bottom_bar_height/2 - icon_size/2,
            width=icon_size,
            height=icon_size
        )
        self.widgets.append(btn)


    

    bar_width = 195
    bar_height = 70  # or int(self.height * 0.1) for 10% of height

    top_bar = tk.Frame(
        self.window,
        bg="white",
        width=bar_width,
        height=bar_height
    )
    top_bar.place(
        relx=1, rely=0, anchor='ne',
        width=bar_width,
        height=bar_height
    )
    self.widgets.append(top_bar)

    openMarkerImg = Image.open("images/addTrashMarkerBTN.png")
    self.addMarkerImg = ImageTk.PhotoImage(openMarkerImg)
    addMarkerButton = Button(top_bar, image = self.addMarkerImg, command=lambda:draw_markers_page(self))
    addMarkerButton.place(x=0, y=0, width = bar_width, height = bar_height)
    self.widgets.append(addMarkerButton)

    
    
    
    
    # # Create a white circle with green border
    # circle_size = 50
    # circle_img = Image.new("RGBA", (circle_size, circle_size), (0, 0, 0, 0))
    # draw = ImageDraw.Draw(circle_img)
    # draw.ellipse((0, 0, circle_size-1, circle_size-1), fill="white", outline="#3b7f3b", width=2)

    # # # Load and paste warning icon into the circle
    # # warning_img = Image.open("images/addTrashMarkerBTN.png")
    # # warning_img = warning_img.resize((150, 150), 0)
    # # warningImgSize = 50
    # # #offset = ((circle_size - warning_img.width)//2, (circle_size - warning_img.height)//2)
    # # #circle_img.paste(warning_img)

    # # if not hasattr(self, 'icon_images'):
    # #     self.icon_images = {}
    # # self.icon_images['warning_circle'] = ImageTk.PhotoImage(warning_img)

    # # Create the warning icon button in the top bar
    # warning_button = Button(
    #     top_bar,
    #     image=self.icon_images['warning_circle'],
    #     bg="white",
    #     relief="flat",
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda:draw_markers_page(self)
    # )
    # warning_button.place(
    #     x=10,
    #     y=(bar_height - circle_size)//2,
    #     width=circle_size,
    #     height=circle_size
    # )
    # self.widgets.append(warning_button)

    number = str(getMarkerCountForUser(self.user_id))
    font = ("Arial", 10, "bold")

    # To create text
    number_label_shadow = tk.Label(
        top_bar,
        text=number,
        font=font,
        fg="black",
        bg="white"
    )
    number_label_shadow.place(
        x=(10 + 50 + 10)+48,
        y=((bar_height - 24)//2)+31,
        height=14
    )
    number_label = tk.Label(
        top_bar,
        text=(f"{number} Markers"),
        font=font,
        fg="#133a6f",
        bg=(addMarkerButton.cget("bg"))
    )
    number_label.place(
        x=(10 + 50 + 10)+48,
        y=((bar_height - 24)//2)+31,
        height=14
    )

    self.widgets.extend([number_label_shadow, number_label])
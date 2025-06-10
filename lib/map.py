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
        ('profile', 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png', self.open_profile_page),
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

    bar_width = int(self.width * 0.19)  # 20% of width
    bar_height = int(self.height * 0.09)

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

    number = str(getMarkerCountForUser(self.user_id))

    # Load plus icon
    icon_url = "https://cdn-icons-png.flaticon.com/512/14090/14090273.png"
    icon_bytes = urlopen(icon_url).read()
    icon_img = Image.open(io.BytesIO(icon_bytes)).resize((40, 40), Image.LANCZOS)
    icon_tk = ImageTk.PhotoImage(icon_img)
    if not hasattr(self, 'icon_images'):
        self.icon_images = {}
    self.icon_images['add_icon'] = icon_tk

    # Create a frame inside the top_bar for icon and text
    icon_text_frame = tk.Frame(
        top_bar,
        bg="white"
    )
    icon_text_frame.pack(fill="both", expand=True)

    # Configure three columns: [spacer | number | icon]
    icon_text_frame.grid_columnconfigure(0, weight=1)  # Spacer expands
    icon_text_frame.grid_columnconfigure(1, weight=0)  # Number label
    icon_text_frame.grid_columnconfigure(2, weight=0)  # Icon

    number_label = tk.Label(
        icon_text_frame,
        text=f"{number}",
        font=("Arial", 18, "bold"),
        fg="#3b7f3b",
        bg="white",
        anchor="e"
    )
    number_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="e")

    addMarkerButton = tk.Button(
        icon_text_frame,
        image=self.icon_images['add_icon'],
        bg="white",
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: draw_markers_page(self)
    )
    addMarkerButton.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

    self.widgets.extend([addMarkerButton, number_label])

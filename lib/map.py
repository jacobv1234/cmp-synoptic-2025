import tkintermapview
from tkinter import Label, Button
from PIL import Image, ImageTk
import io
from urllib.request import urlopen

def open_map(self):
        # Remove all widgets from the window
        self.clear_screen()

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

        if not hasattr(self, 'icon_images'):
            self.icon_images = {}

        icon_size = int(bottom_bar_height * 0.6)
        icons_info = [
            ('back', 'https://cdn-icons-png.flaticon.com/512/93/93634.png', self.return_to_front_page),
            ('shop', 'https://cdn-icons-png.flaticon.com/512/107/107831.png', self.open_shopping_page),
            ('profile', 'https://cdn-icons-png.flaticon.com/512/1077/1077012.png', lambda: print("Profile clicked")),
            ('settings', 'https://cdn-icons-png.flaticon.com/512/2099/2099058.png', lambda: print("Settings clicked"))
        ]

        # Calculate spacing for even distribution
        total_icons = len(icons_info)
        spacing = self.width / (total_icons + 1) 

        for idx, (name, url, command) in enumerate(icons_info):
            # Download image from URL
            image_bytes = urlopen(url).read()
            data_stream = io.BytesIO(image_bytes)
            img = Image.open(data_stream).resize((icon_size, icon_size))
            self.icon_images[name] = ImageTk.PhotoImage(img)
            
            btn = Button(
                self.window,
                image=self.icon_images[name],
                bg="white",
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


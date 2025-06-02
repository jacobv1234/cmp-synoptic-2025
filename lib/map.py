import tkintermapview
from tkinter import Label, Button

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
        self.map_widget.set_position(51.5074, -0.1278)
        self.map_widget.set_zoom(13)
        self.map_widget.set_marker(51.5074, -0.1278, text="London")

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

        # Create the back button
        back_button = Button(
            self.window,
            text="  Back  ",
            bg="white",
            fg="#444444",
            anchor="w",
            relief="flat",
            command=self.return_to_front_page
        )

        # Place the button
        back_button.place(
            relx=0,
            rely=1.0,
            anchor='sw',
            width=100,
            height=bottom_bar_height
        )
        self.widgets.append(back_button)
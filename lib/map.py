import tkintermapview
import tkinter as tk
from tkinter import Label, Button, messagebox
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
from lib.markers import draw_markers_page
from lib.databaseConnectionFront import getMarkerCountForUser
from lib.databaseConnectionFront import get_connection

def open_map(self):
    # Remove all widgets from the window
    self.clear_screen()
    self.window.update()

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

    # Function to darkern a color
    def darken_color(hex_color):
        amount = 0.3
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, int(c - c * amount)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*darker_rgb)
        

    try:
        conn, cur = get_connection()

        # Fetch garbage coordinates, types, and IDs from the database that are not cleaned
        cur.execute("""
            SELECT 
                garbageID,
                ST_AsText(garbageCoord) AS wkt,
                garbageType,
                garbageName,
                garbageDate1,
                garbageStatus,
                userID1
            FROM userGarbage
            WHERE garbageStatus IS NULL
        """)

        results = cur.fetchall()
        print(f"Number of markers found: {len(results)}")

        # Fetch all results
        for garbage_id, wkt, garbage_type, garbage_name, garbage_date, garbage_status, user_id in results:
            coords = wkt.replace('POINT(', '').replace(')', '').split()
            lon, lat = map(float, coords)
            
            # Explicit color selection
            if garbage_type == 'light':
                color = '#3b7f3b'  # green
            elif garbage_type == 'mild':
                color = '#808080'  # gray
            elif garbage_type == 'severe':
                color = '#FFA500'  # orange
            elif garbage_type == 'dangerous':
                color = '#FF0000'  # red

            # Create marker data dictionary to store in the marker
            marker_data = {
                'id': garbage_id,
                'name': garbage_name,
                'type': garbage_type,
                'coordinates': (lat, lon),
                'report_date': garbage_date,
                'status': garbage_status,
                'reporter_id': user_id
            }

            # Add marker to the map with click handler and data
            marker = self.map_widget.set_marker(
                lat,
                lon,
                marker_color_circle=color,
                marker_color_outside=darken_color(color),
                command=lambda marker: self.open_resolve_report_page(marker.data),
                data=marker_data
            )

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to load markers: {str(e)}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()


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
        bg=colour,
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
        bg=colour
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
        bg=colour,
        anchor="e"
    )
    number_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="e")

    addMarkerButton = tk.Button(
        icon_text_frame,
        image=self.icon_images['add_icon'],
        bg=colour,
        relief="flat",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: draw_markers_page(self)
    )
    addMarkerButton.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="e")

    self.widgets.extend([addMarkerButton, number_label])

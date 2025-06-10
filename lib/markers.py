from tkinter import Tk, Label, Button, Entry, Frame, StringVar, filedialog, messagebox
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import tkintermapview
from datetime import datetime
from lib.databaseConnectionFront import get_connection


# Function to create a marker with icons and indicators 
def create_marker_type_selector(app_display, parent, marker_type_var, bgcol):
    icon_files = {
        'light': 'images/exclamation-green.png',
        'mild': 'images/exclamation-grey.png',
        'severe': 'images/exclamation-yellow.png',
        'dangerous': 'images/exclamation-red.png'
    }
    color_map = {
        'light': '#3b7f3b',
        'mild': '#808080',
        'severe': '#FFA500',
        'dangerous': '#FF0000',
    }
    app_display.marker_icons = {}
    icon_size = 55

    # Keep references to images to prevent garbage collection
    if not hasattr(app_display, 'marker_icon_images'):
        app_display.marker_icon_images = []

    # Configure columns for even spacing
    for i in range(4):
        parent.grid_columnconfigure(i, weight=1, uniform="icon")

    # Function to select marker type and update indicator
    def select_type(mtype):
        for mt, widgets in app_display.marker_icons.items():
            widgets['indicator'].config(bg=bgcol)
        app_display.marker_icons[mtype]['indicator'].config(bg=color_map[mtype])
        marker_type_var.set(mtype)
     
    # Create buttons for each marker type
    for idx, (mtype, file_path) in enumerate(icon_files.items()):
        try:
            img = Image.open(file_path)
            img.thumbnail((icon_size, icon_size), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue

        app_display.marker_icon_images.append(img_tk)
        app_display.marker_icons[mtype] = {}
        btn = Button(
            parent,
            image=img_tk,
            bg=bgcol,
            borderwidth=0,
            command=lambda mt=mtype: select_type(mt)
        )
        btn.grid(row=0, column=idx, padx=10, pady=(0,2), sticky="ew")

        indicator = Label(parent, bg=bgcol, width=2, height=1)
        indicator.grid(row=1, column=idx, pady=(0, 4))
        app_display.marker_icons[mtype]['indicator'] = indicator

    marker_type_var.set("")

# Main page function
def draw_markers_page(self):
    self.clear_screen()

    if self.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = "#2A2A2E"
        highlight = 'white'
    
    if self.settings['textsize'] == 'Normal':
        textsize = 20
        smalltext = 11
    else:
        textsize = 25
        smalltext = 20

    # Top header
    self.cobjects.extend([
        self.c.create_text(20, 8, fill='#3b7f3b', font=f'Arial {textsize}', text='Markers', anchor='nw')
    ])

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
        ('back', 'https://cdn-icons-png.flaticon.com/512/6443/6443396.png', self.open_map),
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


    # Input frame for form and map
    input_frame = Frame(self.window, bg=colour)
    input_frame.place(relx=0.5, rely=0.1, anchor="n", width=432, height=550)
    self.widgets.append(input_frame)
    for i in range(4):
        input_frame.grid_columnconfigure(i, weight=1)

    # Marker type selector
    marker_type_var = StringVar()
    create_marker_type_selector(self, input_frame, marker_type_var, colour)

    # Title Entry
    title_label = Label(input_frame, text="Title:", bg=colour, font=("Arial", smalltext), fg=highlight)
    title_label.grid(row=2, column=0, columnspan=1, pady=(10, 2), padx=(10, 2), sticky="w")

    self.title_entry = Entry(input_frame, font=("Arial", smalltext), bg=colour, fg="black")
    self.title_entry.grid(row=2, column=1, columnspan=3, pady=(10, 2), padx=(2, 10), sticky="ew")

    # Image Upload Section
    self.selected_image = None

    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.selected_image = file_path
            image_label.config(text=file_path.split("/")[-1])
        else:
            self.selected_image = None
            image_label.config(text="No image selected")

    upload_btn = Button(
        input_frame,
        text="Upload Image",
        command=upload_image,
        bg="#3b7f3b",
        fg="white",
        relief="flat",
        font=("Arial", smalltext)
    )
    upload_btn.grid(row=3, column=0, columnspan=4, pady=(2, 10), sticky="ew")
    self.widgets.append(upload_btn)

    image_label = Label(input_frame, text="No image selected", bg=colour, font=("Arial", smalltext), fg=highlight)
    image_label.grid(row=4, column=0, columnspan=4, pady=(2, 2), sticky="ew")
    self.widgets.append(image_label)

    # Map widget
    self.selected_coords = None  # To store map coordinates

    map_widget = tkintermapview.TkinterMapView(input_frame, width=400, height=200, corner_radius=0)
    map_widget.grid(row=5, column=0, columnspan=4, pady=(0, 10), sticky="ew")

    # Set default position (Johannesburg)
    map_widget.set_position(-26.2041, 28.0473)
    map_widget.set_zoom(10)

    # Map click handler
    def map_click_event(coordinates_tuple):
        self.selected_coords = coordinates_tuple
        map_widget.delete_all_marker()
        map_widget.set_marker(coordinates_tuple[0], coordinates_tuple[1])

    map_widget.add_left_click_map_command(map_click_event)
    self.widgets.append(map_widget)

    # Add Marker Button
    def add_marker():
        marker_type = marker_type_var.get()
        title = self.title_entry.get().strip()
        if not marker_type:
            messagebox.showerror("Error", "Please select a marker type!")
            return
        if not title:
            messagebox.showerror("Error", "Please enter a title!")
            return
        if not self.selected_coords:
            messagebox.showerror("Error", "Please select a location on the map!")
            return

        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = """INSERT INTO userGarbage 
                    (garbageType, garbageCoord, userID1, garbagePic1, garbageDate1, garbageName)
                    VALUES (%s, ST_GeomFromText(%s), %s, %s, %s, %s)"""
            lat, lon = self.selected_coords
            gps_wkt = f'POINT({lon} {lat})'
            image_blob = None
            if self.selected_image:
                with open(self.selected_image, "rb") as f:
                    image_blob = f.read()
            params = (
                marker_type,
                gps_wkt,
                self.user_id,
                image_blob,
                now,
                title
            )
            conn, cur = get_connection()
            cur.execute(query, params)
            conn.commit()
            self.title_entry.delete(0, 'end')
            self.selected_image = None
            image_label.config(text="No image selected")
            map_widget.delete_all_marker()
            marker_type_var.set("")
            self.selected_coords = None
            messagebox.showinfo("Success", "Marker added successfully!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'cur' in locals():
                cur.close()

    add_btn = Button(
        input_frame,
        text="Add Marker",
        command=add_marker,
        bg="#3b7f3b",
        fg="white",
        font=("Arial", textsize, "bold"),
        relief="flat",
        padx=10,
        pady=6
    )
    add_btn.grid(row=6, column=0, columnspan=4, pady=(12, 2), sticky="ew")
    self.widgets.append(add_btn)

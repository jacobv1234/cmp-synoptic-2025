from tkinter import Label, Button, messagebox, filedialog, StringVar, Frame
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import geocoder
from datetime import datetime
from lib.databaseConnectionFront import get_connection

# Function to create a marker with icons and indicators (input fields)
def create_marker_type_selector(app_display, parent, marker_type_var):
    icon_urls = {
        'light': 'https://cdn-icons-png.flaticon.com/512/3756/3756715.png',
        'mild': 'https://cdn-icons-png.flaticon.com/512/3756/3756712.png',
        'severe': 'https://cdn-icons-png.flaticon.com/512/3756/3756713.png',
        'dangerous': 'https://cdn-icons-png.flaticon.com/512/3756/3756714.png'
    }
    color_map = {
        'light': '#808080',
        'mild': '#FFD700',
        'severe': '#FFA500',
        'dangerous': '#FF0000',
    }
    app_display.marker_icons = {}
    icon_size = 55

    # Create a frame for the selector
    selector_frame = Frame(parent, bg="white")
    selector_frame.grid(row=0, column=0, columnspan=4, pady=(4, 10), sticky="ew")

    for i in range(4):
        selector_frame.grid_columnconfigure(i, weight=1, uniform="icon")

    # Function to select marker type and update indicator
    def select_type(mtype):
        for mt, widgets in app_display.marker_icons.items():
            widgets['indicator'].config(bg='white')
        app_display.marker_icons[mtype]['indicator'].config(bg=color_map[mtype])
        marker_type_var.set(mtype)
     
    # Create buttons for each marker type
    for idx, (mtype, url) in enumerate(icon_urls.items()):
        img_bytes = urlopen(url).read()
        img = Image.open(io.BytesIO(img_bytes)).resize((icon_size, icon_size))
        img_tk = ImageTk.PhotoImage(img)
        app_display.marker_icons[mtype] = {}
        btn = Button(
            selector_frame,
            image=img_tk,
            bg="white",
            borderwidth=0,
            command=lambda mt=mtype: select_type(mt)
        )
        btn.image = img_tk
        btn.grid(row=0, column=idx, padx=8, pady=(0,2), sticky="ew")

        indicator = Label(selector_frame, bg="white", width=2, height=1)
        indicator.grid(row=1, column=idx, pady=(0, 4))
        app_display.marker_icons[mtype]['indicator'] = indicator

    marker_type_var.set("")

def draw_markers_page(self):
    self.clear_screen()

    # Top header
    self.cobjects.extend([
        self.c.create_text(20, 8, fill='#3b7f3b', font='Arial 20', text='Markers', anchor='nw')
    ])

    # Create the bottom bar
    bottom_bar_height = 0.1 * self.height
    bottom_bar = Label(self.window, bg="white", anchor='sw')
    bottom_bar.place(relx=0, rely=1, anchor='sw', relwidth=1, height=bottom_bar_height)
    self.widgets.append(bottom_bar)

    # Navigation icons
    if not hasattr(self, 'nav_icons'):
        self.nav_icons = {}

    icon_size = int(bottom_bar_height * 0.6)
    icons_info = [
        ('back', 'https://cdn-icons-png.flaticon.com/512/6443/6443396.png', self.open_map),
        ('shop', 'https://cdn-icons-png.flaticon.com/512/2838/2838895.png', self.open_shopping_page),
        ('profile', 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png', lambda: print("Profile clicked")),
        ('settings', 'https://cdn-icons-png.flaticon.com/512/563/563541.png', self.open_settings_page)
    ]

    # Calculate spacing for icons
    total_icons = len(icons_info)
    spacing = self.width / (total_icons + 1) 
    
    for idx, (name, url, command) in enumerate(icons_info):
        image_bytes = urlopen(url).read()
        img = Image.open(io.BytesIO(image_bytes)).resize((icon_size, icon_size))
        self.nav_icons[name] = ImageTk.PhotoImage(img)
        
        # Create green overlay
        green_img = Image.new("RGBA", img.size, (59, 127, 59, 255))
        green_icon = Image.composite(green_img, img, img.split()[-1])
        self.nav_icons[name] = ImageTk.PhotoImage(green_icon)

        btn = Button(
            self.window,
            image=self.nav_icons[name],
            bg="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=command
        )
        btn.place(
            x=spacing * (idx + 1) - (icon_size / 2),
            y=self.height - bottom_bar_height/2 - icon_size/2,
            width=icon_size,
            height=icon_size
        )
        self.widgets.append(btn)

    # make objects fill the screen
    input_frame_width = int(480 * 0.9)
    input_frame_height = int(720 * 0.7) 

    from tkinter import Frame

    # Frame for input fields
    input_frame = Frame(self.window, bg="white")
    input_frame.place(relx=0.5, rely=0.18, anchor="n", width=432, height=360)
    self.widgets.append(input_frame)
    for i in range(4):
        input_frame.grid_columnconfigure(i, weight=1)

    # Marker type selector
    marker_type_var = StringVar()
    create_marker_type_selector(self, input_frame, marker_type_var)  # This should use grid inside

    # Image Upload Section
    self.selected_image = None
    image_label = Label(input_frame, text="No image selected", bg="white", font=("Arial", 11))
    image_label.grid(row=2, column=0, columnspan=4, pady=(10, 8), sticky="ew")
    self.widgets.append(image_label)

    # Function to upload an image
    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.selected_image = file_path
            image_label.config(text=file_path.split("/")[-1])

    upload_btn = Button(
        input_frame,
        text="Upload Image",
        command=upload_image,
        bg="#3b7f3b",
        fg="white",
        relief="flat",
        font=("Arial", 11)
    )
    upload_btn.grid(row=1, column=0, columnspan=4, pady=(2, 8), sticky="ew")
    self.widgets.append(upload_btn)

    # function for adding markers to the database
    def add_marker():
        marker_type = marker_type_var.get()
        gps = geocoder.ip('me').latlng
        
        if not marker_type:
            messagebox.showerror("Error", "Please select a marker type!")
            return
            
        try:
            # Get current datetime
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # SQL database query to insert markers
            query = """INSERT INTO markers 
                    (type, gps, user_id, image, timestamp)
                    VALUES (%s, ST_GeomFromText(%s), %s, %s, %s)"""
            
            # Read image (BLOB)
            image_blob = None
            if self.selected_image:
                with open(self.selected_image, "rb") as f:
                    image_blob = f.read()
            
            # Prepare GPS
            gps_wkt = f'POINT({gps[1]} {gps[0]})' if gps else None
            
            # Parameters for the query
            params = (
                marker_type,
                gps_wkt,
                self.user_id,
                image_blob, 
                now
            )
            
            # Execute query
            conn, cur = get_connection()
            cur.execute(query, params)
            conn.commit()
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
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=10,
        pady=6
    )
    add_btn.grid(row=3, column=0, columnspan=4, pady=(12, 2), sticky="ew")
    self.widgets.append(add_btn)


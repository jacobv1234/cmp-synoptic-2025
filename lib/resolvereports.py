import tkinter as tk
from tkinter import Label, Button, filedialog, messagebox
from PIL import Image, ImageTk
import io
from urllib.request import urlopen
from lib.databaseConnectionFront import get_connection
from datetime import datetime

def show_marker_title(app_instance, marker_data):
    app_instance.clear_screen()

    # Theme and sizing
    colour = 'white' if app_instance.settings['theme'] == 'Light' else '#2A2A2E'
    highlight = 'black' if app_instance.settings['theme'] == 'Light' else 'white'

    app_instance.window.geometry('480x720')
    app_instance.window.resizable(False, False)

    # Title label at top center
    title_label = tk.Label(
        app_instance.window,
        text=marker_data.get('name', 'Untitled Marker'),
        font=("Arial", 24, "bold"),
        fg='#3b7f3b',
        bg=colour
    )
    title_label.place(relx=0.5, y=36, anchor="n")
    app_instance.widgets.append(title_label)

    # Display image (if any)
    image_bytes = None
    try:
        conn, cur = get_connection()
        cur.execute(
            "SELECT garbagePic1 FROM userGarbage WHERE garbageID = %s",
            (marker_data['id'],)
        )
        result = cur.fetchone()
        if result and result[0]:
            image_bytes = result[0]
    except Exception as e:
        print(f"Error fetching image: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

    if image_bytes:
        try:
            image_stream = io.BytesIO(image_bytes)
            pil_image = Image.open(image_stream)
            pil_image = pil_image.resize((300, 200))
            tk_image = ImageTk.PhotoImage(pil_image)
            image_label = tk.Label(app_instance.window, image=tk_image, bg=colour)
            image_label.image = tk_image
            image_label.place(relx=0.5, y=90, anchor="n")
            app_instance.widgets.append(image_label)
        except Exception as e:
            error_label = tk.Label(
                app_instance.window,
                text="Image could not be loaded.",
                fg="red",
                bg=colour
            )
            error_label.place(relx=0.5, y=90, anchor="n")
            app_instance.widgets.append(error_label)
    else:
        no_image_label = tk.Label(
            app_instance.window,
            text="No image available.",
            fg=highlight,
            bg=colour
        )
        no_image_label.place(relx=0.5, y=90, anchor="n")
        app_instance.widgets.append(no_image_label)

    # Image Upload Section
    input_frame = tk.Frame(app_instance.window, bg=colour)
    input_frame.place(relx=0.5, rely=0.44, anchor="n")
    app_instance.widgets.append(input_frame)

    app_instance.selected_image = None

    def upload_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            app_instance.selected_image = file_path
            image_label_upload.config(text=file_path.split("/")[-1])
        else:
            app_instance.selected_image = None
            image_label_upload.config(text="No image selected")

    smalltext = 12

    upload_btn = Button(
        input_frame,
        text="Upload Image",
        command=upload_image,
        bg="#3b7f3b",
        fg="white",
        relief="flat",
        font=("Arial", smalltext)
    )
    upload_btn.grid(row=0, column=0, columnspan=4, pady=(2, 10), sticky="ew")
    app_instance.widgets.append(upload_btn)

    image_label_upload = Label(
        input_frame,
        text="No image selected",
        bg=colour,
        font=("Arial", smalltext),
        fg=highlight
    )
    image_label_upload.grid(row=1, column=0, columnspan=4, pady=(2, 2), sticky="ew")
    app_instance.widgets.append(image_label_upload)

    def resolve_marker():
        try: 
            query1 = "UPDATE User SET trashCleaned = trashCleaned + 1 WHERE userID = %s"
            conn1, cur1 = get_connection()
            cur1.execute(query1, (app_instance.user_id,))
            conn1.commit()
        except Exception as e:
            conn1.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'cur1' in locals():
                cur1.close()
        
        try:
            query2 = "UPDATE User SET userTrashPoints = userTrashPoints + 20 WHERE userID = %s"
            conn2, cur2 = get_connection()
            cur2.execute(query2, (app_instance.user_id,))
            conn2.commit()
        except Exception as e:
            conn2.rollback()
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'cur2' in locals():
                cur2.close()
        
        try:
            # Read image bytes if an image was selected
            image_bytes = None
            if app_instance.selected_image:
                with open(app_instance.selected_image, "rb") as f:
                    image_bytes = f.read()

            conn, cur = get_connection()
            # Update garbagePic2, userID2, garbageDate2, and garbageStatus for this marker
            cur.execute("""
                UPDATE userGarbage 
                SET garbagePic2 = %s, 
                    userID2 = %s, 
                    garbageDate2 = %s, 
                    garbageStatus = 'Cleaned'
                WHERE garbageID = %s
            """, (image_bytes, app_instance.user_id, datetime.now(), marker_data['id']))
            conn.commit()
            messagebox.showinfo("Success", "Marker resolved and image uploaded!\nYou got 20 TP")
            app_instance.open_map()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resolve marker: {str(e)}")
        finally:
            if 'cur' in locals(): cur.close()
            if 'conn' in locals(): conn.close()
        

    resolve_btn = Button(
        input_frame,
        text="Resolve Marker",
        command=resolve_marker,
        bg="#3b7f3b",
        fg="white",
        relief="flat",
        font=("Arial", smalltext)
    )
    resolve_btn.grid(row=2, column=0, columnspan=4, pady=(10, 10), sticky="ew")
    app_instance.widgets.append(resolve_btn)

    # Bottom bar
    bottom_bar_height = 0.1 * app_instance.height
    bottom_bar = Label(
        app_instance.window,
        bg=colour,
        anchor='sw',
    )
    bottom_bar.place(
        relx=0,
        rely=1,
        anchor='sw',
        relwidth=1,
        height=bottom_bar_height
    )
    app_instance.widgets.append(bottom_bar)

    if not hasattr(app_instance, 'icon_images'):
        app_instance.icon_images = {}

    icon_size = int(bottom_bar_height * 0.6)
    icons_info = [
        ('back', 'https://cdn-icons-png.flaticon.com/512/6443/6443396.png', app_instance.open_map),
        ('shop', 'https://cdn-icons-png.flaticon.com/512/2838/2838895.png', app_instance.open_shopping_page),
        ('profile', 'https://cdn-icons-png.flaticon.com/512/1077/1077063.png', app_instance.open_profile_page),
        ('settings', 'https://cdn-icons-png.flaticon.com/512/563/563541.png', app_instance.open_settings_page)
    ]

    total_icons = len(icons_info)
    spacing = app_instance.width / (total_icons + 1) 

    for idx, (name, url, command) in enumerate(icons_info):
        try:
            image_bytes_icon = urlopen(url).read()
            data_stream = io.BytesIO(image_bytes_icon)
            img = Image.open(data_stream).resize((icon_size, icon_size))
            app_instance.icon_images[name] = ImageTk.PhotoImage(img)

            green_color = (59, 127, 59, 255)
            green_img = Image.new("RGBA", img.size, green_color)
            green_icon = Image.composite(green_img, img, img.split()[-1])
            app_instance.icon_images[name] = ImageTk.PhotoImage(green_icon)

            btn = Button(
                app_instance.window,
                image=app_instance.icon_images[name],
                bg=colour,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                command=command
            )
            x_position = spacing * (idx + 1) - (icon_size / 2)
            btn.place(
                x=x_position,
                y=app_instance.height - bottom_bar_height/2 - icon_size/2,
                width=icon_size,
                height=icon_size
            )
            app_instance.widgets.append(btn)
        except Exception as e:
            print(f"Error loading icon {name}: {str(e)}")

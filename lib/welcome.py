import tkinter as tk
from PIL import Image, ImageTk

def draw_welcome_page(self):
    self.clear_screen()
    self.window.configure(bg="white")

    # load the logo into app.images
    img = Image.open('images/logo.png')
    imgSmallerResize = img.resize((250,250))
    self.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)

    # Load and resize/crop background
    imgResized = img.resize((int(img.width * (self.height / img.height)), self.height))
    imgcropped = imgResized.crop((0, 0, self.width, self.height))
    self.images['bg'] = ImageTk.PhotoImage(imgcropped)

    # Display the logo
    logo_label = tk.Label(self.window, image=self.images['logo'], bg='white')
    logo_label.place(relx=0.5, rely=0.18, anchor='center')
    self.widgets.append(logo_label)

    # Welcome Text
    welcome_label = tk.Label(self.window, text="Welcome To \nJohannesburg Waste Tracker", font=("Arial", 22, "bold"), bg="white", fg="#3b7f3b")
    welcome_label.place(relx=0.5, rely=0.38, anchor='center')
    self.widgets.append(welcome_label)

    # Subtitle
    subtitle_label = tk.Label(self.window,
        text="Create an account and begin earning lots \nof cool items and rewards!",
        font=("Arial", 12), bg="white", fg="#444")
    subtitle_label.place(relx=0.5, rely=0.5, anchor='center')
    self.widgets.append(subtitle_label)

    # Get Started Button
    get_started_btn = tk.Button(self.window,
        text="Get Started",
        font=("Arial", 14, "bold"),
        bg="#3b7f3b", fg="white",
        activebackground="#3b7f3b", activeforeground="white",
        relief="flat",
        padx=20, pady=10,
        command=self.draw_register_page  # Go to register page
    )
    btn_width = int(self.width * 0.85)
    get_started_btn.place(relx=0.5, rely=0.60, anchor='center', width=btn_width, height=45)
    self.widgets.append(get_started_btn)

    # Log In Button
    login_btn = tk.Button(self.window,
        text="Log In",
        font=("Arial", 12, "bold"),
        bg="white", fg="#3b7f3b",
        activebackground="#e6e6e6", activeforeground="#3b7f3b",
        relief="flat",
        borderwidth=0,
        command=self.draw_front_page  # Go to login page
    )
    login_btn.place(relx=0.5, rely=0.72, anchor='center', width=120, height=35)
    self.widgets.append(login_btn)
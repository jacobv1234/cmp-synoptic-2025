import tkinter as tk
from PIL import Image, ImageTk

def draw_welcome_page(self):
    self.clear_screen()
    if self.settings['theme'] == 'Light':
        colour = 'white'
        highlight = 'black'
    else:
        colour = "#2A2A2E"
        highlight = 'white'
    self.window.configure(bg=colour)

    if self.settings['textsize'] == 'Normal':
        textsize = 14
        smalltext = 12
        bigtext = 22
        extranewline = ' '
        shift = 0
    else:
        textsize = 20
        smalltext = 20
        bigtext = 30
        extranewline= '\n'
        shift = 0.1
        

    # load the logo
    img = Image.open('images/logo_v2.png')
    imgSmallerResize = img.resize((200,200))
    self.images['logo'] = ImageTk.PhotoImage(imgSmallerResize)
    

    # Display the logo
    logo_label = tk.Label(self.window, image=self.images['logo'], bg=colour)
    logo_label.place(relx=0.5, rely=0.18, anchor='center')
    self.widgets.append(logo_label)

    # Welcome Text
    welcome_label = tk.Label(self.window, text=f"Welcome To \nJohannesburg{extranewline}Waste Tracker", font=("Arial", bigtext, "bold"), bg=colour, fg="#3b7f3b")
    welcome_label.place(relx=0.5, rely=0.38, anchor='center')
    self.widgets.append(welcome_label)

    # Subtitle
    subtitle_label = tk.Label(self.window,
        text=f"Create an account{extranewline}and begin earning lots \nof cool items and rewards!",
        font=("Arial", smalltext), bg=colour, fg=highlight
    )
    subtitle_label.place(relx=0.5, rely=0.5+shift, anchor='center')
    self.widgets.append(subtitle_label)

    # Get Started Button
    get_started_btn = tk.Button(self.window,
        text="Get Started",
        font=("Arial", textsize, "bold"),
        bg="#3b7f3b", fg=colour,
        activebackground="#3b7f3b", activeforeground=colour,
        relief="flat",
        padx=20, pady=10,
        command=self.draw_register_page  # Go to register page
    )
    btn_width = int(self.width * 0.85)
    get_started_btn.place(relx=0.5, rely=0.60+shift, anchor='center', width=btn_width, height=45)
    self.widgets.append(get_started_btn)

    # Log In Button
    login_btn = tk.Button(self.window,
        text="Log In",
        font=("Arial", smalltext, "bold"),
        bg=colour, fg="#3b7f3b",
        activebackground=colour, activeforeground="#3b7f3b",
        relief="flat",
        borderwidth=0,
        command=self.draw_front_page  # Go to login page
    )
    login_btn.place(relx=0.5, rely=0.72+shift, anchor='center', width=120, height=35)
    self.widgets.append(login_btn)
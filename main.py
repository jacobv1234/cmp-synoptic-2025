# third-party imports
try:
    import PIL as PIL
    import mariadb as mariadb
    import pytest as pytest
    import nuitka as nuitka
    import bcrypt as bcrypt
    import tkintermapview as tkintermapview
    import cloudinary as cloudinary

except ModuleNotFoundError:
    # automatically install modules
    from os import system
    install = input('Important modules are not installed. Install? (y/n) ')
    if install.lower() == 'y':
        system('python -m pip install pillow mariadb pytest nuitka bcrypt tkintermapview cloudinary')
        exit()

# global imports
#from time import sleep, perf_counter

# local imports
from lib.appdisplay import AppDisplay
from lib.settings import load_settings

settings = load_settings()
screen = AppDisplay(settings)

screen.window.mainloop() # run


# Alt main loop - scrapped due to not working with the map

#while screen.running:
#    start = perf_counter()
#
#    screen.update()
#
#    # lock to roughly 60fps
#    end = perf_counter()
#    difference = end - start
#    if difference < 0.017:
#        sleep(0.017 - difference)
    

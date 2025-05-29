# third-party imports
try:
    import PIL as pillow
    import mariadb as mariadb
    import pytest as pytest
except ModuleNotFoundError:
    # automatically install modules
    from os import system
    install = input('Important modules are not installed. Install? (y/n) ')
    if install.lower() == 'y':
        system('python -m pip install pillow mariadb pytest')
        exit()

# global imports
from time import sleep, perf_counter

# local imports
from lib.appdisplay import AppDisplay


screen = AppDisplay()

while screen.running:
    start = perf_counter()

    screen.update()

    # lock to roughly 60fps
    end = perf_counter()
    diff = end - start
    if diff < 0.017:
        sleep(0.017 - diff)
    

    


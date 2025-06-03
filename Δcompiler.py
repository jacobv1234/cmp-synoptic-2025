from os import system

# COMPILER INSTRUCTIONS
# run this file
# ignore any yellow warnings
# delete main.build, main.dist, main.onefile-build folders
# move EXE and any other files the program uses (except lib folder) into a new folder

# PARAMETERS
# add --disable-console to hide the terminal in the resulting EXE
# add --windows-icon-from-ico="filename.ico" to set the icon
# feel free to change --output-filename

system('python -m nuitka --standalone --onefile --output-filename="Johannesburg Flytipping Report.exe" --windows-icon-from-ico="images/logo.ico --enable-plugin=tk-inter main.py')
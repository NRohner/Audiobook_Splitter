from PIL import Image
Image.CUBIC = Image.BICUBIC
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

#############################################
#          GUI for Book Splitter App        #
#############################################

# 0.0 - Establishing some variables
window_w = 600  # Pixel width of the window
window_h = 400  # Pixel height of the window



# 1.0 - Create the main window
app = ttk.Window(themename='superhero')

# 1.1 - Set the title of the window
app.title("Book Splitter")

# 1.2 - Set the dimensions of the window to 600x400 pixels
app.geometry("600x400")

# 1.3 - Make the window non-resizeable
app.resizable(False, False)


# 2.0 - Creating the brose section to browse to the desired audio file
browse_label = ttk.Label(bootstyle='default', text='Browse to the audio file you want to split')
browse_label.pack(padx=10, pady=10)

browse_button = ttk.Button(app, text="Browse")
browse_button.pack(padx=10, pady=10)

# Run the Tkinter event loop
app.mainloop()
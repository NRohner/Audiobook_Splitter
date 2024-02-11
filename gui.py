import tkinter as tk
from tkinter import ttk, filedialog
import ttkbootstrap as tb

def create_gui():
    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

    # Create main window
    root = tk.Tk()
    root.title("Audio Book Splitter")
    root.geometry("800x400")

    # Apply superhero theme
    style = tb.Style(theme='superhero')
    style.master.title("Audio Book Splitter")

    # Browse to file section
    file_frame = ttk.Frame(root, padding="10")
    file_frame.grid(row=0, column=0, sticky="w")

    file_label = ttk.Label(file_frame, text="Select audiobook file:")
    file_label.grid(row=0, column=0, padx=(0, 10), pady=10)

    file_entry = ttk.Entry(file_frame, width=50)
    file_entry.grid(row=0, column=1, padx=(0, 10), pady=10)

    browse_button = ttk.Button(file_frame, text="Browse", command=browse_file)
    browse_button.grid(row=0, column=2, pady=10)

    # Horizontal Divider
    divider = ttk.Separator(root, orient="horizontal")
    divider.grid(row=1, column=0, sticky="ew", pady=10)

    # Preferences Section
    # preferences_label = ttk.Label(root, text="Preferences")
    # preferences_label.grid(row=2, column=0, pady=(10, 5))

    # dB Threshold Meter
    threshold_meter = tb.Meter(metersize=180, interactive=True)
    threshold_meter.grid(row=2, column=0)

    # Duration Slider
    duration_label = ttk.Label(root, text="Duration")
    duration_label.grid(row=5, column=0, pady=(0, 5))

    duration_var = tk.DoubleVar()
    duration_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal", length=200, variable=duration_var)
    duration_slider.grid(row=6, column=0, pady=(0, 5))

    duration_value_label = ttk.Label(root, textvariable=duration_var, width=5)
    duration_value_label.grid(row=6, column=1, pady=(0, 5), padx=(5, 0))

    root.mainloop()

if __name__ == "__main__":
    create_gui()

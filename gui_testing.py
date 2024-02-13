import csv
import datetime
import pathlib
import tkinter
from queue import Queue
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename

from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Audiobook Splitter')
        self.style = Style('superhero')
        self.search = SearchEngine(self, padding=10)
        self.search.pack(fill='both', expand='yes')

        # Set the window size to 600x
        self.geometry('600x300')


class SearchEngine(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.file_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()))
        self.search_term_var = tkinter.StringVar(value='txt')
        self.search_type_var = tkinter.StringVar(value='endswidth')
        self.search_count = 0
        self.dB_threshold_var = tkinter.DoubleVar(value=-40)
        self.duration_var = tkinter.DoubleVar(value=2.5)
        self.output_file_name = tkinter.StringVar(value='file_name')
        self.output_file_path = tkinter.StringVar(value=str(pathlib.Path().absolute()))

        # container for user input
        input_labelframe = ttk.Labelframe(self, text='Select an audio file', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # container for analysis parameters
        params_labelframe = ttk.Labelframe(self, text='Analysis parameters', padding=(20, 10, 10, 5))
        params_labelframe.pack(side='top', fill='x')
        params_labelframe.columnconfigure(1, weight=1)

        # container for output settings
        output_labelframe = ttk.Labelframe(self, text='Output settings', padding=(20, 10, 10, 5))
        output_labelframe.pack(side='top', fill='x')
        output_labelframe.columnconfigure(1, weight=1)

        # file path input
        ttk.Label(input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(input_labelframe, textvariable=self.file_path_var)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(input_labelframe, text='Browse', command=self.on_in_browse, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # analysis parameters
        # dB Threshold
        ttk.Label(params_labelframe, text='dB Threshold').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        dB_slider = ttk.Scale(params_labelframe, from_=-80, to=0, value=-40, variable=self.dB_threshold_var, length=520)
        dB_slider.grid(row=1, column=0, padx=10, pady=2, sticky='ew')

        # Duration
        ttk.Label(params_labelframe, text='Duration').grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        duration_slider = ttk.Scale(params_labelframe, from_=0, to=15, value=2.5, variable=self.duration_var, length=520)
        duration_slider.grid(row=3, column=0, padx=10, pady=2, sticky='ew')

        # output settings
        ttk.Label(output_labelframe, text="Output file location").grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e2 = ttk.Entry(output_labelframe, textvariable=self.output_file_path)
        e2.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(output_labelframe, text='Browse', command=self.on_out_browse, style='primary.TButton')
        b2.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        ttk.Label(output_labelframe, text="Output file name").grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e3 = ttk.Entry(output_labelframe, textvariable=self.output_file_name)
        e3.grid(row=1, column=1, sticky='ew', padx=10, pady=2)


        b3 = ttk.Button(output_labelframe, text='Save', command=self.on_save, style='success.TButton')
        b3.grid(row=1, column=2, sticky='ew', pady=2, ipadx=10)


    def on_save(self):
        """Callback for save button press"""
        pass

    def on_in_browse(self):
        """Callback for input browse"""
        path = askopenfilename(title='Select an audio file', filetypes=[('Audio Files', '*.wav;*.mp3;*.ogg')])
        if path:
            self.file_path_var.set(path)

    def on_out_browse(self):
        """Callback for output browse"""
        path = askdirectory(title='Select directory')
        if path:
            self.output_file_path.set(path)

if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()
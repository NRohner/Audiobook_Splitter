import numpy as np
import librosa
import soundfile as sf
import time
from icecream import ic
import pathlib
import tkinter
from queue import Queue
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from ttkbootstrap import Style
import tkinter.messagebox


# Roadmap and feature wishlist:
# 1. Get the basic app working in an IDE environment - DONE
# 1.5 Performance optimization - only analyze every nth sample - DONE
# 2. Error proof the user input sections
# 3. Add progress bars
# 4. Add more user control ex. ignore silence in first/last X:XX of the audio file
# 5. More control over naming of split, output files
# 6. Make a .exe for the app, so it can run outside an IDE
# 7. GUI - WIP
# 8. More advanced processing/chapter detection methods (AI??)


# Global variables

samples_per_second = 30     # This is the number of samples per second to be analyzed by the app


# Definitions
def load_audio(file_path):
    imported_audio, imported_sample_rate = librosa.load(file_path)

    return imported_audio, imported_sample_rate

# Function to convert samples into time
def samples_2_time(sample_num, sample_rate):
    total_seconds = sample_num * (1 / sample_rate)
    hours = int(total_seconds / 3600)
    minutes = int(((total_seconds / 3600) - hours) * 60)
    seconds = int(((((total_seconds / 3600) - hours) * 60) - minutes) * 60)

    time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds)

    return time_string


# Function to actually split the audio
def split_file(audio, silences):
    split_audio = []

    # Calculating the split points from silences array
    mid_pts = []

    for i in range(0, silences.shape[0]):
        mid_pt = int(((silences[i][1] - silences[i][0]) / 2) + silences[i][0])
        mid_pts.append(mid_pt)

    # Adding the first segment from the start of audio until the first split point
    split_audio.append(audio[:mid_pts[0]])

    # Adding the middle segments of audio between each split point
    for j in range(len(mid_pts) - 1):
        split_audio.append(audio[mid_pts[j]:mid_pts[j + 1]])

    # Adding the last audio segment between the last split point and the end of the file
    split_audio.append(audio[mid_pts[-1]:])

    return split_audio


# Function to write the split files to memory
def write_files(audio_chunks, sample_rate):
    # Prompting user if they want to split and write the files
    proceed = str(input("Do you want to proceed and split the file and save the resulting audio chunks? [y/n]"))
    proceed = proceed.lower()

    if proceed == "y":
        # Prompt for destination folder path
        dest_path = str(input("Please enter the folder path to the location you want to save the new audio files"
                              " [NO QUOTATION MARKS!]: "))

        # Prompt for the desired file name prefix
        file_prefix = str(input("Please enter the desired file name prefix: "))

        # Write the files
        for i in range(len(audio_chunks)):
            file_name = str(dest_path + "/" + file_prefix + "_" + str(i + 1) + ".mp3")
            sf.write(file_name, audio_chunks[i], sample_rate)
        print("Your files have been written to the destination folder.")
        print("Thank you for using Audio Book Splitter!")

    else:
        print("Thank you for using Audio Book Splitter!")


# Class Definitions
class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Audiobook Splitter')
        self.style = Style('superhero')
        self.window = MainWindow(self, padding=10)
        self.window.pack(fill='both', expand='yes')

        # Set the window size to 600x300
        self.geometry('600x380')


class MainWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables
        self.file_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()))
        self.dB_threshold_var = tkinter.DoubleVar(value=-40)
        self.duration_var = tkinter.DoubleVar(value=2.5)
        self.output_file_name = tkinter.StringVar(value='file_name')
        self.output_folder_path = tkinter.StringVar(value=str(pathlib.Path().absolute()))

        # Dynamic Label Variables - starting by setting them to the defualt values
        self.dB_label_value = tkinter.StringVar(value="-40")
        self.duration_label_value = tkinter.StringVar(value="2.5")

        # Progress bar variable
        self.prog_bar_value = tkinter.DoubleVar(value=0)

        # Boolean variables for error proofing
        self.has_analyzed = False

        # Audio and sample rate variables
        self.audio = []
        self.sample_rate = 0



        # container for user input
        input_labelframe = ttk.Labelframe(self, text='Select an audio file', padding=(20, 10, 10, 5))
        input_labelframe.pack(side='top', fill='x')
        input_labelframe.columnconfigure(1, weight=1)

        # container for analysis parameters
        params_labelframe = ttk.Labelframe(self, text='Analysis parameters', padding=(20, 10, 10, 5))
        params_labelframe.pack(side='top', fill='x')
        params_labelframe.columnconfigure(1, weight=1)

        # container for analyze button and progress bar
        analyze_labelframe = ttk.Labelframe(self, text='Analyze', padding=(20, 10, 10, 5))
        analyze_labelframe.pack(side='top', fill='x')
        analyze_labelframe.columnconfigure(1, weight=1)

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
        ttk.Label(params_labelframe, text='dB Threshold: ').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        dB_slider = ttk.Scale(params_labelframe, from_=-80, to=0, value=-40, variable=self.dB_threshold_var, length=520, command=self.update_dB_label)
        dB_slider.grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        # dB Value Label
        dB_value_label = ttk.Label(params_labelframe, textvariable=self.dB_label_value)
        dB_value_label.grid(row=0, column=0, padx=100, pady=2, sticky='w')


        # Duration
        ttk.Label(params_labelframe, text='Duration: ').grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        duration_slider = ttk.Scale(params_labelframe, from_=0, to=15, value=2.5, variable=self.duration_var, length=520, command=self.update_duration_label)
        duration_slider.grid(row=3, column=0, padx=10, pady=2, sticky='ew')
        # Duration Value Label
        duration_value_label = ttk.Label(params_labelframe, textvariable=self.duration_label_value)
        duration_value_label.grid(row=2, column=0, padx=70, pady=2, sticky='w')

        # Analyze button
        analyze_button = ttk.Button(analyze_labelframe, text='Analyze', command=self.on_analyze, style='success.TButton')
        analyze_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Analyze progress bar
        analyze_prog_bar = ttk.Progressbar(analyze_labelframe, style='success.Striped.Horizontal.TProgressbar', variable=self.prog_bar_value, maximum=110)
        analyze_prog_bar.grid(row=0, column=1, padx=10, pady=10, sticky='ew')


        # output settings
        ttk.Label(output_labelframe, text="Output file location").grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e2 = ttk.Entry(output_labelframe, textvariable=self.output_folder_path)
        e2.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(output_labelframe, text='Browse', command=self.on_out_browse, style='primary.TButton')
        b2.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        ttk.Label(output_labelframe, text="Output file name").grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e3 = ttk.Entry(output_labelframe, textvariable=self.output_file_name)
        e3.grid(row=1, column=1, sticky='ew', padx=10, pady=2)


        b3 = ttk.Button(output_labelframe, text='Save', command=self.on_save, style='success.TButton')
        b3.grid(row=1, column=2, sticky='ew', pady=2, ipadx=10)

    def return_silences(self, audio, sample_rate, threshold, duration, n_samples):
        # We are going to time this function for benchmarking purposes
        start_time = time.time()

        dB = librosa.amplitude_to_db(abs(audio), ref=np.max)

        # Finding our sample conversion rate based on the number of samples we want to scan each second
        sample_conversion_rate = int(sample_rate / n_samples)

        # Convert duration into samples
        sample_duration = int(sample_rate * duration)

        # Creating a blank list for our start and stop indexes
        a = np.empty((0, 2), int)

        streak = 0
        start_index = 0
        end_index = 0
        i = 0
        j = 0
        active_streak = False

        # Creating a variable to feed to the progress bar
        total_samples = len(dB) / sample_conversion_rate

        # For every value in the dB list
        # add 1 to the sample counter (i)
        # If that value is less than the threshold value && there is no active streak
        # Start a streak. Set the start_index to whatever sample number we are at (i), add 1 to the streak counter
        # Else if that value is less than the threshold value && there is an active streak
        # add one to the streak counter
        # Else if the value is greater than the threshold value && there is an active streak
        # If streak >= sample_duration
        # Set the end_index to whatever sample number we are at (i). Append the start and end indexes to array a.
        # Re-set the start and end indexes to 0. Re-set the streak counter and active_streak to 0/False
        # Else
        # Re-set the start and end indexes to 0. Re-set the streak counter and active_streak to 0/False
        # Else if the value is greater than the threshold value && there is no active streak
        # Do nothing

        below_threshold = dB < threshold
        above_threshold = ~below_threshold
        while i < len(dB):
            # Updating progress bar
            # So, this progress bar part causes a 3 order of magnitude increase in processing time. I NEED to either
            # Get rid of it, or speed it up a lot

            # Turns out that only sending every 1000 times speeds it up a good bit

            if j % 1000 == 0:
                pct_done = ((j / total_samples) * 100) + 10
                self.prog_bar_value.set(pct_done)
                self.update_idletasks()

            if below_threshold[i] and not active_streak:
                streak += 1
                start_index = i
                active_streak = True

            elif below_threshold[i] and active_streak:
                streak += sample_conversion_rate

            elif above_threshold[i] and active_streak:
                if streak >= sample_duration:
                    end_index = i
                    b = np.array([start_index, end_index]).reshape(1, -1)
                    a = np.append(a, b, axis=0)
                    start_index = 0
                    end_index = 0
                    streak = 0
                    active_streak = False
                else:
                    start_index = 0
                    end_index = 0
                    streak = 0
                    active_streak = False
            j += 1
            i = sample_conversion_rate * j

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Final progress bar update
        pct_done = ((j / total_samples) * 100) + 10
        self.prog_bar_value.set(pct_done)
        self.update_idletasks()

        return a


    def update_dB_label(self, event=None):
        """Update the label to show the current dB Value"""
        self.dB_label_value.set(str(round(self.dB_threshold_var.get(), 1)))

    def update_duration_label(self, event=None):
        """Update the label to show the current duration value"""
        self.duration_label_value.set(str(round(self.duration_var.get(), 1)))

    def on_analyze(self):
        """Callback for analyze button press"""
        # This function is going to be the powerhouse of this application. It will do the bulk of the actual work.
        #
        # Function Roadmap:
        # 0. Collect values from sliders, file path box, ect. - DONE
        # 0.1 Update the progress bar 5% to show the load is starting - DONE
        # 1. Load audio using the load audio function - DONE
        #       1.1 Update the progress bar to 10% to show the load is finished - DONE
        # 2. Run return_silences on the audio we loaded in step 1
        # 3. Add some extra functionality to return silences so that the progress bar works - DONE (I think)
        # 4. Update the progress bar - DONE
        # 5. Trigger a popup window with the info about how many splits were found and where they are - DONE
        #       5.1. Proceed/Start over options on that popup window - Done
        # 6. set has_analyzed to True - DONE

        # 0. Collect values from GUI
        file_path = self.file_path_var.get()
        dB_thresh = self.dB_threshold_var.get()
        duration = self.duration_var.get()

        # 0.1 - Update progress bar to 5%
        self.prog_bar_value.set(5)
        self.update_idletasks()

        # 1. Load Audio
        self.audio, self.sample_rate = load_audio(file_path)

        # 1.1 - Update progress bar to 10%
        self.prog_bar_value.set(10)
        self.update_idletasks()

        # 2, 3, 4. - Run return silences
        self.silences = self.return_silences(self.audio, self.sample_rate, dB_thresh, duration, n_samples=samples_per_second)

        # 5. - Display popup window that says "Analysis has finished"
        self.show_analysis_popup(self.silences, self.sample_rate)


        self.has_analyzed = True


    def show_analysis_popup(self, silences, sr):
        # Calculating the midpoints
        mid_pts = []  # List of strings that contain the time stamp of each midpoint
        for i in range(0, silences.shape[0]):
            mid_pt = ((silences[i][1] - silences[i][0]) / 2) + silences[i][0]
            mid_pts.append(samples_2_time(mid_pt, sr))

        popup_title = "Analysis Finished"
        popup_message = f"Analysis has finished. \n\n{len(silences)} split location(s) detected." \
                        f" This will result in {len(silences) + 1} file(s)." \
                        f"\n\nFile will be split at: {mid_pts}." \
                        f"\n\nDo you wish to proceed?"

        result = tkinter.messagebox.askquestion(popup_title, popup_message)

        if result == 'yes':
            pass
        else:
            self.prog_bar_value.set(0)
            self.has_analyzed = False


    def save_popup_warning(self, message:str):
        save_popup_title = "Warning"

        result = tkinter.messagebox.showwarning(save_popup_title, message)


    def on_save(self):
        """Callback for save button press"""

        # 1. Check if has_analyzed = True. If not, prompt user to analyze files first - DONE
        # 2. Read in file name and path - DONE
        # 3. Check if the file name field is blank or equal to the default
        #       3.1. If it is blank, popup with message "Please enter a file name before you save." - DONE
        #       3.2. If it is equal to the default value, popup with message "It looks like you haven't changed the file name. Are you sure you want to name your files "file_name" - DONE
        #           3.2.1. Update save_popup_yn to write the files to memory if the say yes
        # 4. Split files - DONE
        # 5. Create string for full new file name
        # 6. Check if there is a file with the same name already in the save file path
        #       6.1. If there is already file with the same name, popup with message "There is already a file with that name in this location. Would you like to overwrite?"
        # 7. Write files

        # 1. Check has_analyzed
        if self.has_analyzed == False:
            msg = "Please analyze an audio file before trying to save."
            self.save_popup_warning(msg)

        else:
        # 2. Read in file name and path
            save_folder = self.output_folder_path.get()
            save_name = self.output_file_name.get()

        # 3. Check if the file name has been changed or is blank
            if save_name == "":
                msg = "Your output file name is blank. Please enter a valid output file name before saving."
                self.save_popup_warning(msg)
            elif save_name == 'file_name':
                msg = "You didn't change the output file name. Please change the output name and re-save."
                self.save_popup_warning(msg)
            else:
                # 4. Split files
                split_audio = split_file(self.audio, self.silences)

                # 7. Write Files
                for i in range(len(split_audio)):
                    file_name = str(save_folder + "/" + save_name + "-" + str(i + 1) + ".mp3")
                    sf.write(file_name, split_audio[i], self.sample_rate)

                tkinter.messagebox.showinfo(title=None, message="Your files have been saved.")


    def on_in_browse(self):
        """Callback for input browse"""
        path = filedialog.askopenfilename(title='Select an audio file', filetypes=[("Audio Files", "*.wav; *.mp3")])
        if path:
            self.file_path_var.set(path)

        self.has_analyzed = False
        self.prog_bar_value.set(0)

    def on_out_browse(self):
        """Callback for output browse"""
        path = askdirectory(title='Select directory')
        if path:
            self.output_folder_path.set(path)

# Running the main application
if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()
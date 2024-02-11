import numpy as np
import librosa
import soundfile as sf
import time
from icecream import ic


# Roadmap and feature wishlist:
# 1. Get the basic app working in an IDE environment - DONE
# 1.5 Performance optimization - only analyze every nth sample
# 2. Error proof the user input sections
# 3. Add progress bars
# 4. Add more user control ex. ignore silence in first/last X:XX of the audio file
# 5. More control over naming of split, output files
# 6. Make a .exe for the app, so it can run outside an IDE
# 7. GUI???
# 8. More advanced processing/chapter detection methods (AI??)

# App startup function. This runs when the app starts and takes in the required info from the user
# NOTE: The user input sections of this function are not error proofed at all. This is something you could come back to
# once the thing is functioning
def startup():
    # Startup Message
    print("Welcome to the audio book splitter app.")
    print("This app will split the desired audio file into smaller files wherever there are long silences.")

    # Asking user for the file path to the audio file
    file_path = str(input("Please enter the file path to the audio file you want to split [NO QUOTATION MARKS!]: "))

    # Asking user for dB cutoff and duration
    print("Please enter your desired dB cutoff value. This should be a number between -80 and 0. We recommend -40.")
    dB_Thresh = float(input("dB Cutoff: "))

    print("Please enter the minimum length of silence you want to scan for in seconds. "
          "Any pauses or silences shorter than this value will not result in an audio split."
          " We recommend starting around 3 seconds.")
    duration = float(input("Duration: "))
    return file_path, dB_Thresh, duration


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


def return_silences(audio, sample_rate, threshold, duration, n_samples):
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
        #ic(i)

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

    a = np.array(a)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Book Splitter identified " + str(a.shape[0]) + " split location(s). This will result in " +
          str(a.shape[0] + 1) + " files.")

    print(f"Book Splitter took {elapsed_time} seconds to complete.")

    time_stamps = str(input("Would you like to see the time stamps for each split location? [y/n]"))
    time_stamps = time_stamps.lower()

    if time_stamps == "y":
        # Find the midpoint of the silence stored in each row of a
        mid_pts = []  # List of strings that contain the time stamp of each midpoint
        for i in range(0, a.shape[0]):
            mid_pt = ((a[i][1] - a[i][0]) / 2) + a[i][0]
            mid_pts.append(samples_2_time(mid_pt, sample_rate))
        print("The timestamps for each split location are: ")
        print(mid_pts)
        print("If the number or location of these splits seems incorrect, "
              "please quit the program and re-try with different input parameters.")
    else:
        print("If this number of splits seems incorrect, "
              "please quit the program and re-try with different input parameters.")

    return a


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


# The actual running of the app happens here:
startup_time_start = time.time()
path, dB_cutoff, duration = startup()
startup_time_end = time.time()
startup_time = startup_time_end - startup_time_start
#ic(startup_time)
load_timer_start = time.time()
audio, sample_rate = load_audio(path)
load_timer_end = time.time()
load_timer = load_timer_end - load_timer_start
#ic(load_timer)
silences_timer_start = time.time()
silences = return_silences(audio, sample_rate, dB_cutoff, duration, n_samples=30)
silences_timer_end = time.time()
silences_timer = silences_timer_end - silences_timer_start


audio_chunks = split_file(audio, silences)
write_files(audio_chunks, sample_rate)

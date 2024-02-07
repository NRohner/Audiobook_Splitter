import numpy as np
import librosa
import soundfile as sf

# Roadmap and feature wishlist:
# 1. Get the basic app working in an IDE environment
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
    audio, sample_rate = librosa.load(file_path)

    return audio, sample_rate

# Function to convert samples into time
def samples_2_time(sample_num, sample_rate):
    total_seconds = sample_num * (1 / sample_rate)
    hours = int(total_seconds / 3600)
    minutes = int(((total_seconds / 3600) - hours) * 60)
    seconds = int(((((total_seconds / 3600) - hours) * 60) - minutes) * 60)

    time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds)

    return time_string

def return_silences(audio, sample_rate, threshold, duration):
    dB = librosa.amplitude_to_db(abs(audio), ref=np.max)

    # Convert duration into samples
    sample_duration = int(sample_rate * duration)

    # Creating a blank list for our start and stop indexes
    a = []

    streak = 0
    start_index = 0
    end_index = 0
    i = 0
    active_streak = False

# For every value in the dB list
    # add 1 to the sample counter (i)
    # If that value is less than the threshold value && there is no active streak
        # Start a streak. Set the start_index to whatever sample number we are at (i), add 1 to the streak counter
    # Else if that value is less than the threshold value && there is an active streak
        # add one to the streak counter
    # Else if the value is greater than the threshold value && there is an active streak
        #If streak >= sample_duration
            # Set the end_index to whatever sample number we are at (i). Append the start and end indexes to array a.
            # Re-set the start and end indexes to 0. Re-set the streak counter and active_streak to 0/False
        #Else
    # Re-set the start and end indexes to 0. Re-set the streak counter and active_streak to 0/False
    # Else if the value is greater than the threshold value && there is no active streak
        # Do nothing

    for value in dB:
        i += 1
        if (value < threshold) and not active_streak:
            streak += 1
            start_index = i
            active_streak = True

        elif (value < threshold) and active_streak:
            streak += 1

        elif (value >= threshold) and active_streak:
            if streak >= sample_duration:
                end_index = i
                b = [start_index, end_index]
                a.append(b)
                start_index = 0
                end_index = 0
                streak = 0
                active_streak = False
            else:
                start_index = 0
                end_index = 0
                streak = 0
                active_streak = False


    a = np.array(a)

    print("Book Splitter identified " + str(a.shape[0]) + " split location(s). This will result in " +
          str(a.shape[0] + 1) + " files.")

    time_stamps = str(input("Would you like to see the time stamps for each split location? [y/n]"))
    time_stamps = time_stamps.lower()

    if time_stamps == "y":
        # Find the midpoint of the silence stored in each row of a
        mid_pts = []    # List of strings that contian the time stamp of each midpoint
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
        split_audio.append(audio[mid_pts[j]:mid_pts[j+1]])

    # Adding the last audio segment between the last split point and the end of the file
    split_audio.append(audio[mid_pts[-1]:])

    return split_audio

# Function to write the split files to memory
def write_files(audio_chunks):
    # Prompting user if they want to split and write the files
    proceed = str(input("Do you want to proceed and split the file and save the resulting audio chunks? [y/n]"))
    proceed = proceed.lower()

    if proceed == "y":
        # Prompt for destination folder path
        dest_path = str(input("Please enter the folder path to the location you want to save the new audio files"
                              " [NO QUOTATION MARKS!]: "))
        # Write the files
        print("len(audio_chunks) = " + str(len(audio_chunks)))
        for i in range(len(audio_chunks)):
            print("i = " + str(i))



    #else:

# The actual running of the app happens here:

path, dB_cutoff, duration = startup()
audio, sample_rate = load_audio(path)
silences = return_silences(audio, sample_rate, dB_cutoff, duration)

audio_chunks = split_file(audio, silences)
#write_files(audio_chunks)



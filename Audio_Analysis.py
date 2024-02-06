import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from itertools import cycle

from glob import glob

import librosa
import librosa.display

# Settings for the silence finder
dB_Thresh = -40  # Threshold value below which we consider something "silent"
duration = 3  # Value in seconds of time duration we want the silence to be longer than.

# Loading the audio file
audio_files = glob('../Audio_Book_Chapters/Audio/*.mp3')
y, sr = librosa.load("D:\clipping.mp3")
y_ser = pd.Series(y)

# Calculating the dB values
d = librosa.amplitude_to_db(abs(y), ref=np.max)
d_ser = pd.Series(d)

def return_silences(audio, sample_rate, threshold, duration):
    dB = librosa.amplitude_to_db(abs(audio), ref=np.max)

    # Convert duration into samples
    sample_duration = sample_rate * duration

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
    return a

silence_index = return_silences(y, sr, dB_Thresh, duration)

print(silence_index)



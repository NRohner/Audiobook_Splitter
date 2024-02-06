import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from itertools import cycle

from glob import glob

import librosa
import librosa.display


sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

audio_files = glob('../Audio_Book_Chapters/Audio/*.mp3')    #Making a list of all the mp3 files we have in the Audio subfolder


#Loading in the audio data

#Loading Dune Clip
#y, sr = librosa.load(r'E:\BigTor\Dune - Audiobook Collection 2015\01 - Dune Saga\mp3\clipping.mp3')    #Loading the first file in our list we created above 'audio_files'. librosa.load outputs 'y' and 'sample rate (sr)'.
                                        # y is the raw data of the audio file. sample rate is an int value of the sample rate

#Loading shorter audiofile
y, sr = librosa.load(audio_files[1])

pd.Series(y).plot()
plt.show()

#I dont have full understanding of what's going on in this section but I know we are doing an fft of the audio file
# With the ultimate goal of finding the dB values at each sample position and then finding the max dB value
#n_fft = 2048
#S = librosa.stft(y, n_fft=n_fft, hop_length=n_fft//2)
#print(S.shape)



#Convert to dB
D = librosa.amplitude_to_db(np.abs(y), ref=np.max)
print("Shape of D: " + str(np.shape(D)))
maxdB = np.max(abs(D))
mindB = np.min(abs(D))
avgdB = np.mean(abs(D))

print("Max dB: " + str(maxdB))
print("Min dB: " + str(mindB))
print("Mean dB: " + str(avgdB))

nonMuteSections = librosa.effects.split(y)

print(len(nonMuteSections))


# Audio_Book_Chapters
 Python script to split large audiobook files into chapters

There is both a GUI and a terminal based version of this app.
They can be found in their respective folders.


Instructions:

This program identifies chapter breaks in audiobook and long auido
files by looking for periods of silence within the file. You can tell
the program how 'silent' it really needs to be by adjusting the 
dB threshold slider. The larger the value, the louder the program will
consider 'silence' to be. I recommend a value of around -40dB.
The duration slider tells the program how long a silent period needs to be
to count as a chapter break. This will vary with each audiobook. I recomend 
starting somewhere around the 2.5 - 3 second range and adjusting from there.
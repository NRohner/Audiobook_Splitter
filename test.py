import numpy as np
import matplotlib.pyplot as plt

def samples_2_time(sample_num, sample_rate):
    total_seconds = sample_num * (1 / sample_rate)
    hours = int(total_seconds / 3600)
    minutes = int(((total_seconds / 3600) - hours) * 60)
    seconds = int(((((total_seconds / 3600) - hours) * 60) - minutes) * 60)

    time_string = str(hours) + ":" + str(minutes) + ":" + str(seconds)

    return time_string


time = samples_2_time(51207691, 22050)

print(time)

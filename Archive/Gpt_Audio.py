import librosa
import numpy as np

from glob import glob


audio_files = glob('../Audio_Book_Chapters/Audio/*.mp3')


def find_mute_sections(audio_file_path, threshold=20):
    # Load the audio file
    y, sr = librosa.load(audio_file_path, sr=None)

    # Calculate the dB values
    db_values = librosa.amplitude_to_db(np.abs(y), ref=np.max)

    # Find the mute sections based on the threshold
    mute_sections = np.where(db_values < threshold)[0]

    print(len(y))

    return mute_sections

# Example usage
mute_sections = find_mute_sections(audio_files[1])

print(len(mute_sections))
print("Mute Sections Sample Indices:", mute_sections)
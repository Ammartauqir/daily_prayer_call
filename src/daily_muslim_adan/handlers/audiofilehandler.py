import threading
from pydub import AudioSegment
from pydub.playback import play
import os
from pydub.utils import which
print(which("ffmpeg"))

def play_wav(file_path):
    audio = AudioSegment.from_wav(file_path)
    play(audio)


def play_sound_in_thread(file_path):
    thread = threading.Thread(target=play_wav, args=(file_path,), daemon=True)
    thread.start()


# Example usage
wav_adan_filepath = os.path.abspath(os.path.join("data", "adan2.mp3"))
print(wav_adan_filepath)
sound = AudioSegment.from_mp3(wav_adan_filepath)
sound.export("adhan.wav", format="wav")  # Convert to WAV
# play(AudioSegment.from_wav("adhan.wav"))
play_sound_in_thread("adhan.wav")


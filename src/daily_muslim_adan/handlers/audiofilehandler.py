import simpleaudio as sa
import threading


class AudioPlayer:
    def __init__(self):
        self.audio_thread = None
        self.playing_audio = False

    def play_audio(self, file_path):
        """
        Plays the audio file in a separate thread if no other audio is playing.
        """
        if self.playing_audio:
            return  # Prevent multiple overlapping audio plays
        self.playing_audio = True  # Set flag before playing

        def audio_finished():
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait for playback to finish
            self.playing_audio = False  # Reset flag after audio finishes

        # Start audio in a new thread
        self.audio_thread = threading.Thread(target=audio_finished, daemon=True)
        self.audio_thread.start()

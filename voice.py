import pyaudio
import wave
import whisper
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# # Parameters for recording
# CHUNK = 1024  # Number of audio frames per buffer
# FORMAT = pyaudio.paInt16  # Format for audio stream
# CHANNELS = 1  # Mono audio
# RATE = 44100  # Sampling rate (44.1 kHz)
# RECORD_SECONDS = 10  # Duration of recording
# OUTPUT_FILE = "output.mp4"  # File to save the recording

# # Initialize PyAudio
# audio = pyaudio.PyAudio()

# # Open the audio stream
# stream = audio.open(format=FORMAT, channels=CHANNELS,
#                     rate=RATE, input=True,
#                     frames_per_buffer=CHUNK)

# print("Recording...")

# frames = []

# # Record audio in chunks
# for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("Finished recording!")

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# audio.terminate()

# # Save the recording to a file
# with wave.open(OUTPUT_FILE, 'wb') as wf:
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(audio.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))

# print(f"Audio saved to {OUTPUT_FILE}")


class Record_Voice():

    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 10
        self.OUTPUT_FILE = "output.wav"
        self.frames = []

    def start_recording(self):

        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)

        print("Recording...")


        # Record audio in chunks
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        self.save_recording_file(audio)

    def save_recording_file(self,audio):

        with wave.open(self.OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))

        print(f"Audio saved to {self.OUTPUT_FILE}")

    
    def fetch_transcript(self):
        model = whisper.load_model("base")
        result = model.transcribe(self.OUTPUT_FILE)

        print("Transcription:")
        print(result["text"])


recorder = Record_Voice()

recorder.start_recording()
recorder.fetch_transcript()
import pyaudio
import wave
import whisper
import warnings
import os
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
import assemblyai as aai


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
        aai.settings.api_key = "6fc33d41f46a4c908b132acb3b48f2d6"

        transcriber = aai.Transcriber()

        audio_file = (
            self.OUTPUT_FILE
        )

        config = aai.TranscriptionConfig(speaker_labels=True)

        transcript = transcriber.transcribe(audio_file, config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            exit(1)

        print(transcript.text)

        for utterance in transcript.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")


recorder = Record_Voice()

recorder.start_recording()
recorder.fetch_transcript()
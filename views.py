import gradio as gr
import wave

# Function to save audio to a file
def save_audio_to_file(audio):
    if audio is None:
        return "No audio was recorded!"

    file_path, sample_rate = audio  # `audio` is a tuple (file_path, sample_rate)

    # Read the recorded audio file
    with open(file_path, "rb") as f:
        audio_data = f.read()

    # Save the audio to a new file (e.g., "output.wav")
    output_file = "output.wav"
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(1)  # Assuming mono audio
        wf.setsampwidth(2)  # Assuming 16-bit audio (2 bytes)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

    return f"Audio successfully saved to {output_file}!"

# Gradio Interface
interface = gr.Interface(
    fn=save_audio_to_file,
    inputs=gr.Audio(type="filepath", label="Record or Upload Audio"),  # Capture audio
    outputs="text",  # Text output to indicate save status
    live=False  # Disable live mode for non-streaming use
)

interface.launch()

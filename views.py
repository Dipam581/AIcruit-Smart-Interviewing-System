import gradio as gr
import speech_recognition as sr

# Function to process the audio input
def process_audio(audio):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            response = f"Received: {text}."
    except Exception as e:
        response = "Could not recognize your voice."
    return response

# Gradio Interface
with gr.Blocks() as voice_assistant:
    gr.Markdown("## Voice Assistant")
    gr.Markdown("Talk to the assistant by recording your voice.")
    audio_input = gr.Audio(type="filepath", label="Upload or Record Your Voice")
    
    with gr.Row():
        output = gr.Textbox(label="Assistant Response")
        audio_input.change(process_audio, inputs=audio_input, outputs=output)
        response = gr.Textbox()
    
    submit = gr.Button("Submit")

voice_assistant.launch(debug=True)

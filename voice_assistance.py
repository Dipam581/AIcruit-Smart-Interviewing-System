import streamlit as st
import assemblyai as aai
import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
import time
import pyttsx3


os.environ["MISTRAL_API_KEY"] = "PAPSilB8Xtq8IjvensOxoVdjkRuke2oi"


class VoiceAchiver():

    def __init__(self):
        self.audio_file = "recorded_audio.wav"
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

    def fetch_transcript(self):
        aai.settings.api_key = "6fc33d41f46a4c908b132acb3b48f2d6"

        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(speaker_labels=True)
        transcript = transcriber.transcribe(self.audio_file, config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            exit(1)

        return transcript.text


    def get_response_from_llm(self,transcript):
        
        model = ChatMistralAI(model="mistral-large-latest")
        system_template = '''You are an interviewer conducting an interview for a Data Science and Artificial Intelligence role. 
                            The candidate answers your questions, and your task is to respond by asking follow-up questions based on their answers. 

                            Your follow-up questions should:
                            - Be thoughtful and tailored to the candidate's responses.
                            - Gradually increase in difficulty to evaluate the candidate's depth of knowledge and problem-solving skills.
                            - Be detailed and well-structured, avoiding overly brief or vague phrasing.

                            Maintain a professional tone throughout the interview.'''


        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        prompt = prompt_template.invoke({ "text": transcript})

        response = model.invoke(prompt)
        return response.content
    
    def play_audio(self,file):
        audio_file = open(file, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

    def convert_msg_to_audio(self, text):
        self.tts_engine.save_to_file(text, self.audio_file)
        self.tts_engine.runAndWait()
        self.play_audio(self.audio_file)
        
vc = VoiceAchiver()



st.title("Voice-Assisted Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

audio_input = st.audio_input("Please give the answer")


if audio_input:
    with st.spinner('Analyzing...'):

        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_input.read())
        
        text_input = vc.fetch_transcript()
        

        st.chat_message("user").markdown(text_input)
        st.session_state.messages.append({"role": "user", "content": text_input})
        
        bot_response = vc.get_response_from_llm(text_input)
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        vc.convert_msg_to_audio(bot_response)

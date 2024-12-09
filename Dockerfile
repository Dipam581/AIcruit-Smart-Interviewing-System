FROM python:3.12

WORKDIR /voiceassistance

COPY . /voiceassistance

# Install dependencies for eSpeak-ng
RUN apt-get update && \
    apt-get install -y espeak-ng

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8503

CMD ["streamlit", "run", "voice_assistance.py", "--server.port=8501"]

# docker build -t voiceassistance . 
# docker run -p 8501:8501 voiceassistance
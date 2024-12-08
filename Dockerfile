FROM python:3.12

WORKDIR /voiceassistance

COPY . /voiceassistance

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8503

CMD ["streamlit", "run", "voice_assistance.py", "--server.port=8501"]

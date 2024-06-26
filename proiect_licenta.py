from pathlib import Path
from openai import OpenAI
import os
import dotenv
from playsound import playsound
from devices import record
from pvrecorder import PvRecorder
import wave
import struct

dotenv.load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #improting openai api key from env vars

def record():
    recorder = PvRecorder(device_index=1, frame_length=512)
    audio = []
    path = 'input.wav'
    try:
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()
        with wave.open(path, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()


def speech_to_text():
    input_audio_file=open("input.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=input_audio_file,
    # language="ro"
    )
    print(transcription.text)
    return transcription.text

def assistant_request(context, text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        # max_tokens=300,
    )

    raspuns = completion.choices[0].message.content
    # print(raspuns)
    return raspuns


def text_to_speech(raspuns):
    file_path = Path(__file__).parent / "output.mp3"
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=raspuns
        ) as  response:
            response.stream_to_file(file_path)

def main():
    context = ""
    while True:
        try:
            record()
            text=speech_to_text()
            response=assistant_request(context, text)
            text_to_speech(response)
            context = context + "\nuser question: " + text + "\nchatgpt response: " + response 
            playsound('C:/Users/roman/VS_Code/Licenta/output.mp3')
        except KeyboardInterrupt:
            print("Program incheiat!!!")
            exit()
if __name__ == "__main__":
    main()
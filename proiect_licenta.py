from pathlib import Path
from openai import OpenAI
import os
import dotenv
# import json
from playsound import playsound
from devices import record

dotenv.load_dotenv()


context = "limba vorbita: romana"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #improting openai api key from env vars
while True:
    record()
    input_audio_file=open("input.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=input_audio_file
    language="romanian"
    )

    print(transcription.text)

    

    completion = client.chat.completions.create(
        model="gpt-4o",
        # response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": transcription.text,
            },
        ],
        # max_tokens=300,
    )

    raspuns = completion.choices[0].message.content
    # for key in raspuns:
    #     print(type(raspuns[key]))
    # print(completion.choices[0].message)
    print(raspuns)

    context = context + "\nuser question: " + transcription.text + "\nchatgpt response: " + raspuns 
    
    file_path = Path(__file__).parent / "output.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=raspuns
    )

    response.stream_to_file(file_path)
    # response.with_streaming_response.methond()

    playsound('C:/Users/roman/VS_Code/Licenta/output.mp3')

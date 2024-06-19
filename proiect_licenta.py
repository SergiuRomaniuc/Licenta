from pathlib import Path
from openai import OpenAI
import os
import dotenv
import json

dotenv.load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #improting openai api key from env vars

completion = client.chat.completions.create(
    model="gpt-4o",
    # response_format={ "type": "json_object" },
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant in the form of an intelligent speaker. You do not show text as response, but rather speak with the user.",
        },
        {
            "role": "user",
            "content": "Salut asistentule, spune-mi despre tine, cine esti si cum functionezi, si povesteste-mi o istoriara interesanta.",
        },
    ],
    # max_tokens=300,
)

raspuns = completion.choices[0].message.content
# for key in raspuns:
#     print(type(raspuns[key]))
# print(completion.choices[0].message)
print(raspuns)

file_path = Path(__file__).parent / "output.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=raspuns
)

response.stream_to_file(file_path)
# response.with_streaming_response.methond()

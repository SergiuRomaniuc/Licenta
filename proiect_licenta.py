from openai import OpenAI
import os
import dotenv
import json

dotenv.load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #improting openai api key from env vars

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={ "type": "json_object" },
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. You output JSON.",
        },
        {
            "role": "user",
            "content": "Poti sa imi spui despre tine, cine esti ?",
        },
    ],
)

raspuns = json.loads(completion.choices[0].message.content)
for key in raspuns:
    print(type(raspuns[key]))
print(completion.choices[0].message)



response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input=raspuns[list(raspuns)[0]],
)

response.stream_to_file("output.mp3")
# response.with_streaming_response.methond()

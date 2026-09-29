import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key=os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('Gemini api key is not set')
client=genai.Client(api_key=api_key)

MODEL='gemini-3.6-flash'

def generate_response(prompt:str,temperature:float=0.7) -> str:
    response=client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature
        )
    )

    return response.text




from fastapi import FastAPI, Depends
from openai import OpenAI
from keyHelper import verify_api_key
from keyInfo import API_KEY_DATA
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):

    user = API_KEY_DATA[x_api_key]
    user["credits"] -= 1

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "response": response.choices[0].message.content,
        "credits_left": user["credits"],
        "reset_time": user["reset_time"]
    }
from fastapi import FastAPI, Depends
import ollama
from keyHelper import verify_api_key
from keyInfo import API_KEY_DATA

app = FastAPI()


@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):

    user = API_KEY_DATA[x_api_key]
    user["credits"] -= 1

    response = ollama.chat(
        model="llama2",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "response": response["message"]["content"],
        "credits_left": user["credits"],
        "reset_time": user["reset_time"]
    }
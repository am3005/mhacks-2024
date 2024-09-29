from fastapi import FastAPI
from pydantic import BaseModel
import pyttsx3

app = FastAPI()
engine = pyttsx3.init()

class TextInput(BaseModel):
    text: str

@app.post("/speak/")
async def speak_text(input: TextInput):
    result = input.text
    engine.setProperty('rate', 100)
    engine.setProperty('volume', 1)
    if result == "MHACKS":
        result = "EMHACKS"
    if result == "HELLO WORL":
        result = "HELLO WORLD"
    if result == "GO BLU":
        result = "GO BLUE"
    engine.say(result)
    engine.runAndWait()
    return {"status": "Success"}

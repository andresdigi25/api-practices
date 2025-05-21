from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from datetime import datetime
import os
from typing import List, Dict, Optional
import speech_recognition as sr
import pyttsx3
import ollama

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StandupData(BaseModel):
    date: str
    team_members: Dict[str, Dict[str, str]]

class ScrumMaster:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.standup_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "team_members": {}
        }
        self.mic_index = None

    def get_joke(self, context: str) -> str:
        response = ollama.chat(model="mistral", messages=[
            {
                'role': 'user',
                'content': f"Based on this standup update: {context} Tell me a short, work-appropriate joke related to software development or team work."
            }
        ])
        return response['message']['content']

    def get_scrum_joke(self) -> str:
        response = ollama.chat(model="mistral", messages=[
            {
                'role': 'user',
                'content': "Tell me a short, work-appropriate joke about Agile methodology or Scrum Masters."
            }
        ])
        return response['message']['content']

    def save_standup(self):
        if not os.path.exists("standups"):
            os.makedirs("standups")
        filename = f"standups/standup_{self.standup_data['date']}.json"
        with open(filename, 'w') as f:
            json.dump(self.standup_data, f, indent=4)
        return filename

scrum_master = ScrumMaster()

@app.get("/")
async def root():
    return {"message": "Scrum Master Bot API"}

@app.get("/api/microphones")
async def get_microphones():
    return {"microphones": sr.Microphone.list_microphone_names()}

@app.post("/api/select-microphone")
async def select_microphone(mic_index: int):
    if 0 <= mic_index < len(sr.Microphone.list_microphone_names()):
        scrum_master.mic_index = mic_index
        return {"message": f"Selected microphone: {sr.Microphone.list_microphone_names()[mic_index]}"}
    raise HTTPException(status_code=400, detail="Invalid microphone index")

@app.post("/api/process-audio")
async def process_audio(audio_data: bytes):
    if scrum_master.mic_index is None:
        raise HTTPException(status_code=400, detail="Microphone not selected")
    
    with sr.Microphone(device_index=scrum_master.mic_index) as source:
        scrum_master.recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            text = scrum_master.recognizer.recognize_google(audio_data)
            return {"text": text}
        except sr.UnknownValueError:
            raise HTTPException(status_code=400, detail="Could not understand audio")
        except sr.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.post("/api/add-team-member")
async def add_team_member(update: Dict[str, str]):
    name = update.get("name")
    yesterday = update.get("yesterday")
    today = update.get("today")
    blockers = update.get("blockers")

    if not all([name, yesterday, today, blockers]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    scrum_master.standup_data["team_members"][name] = {
        "yesterday": yesterday,
        "today": today,
        "blockers": blockers
    }

    context = f"{name} worked on {yesterday} yesterday, plans to work on {today} today, and has blockers: {blockers}"
    joke = scrum_master.get_joke(context)
    
    return {
        "message": "Team member added successfully",
        "joke": joke
    }

@app.post("/api/end-standup")
async def end_standup():
    filename = scrum_master.save_standup()
    final_joke = scrum_master.get_scrum_joke()
    return {
        "message": "Standup ended successfully",
        "filename": filename,
        "final_joke": final_joke
    }

@app.get("/api/standup-history")
async def get_standup_history():
    if not os.path.exists("standups"):
        return {"standups": []}
    
    standups = []
    for filename in os.listdir("standups"):
        if filename.endswith(".json"):
            with open(f"standups/{filename}", 'r') as f:
                standups.append(json.load(f))
    
    return {"standups": standups}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
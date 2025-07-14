import edge_tts
import asyncio
import uuid
import os

OUTPUT_DIR = "static/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def _synthesize(text, voice, file_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def synthesize_speech(text, language="english"):
    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(OUTPUT_DIR, filename)
    voice = "en-IN-NeerjaNeural" if language == "hindi" else "en-US-AriaNeural"

    asyncio.run(_synthesize(text, voice, file_path))
    return f"/{file_path}"  # Return relative URL for frontend
